from __future__ import annotations

import hashlib
import xml.etree.ElementTree as ET
from datetime import UTC, datetime
from email.utils import parsedate_to_datetime
from typing import Iterable

import httpx

from pulseforge.config import Settings
from pulseforge.domain.models import Document, ProcessingStage, Source, SourceType
from pulseforge.services.security import validate_public_url


class RssConnector:
    """Bounded RSS/Atom connector with URL revalidation on redirects."""

    def __init__(self, settings: Settings):
        self.settings = settings

    async def fetch(self, source: Source) -> list[Document]:
        validate_public_url(str(source.source_url))
        async with httpx.AsyncClient(follow_redirects=False, timeout=15) as client:
            response = await client.get(str(source.source_url), headers={"User-Agent": "PulseForge/0.1"})
            redirects = 0
            while response.is_redirect:
                redirects += 1
                if redirects > 5:
                    raise ValueError("Too many redirects")
                target = str(response.next_request.url)
                validate_public_url(target)
                response = await client.send(response.next_request, follow_redirects=False)
            response.raise_for_status()

        content_type = response.headers.get("content-type", "").split(";", 1)[0].strip().lower()
        if content_type and content_type not in self.settings.content_types:
            raise ValueError(f"Unsupported content type: {content_type}")
        if len(response.content) > self.settings.max_download_bytes:
            raise ValueError("Feed exceeded configured download limit")
        return list(self.parse(source, response.content))

    @staticmethod
    def _text(element: ET.Element, names: tuple[str, ...]) -> str | None:
        for child in list(element):
            local_name = child.tag.rsplit("}", 1)[-1].lower()
            if local_name in names and child.text:
                return child.text.strip()
        return None

    @staticmethod
    def _link(element: ET.Element) -> str | None:
        for child in list(element):
            if child.tag.rsplit("}", 1)[-1].lower() != "link":
                continue
            href = child.attrib.get("href")
            if href:
                return href.strip()
            if child.text:
                return child.text.strip()
        return None

    @staticmethod
    def _published(raw: str | None, fallback: datetime) -> datetime:
        if not raw:
            return fallback
        try:
            return parsedate_to_datetime(raw).astimezone(UTC)
        except (TypeError, ValueError):
            try:
                return datetime.fromisoformat(raw.replace("Z", "+00:00")).astimezone(UTC)
            except ValueError:
                return fallback

    def parse(self, source: Source, payload: bytes) -> Iterable[Document]:
        try:
            root = ET.fromstring(payload)
        except ET.ParseError as exc:
            raise ValueError("Feed is not valid XML") from exc
        retrieved = datetime.now(UTC)
        entries = [
            element
            for element in root.iter()
            if element.tag.rsplit("}", 1)[-1].lower() in {"item", "entry"}
        ]
        for index, entry in enumerate(entries):
            link = self._link(entry) or str(source.canonical_url)
            title = self._text(entry, ("title",)) or "Untitled"
            content = self._text(entry, ("summary", "description", "content")) or title
            raw_date = self._text(entry, ("published", "updated", "pubdate"))
            published = self._published(raw_date, retrieved)
            canonical = link if link.startswith(("http://", "https://")) else str(source.canonical_url)
            digest = hashlib.sha256(content.encode("utf-8")).hexdigest()
            yield Document(
                id=f"{source.id}:{digest[:16]}:{index}",
                workspace_id=source.workspace_id,
                source_id=source.id,
                source_type=SourceType.RSS,
                source_url=source.source_url,
                canonical_url=canonical,
                retrieved_at=retrieved,
                published_at=published,
                content_hash=digest,
                title=title,
                content=content,
                metadata={"connector": "rss"},
                stage=ProcessingStage.INGESTED,
            )
