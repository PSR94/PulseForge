from __future__ import annotations

import hashlib
import re
from datetime import UTC, datetime

from pulseforge.config import Settings
from pulseforge.connectors.base import Connector
from pulseforge.connectors.http import fetch_bounded
from pulseforge.domain.models import Document, Source, SourceType

_REPO = re.compile(r"github\.com/([^/]+)/([^/#?]+)")


class GitHubConnector(Connector):
    source_type = SourceType.GITHUB

    def __init__(self, settings: Settings):
        self.settings = settings

    async def fetch(self, source: Source, *, since: datetime | None = None) -> list[Document]:
        match = _REPO.search(str(source.source_url))
        if not match:
            raise ValueError("GitHub source URL must identify a repository")
        owner, repo = match.group(1), match.group(2).removesuffix(".git")
        api_url = f"https://api.github.com/repos/{owner}/{repo}/releases?per_page=50"
        body, _ = await fetch_bounded(api_url, self.settings, accept="application/vnd.github+json")
        import json
        releases = json.loads(body)
        docs: list[Document] = []
        now = datetime.now(UTC)
        for release in releases:
            published_raw = release.get("published_at") or release.get("created_at")
            published = datetime.fromisoformat(published_raw.replace("Z", "+00:00"))
            if since and published < since:
                continue
            canonical = release.get("html_url") or str(source.source_url)
            content = release.get("body") or ""
            title = release.get("name") or release.get("tag_name") or "GitHub release"
            digest = hashlib.sha256((canonical + "\n" + content).encode()).hexdigest()
            docs.append(
                Document(
                    id=f"doc-gh-{digest[:24]}",
                    workspace_id=source.workspace_id,
                    source_id=source.id,
                    source_type=SourceType.GITHUB,
                    source_url=source.source_url,
                    canonical_url=canonical,
                    retrieved_at=now,
                    published_at=published,
                    content_hash=digest,
                    title=title,
                    content=content,
                    metadata={
                        "connector": "github",
                        "tag": release.get("tag_name"),
                        "prerelease": bool(release.get("prerelease")),
                    },
                )
            )
        return docs
