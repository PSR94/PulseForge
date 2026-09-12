from __future__ import annotations

import hashlib
import json
from datetime import UTC, datetime
from urllib.parse import urljoin

from pulseforge.config import Settings
from pulseforge.connectors.base import Connector
from pulseforge.connectors.http import fetch_bounded
from pulseforge.domain.models import Document, Source, SourceType


class JsonFeedConnector(Connector):
    source_type = SourceType.JSON

    def __init__(self, settings: Settings):
        self.settings = settings

    async def fetch(self, source: Source, *, since: datetime | None = None) -> list[Document]:
        body, response = await fetch_bounded(
            str(source.source_url), self.settings, accept="application/json"
        )
        payload = json.loads(body)
        items = payload if isinstance(payload, list) else payload.get("items", payload.get("results", []))
        documents: list[Document] = []
        now = datetime.now(UTC)
        for index, item in enumerate(items[:500]):
            if not isinstance(item, dict):
                continue
            title = str(item.get("title") or item.get("name") or f"Item {index + 1}")
            content = str(item.get("content_text") or item.get("content") or item.get("summary") or "")
            raw_url = str(item.get("url") or item.get("external_url") or response.url)
            canonical = urljoin(str(response.url), raw_url)
            published_raw = item.get("date_published") or item.get("published_at")
            try:
                published = datetime.fromisoformat(str(published_raw).replace("Z", "+00:00")) if published_raw else now
            except ValueError:
                published = now
            if since and published < since:
                continue
            digest = hashlib.sha256((canonical + "\n" + content).encode()).hexdigest()
            documents.append(
                Document(
                    id=f"doc-json-{digest[:24]}",
                    workspace_id=source.workspace_id,
                    source_id=source.id,
                    source_type=SourceType.JSON,
                    source_url=source.source_url,
                    canonical_url=canonical,
                    retrieved_at=now,
                    published_at=published,
                    content_hash=digest,
                    title=title[:500],
                    content=content,
                    metadata={"connector": "json", "raw_id": item.get("id")},
                )
            )
        return documents
