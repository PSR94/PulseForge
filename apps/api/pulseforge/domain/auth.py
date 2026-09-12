from __future__ import annotations

from datetime import UTC, datetime
from enum import StrEnum

from pydantic import BaseModel, Field


class WorkspaceRole(StrEnum):
    VIEWER = "viewer"
    ANALYST = "analyst"
    ADMIN = "admin"


class Principal(BaseModel):
    user_id: str
    email: str
    workspace_roles: dict[str, WorkspaceRole] = Field(default_factory=dict)
    authenticated_at: datetime = Field(default_factory=lambda: datetime.now(UTC))

    def require_workspace(self, workspace_id: str, minimum: WorkspaceRole = WorkspaceRole.VIEWER) -> None:
        role = self.workspace_roles.get(workspace_id)
        if role is None:
            raise PermissionError(f"No access to workspace {workspace_id}")
        order = {WorkspaceRole.VIEWER: 0, WorkspaceRole.ANALYST: 1, WorkspaceRole.ADMIN: 2}
        if order[role] < order[minimum]:
            raise PermissionError(f"{minimum.value} access required")
