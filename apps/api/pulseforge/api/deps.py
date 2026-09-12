from __future__ import annotations

from typing import Annotated

from fastapi import Depends, Header, HTTPException

from pulseforge.services.demo_repository import DemoRepository
from pulseforge.services.workspace_registry import get_workspace_registry


def get_repository(
    x_workspace_id: Annotated[str | None, Header()] = None,
) -> DemoRepository:
    workspace_id = x_workspace_id or "ai-industry"
    repo = get_workspace_registry().get(workspace_id)
    if repo is None:
        raise HTTPException(status_code=404, detail="Workspace not found")
    return repo


Repo = Annotated[DemoRepository, Depends(get_repository)]
