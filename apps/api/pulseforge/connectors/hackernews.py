from __future__ import annotations

import hashlib
import json
from datetime import UTC, datetime

from pulseforge.config import Settings
from pulseforge.connectors.base import Connector
from pulseforge.connectors.http import fetch_bounded
from pulseforge.domain.models import Document, Source, SourceType


class HackerNewsConnector(Connector):
    source_type = SourceType.HACKER_NEWS

    def __init__(self, settings: Settings):
        self.settings = settings

    async def fetch(self, source: Source, *, since: datetime | None = None) -> list[Document]:
        body, _ = await fetch_bounded(
            "https://hacker-news.firebaseio.com/v0/newstories.json",
            self.settings,
            accept="application/json",
        )
        ids = json.loads(body)[:60]
        now = datetime.now(UTC)
        docs: list[Document] = []
        for item_id in ids:
            item_body, _ = await fetch_bounded(
                f"https://hacker-news.firebaseio.com/v0/item/{item_id}.json",
                self.settings,
                accept="application/json",
            )
            item = json.loads(item_body)
            if not item or item.get("type") != "story":
                continue
            published = datetime.fromtimestamp(item.get("time", int(now.timestamp())), tz=UTC)
            if since and published < since:
                continue
            canonical = item.get("url") or f"https://news.ycombinator.com/item?id={item_id}"
            content = item.get("text") or item.get("title") or ""
            digest = hashlib.sha256((canonical + "\n" + content).encode()).hexdigest()
            docs.append(
                Document(
                    id=f"doc-hn-{digest[:24]}",
                    workspace_id=source.workspace_id,
                    source_id=source.id,
                    source_type=SourceType.HACKER_NEWS,
                    source_url=source.source_url,
                    canonical_url=canonical,
                    retrieved_at=now,
                    published_at=published,
                    content_hash=digest,
                    title=item.get("title") or "Hacker News story",
                    content=content,
                    metadata={"connector": "hacker_news", "hn_id": item_id, "score": item.get("score", 0)},
                )
            )
        return docs
