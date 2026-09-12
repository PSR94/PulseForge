from __future__ import annotations

import hashlib
import urllib.parse
import xml.etree.ElementTree as ET
from datetime import UTC, datetime

from pulseforge.config import Settings
from pulseforge.connectors.base import Connector
from pulseforge.connectors.http import fetch_bounded
from pulseforge.domain.models import Document, Source, SourceType

ATOM = {"a": "http://www.w3.org/2005/Atom"}


class ArxivConnector(Connector):
    source_type = SourceType.ARXIV

    def __init__(self, settings: Settings):
        self.settings = settings

    async def fetch(self, source: Source, *, since: datetime | None = None) -> list[Document]:
        query = source.metadata.get("query") or source.name
        url = "https://export.arxiv.org/api/query?" + urllib.parse.urlencode(
            {"search_query": f"all:{query}", "start": 0, "max_results": 50, "sortBy": "submittedDate", "sortOrder": "descending"}
        )
        body, _ = await fetch_bounded(url, self.settings, accept="application/atom+xml")
        root = ET.fromstring(body)
        now = datetime.now(UTC)
        docs: list[Document] = []
        for entry in root.findall("a:entry", ATOM):
            title = " ".join((entry.findtext("a:title", default="", namespaces=ATOM)).split())
            content = " ".join((entry.findtext("a:summary", default="", namespaces=ATOM)).split())
            canonical = entry.findtext("a:id", default=str(source.source_url), namespaces=ATOM)
            published_raw = entry.findtext("a:published", default="", namespaces=ATOM)
            published = datetime.fromisoformat(published_raw.replace("Z", "+00:00")) if published_raw else now
            if since and published < since:
                continue
            digest = hashlib.sha256((canonical + "\n" + content).encode()).hexdigest()
            docs.append(
                Document(
                    id=f"doc-arxiv-{digest[:24]}",
                    workspace_id=source.workspace_id,
                    source_id=source.id,
                    source_type=SourceType.ARXIV,
                    source_url=source.source_url,
                    canonical_url=canonical,
                    retrieved_at=now,
                    published_at=published,
                    content_hash=digest,
                    title=title,
                    content=content,
                    metadata={"connector": "arxiv", "query": query},
                )
            )
        return docs
