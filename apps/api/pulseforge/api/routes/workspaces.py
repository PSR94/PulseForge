from __future__ import annotations

from fastapi import APIRouter, HTTPException, Response

from pulseforge.domain.workspaces import WorkspaceCreate
from pulseforge.services.workspace_registry import get_workspace_registry

router = APIRouter(tags=["workspaces"])


@router.get("/workspaces")
def list_workspaces():
    return get_workspace_registry().list()


@router.post("/workspaces", status_code=201)
def create_workspace(payload: WorkspaceCreate, response: Response):
    repo = get_workspace_registry().create(
        name=payload.name,
        description=payload.description,
        workspace_id=payload.workspace_id,
    )
    response.headers["X-Workspace-ID"] = repo.workspace.id
    return repo.workspace


@router.get("/workspaces/{workspace_id}")
def get_workspace(workspace_id: str):
    repo = get_workspace_registry().get(workspace_id)
    if repo is None:
        raise HTTPException(status_code=404, detail="Workspace not found")
    return repo.workspace
