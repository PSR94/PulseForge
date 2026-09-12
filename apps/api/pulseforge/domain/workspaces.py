from __future__ import annotations

from pydantic import BaseModel, Field


class WorkspaceCreate(BaseModel):
    name: str = Field(min_length=2, max_length=200)
    description: str = Field(default="", max_length=2000)
    workspace_id: str | None = Field(default=None, pattern=r"^[a-z0-9][a-z0-9-]{1,62}$")
