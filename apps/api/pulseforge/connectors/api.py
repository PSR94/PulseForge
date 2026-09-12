from __future__ import annotations

import hashlib
import json
from datetime import UTC, datetime

from pulseforge.config import Settings
from pulseforge.connectors.base import Connector
from pulseforge.connectors.http import fetch_bounded
from pulseforge.domain.models import Document, Source, SourceType


class PublicAPIConnector(Connector):
    """Read-only connector for public JSON APIs.

    Authentication secrets are intentionally not accepted from browser-supplied source metadata.
    Deployments that need authenticated APIs should provide a server-side connector adapter.
    """

    source_type = SourceType.API

    def __init__(self, settings: Settings):
        self.settings = settings

    async def fetch(self, source: Source, *, since: datetime | None = None) -> list[Document]:
        body, response = await fetch_bounded(
            str(source.source_url), self.settings, accept="application/json"
        )
        payload = json.loads(body)
        configured_path = str(source.metadata.get("items_path") or "").strip()
        for segment in [part for part in configured_path.split(".") if part]:
            if isinstance(payload, dict):
                payload = payload.get(segment, [])
        items = payload if isinstance(payload, list) else [payload]
        now = datetime.now(UTC)
        documents: list[Document] = []
        for index, item in enumerate(items[:500]):
            if not isinstance(item, dict):
                item = {"value": item}
            content = json.dumps(item, sort_keys=True, ensure_ascii=False)
            title = str(
                item.get("title")
                or item.get("name")
                or item.get("id")
                or f"{source.name} item {index + 1}"
            )
            canonical = str(item.get("url") or response.url)
            digest = hashlib.sha256((canonical + "\n" + content).encode()).hexdigest()
            documents.append(
                Document(
                    id=f"doc-api-{digest[:24]}",
                    workspace_id=source.workspace_id,
                    source_id=source.id,
                    source_type=SourceType.API,
                    source_url=source.source_url,
                    canonical_url=canonical,
                    retrieved_at=now,
                    published_at=now,
                    content_hash=digest,
                    title=title[:500],
                    content=content,
                    metadata={"connector": "api", "index": index},
                )
            )
        return documents
