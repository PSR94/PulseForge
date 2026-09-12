from __future__ import annotations

import re
from datetime import UTC, datetime
from functools import lru_cache

from pulseforge.domain.models import Workspace
from pulseforge.services.demo_repository import DemoRepository, get_demo_repository


def _slug(name: str) -> str:
    value = re.sub(r"[^a-z0-9]+", "-", name.casefold()).strip("-")
    return value[:48] or "workspace"


class WorkspaceRegistry:
    """Isolated in-memory workspace states for zero-config mode.

    Database mode uses the same workspace identifier at the persistence boundary; this registry keeps
    local development useful without requiring Postgres.
    """

    def __init__(self) -> None:
        self._repos: dict[str, DemoRepository] = {"ai-industry": get_demo_repository()}

    def list(self) -> list[Workspace]:
        return [repo.workspace for repo in self._repos.values()]

    def get(self, workspace_id: str) -> DemoRepository | None:
        return self._repos.get(workspace_id)

    def create(self, *, name: str, description: str, workspace_id: str | None = None) -> DemoRepository:
        base = workspace_id or _slug(name)
        candidate = base
        suffix = 2
        while candidate in self._repos:
            candidate = f"{base[:54]}-{suffix}"
            suffix += 1
        repo = DemoRepository()
        repo.workspace_id = candidate
        now = datetime.now(UTC)
        repo.workspace = Workspace(
            id=candidate,
            name=name,
            description=description,
            updated_at=now,
            last_visited_at=now,
        )
        repo.sources = []
        repo.entities = []
        repo.events = []
        repo.relationships = []
        repo.claims = []
        repo.contradictions = []
        repo.signals = []
        self._repos[candidate] = repo
        return repo


@lru_cache
def get_workspace_registry() -> WorkspaceRegistry:
    return WorkspaceRegistry()
