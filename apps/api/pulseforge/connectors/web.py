from __future__ import annotations

import hashlib
import re
from datetime import UTC, datetime
from html import unescape

from pulseforge.config import Settings
from pulseforge.connectors.base import Connector
from pulseforge.connectors.http import fetch_bounded
from pulseforge.domain.models import Document, Source, SourceType

_TITLE = re.compile(r"<title[^>]*>(.*?)</title>", re.I | re.S)
_TAGS = re.compile(r"<[^>]+>")
_SCRIPTS = re.compile(r"<(script|style)[^>]*>.*?</\1>", re.I | re.S)


class WebPageConnector(Connector):
    source_type = SourceType.WEB

    def __init__(self, settings: Settings):
        self.settings = settings

    async def fetch(self, source: Source, *, since: datetime | None = None) -> list[Document]:
        body, response = await fetch_bounded(str(source.source_url), self.settings, accept="text/html")
        html = body.decode(response.encoding or "utf-8", errors="replace")
        title_match = _TITLE.search(html)
        title = unescape(_TAGS.sub("", title_match.group(1))).strip() if title_match else source.name
        clean = _SCRIPTS.sub(" ", html)
        clean = unescape(_TAGS.sub(" ", clean))
        content = " ".join(clean.split())
        now = datetime.now(UTC)
        canonical = str(response.url)
        digest = hashlib.sha256((canonical + "\n" + content).encode()).hexdigest()
        return [
            Document(
                id=f"doc-web-{digest[:24]}",
                workspace_id=source.workspace_id,
                source_id=source.id,
                source_type=SourceType.WEB,
                source_url=source.source_url,
                canonical_url=canonical,
                retrieved_at=now,
                published_at=now,
                content_hash=digest,
                title=title[:500],
                content=content,
                metadata={"connector": "web"},
            )
        ]
