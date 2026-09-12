from __future__ import annotations

from datetime import UTC, datetime, timedelta
from typing import Annotated

import jwt
from fastapi import Depends, Header, HTTPException

from pulseforge.config import Settings, get_settings
from pulseforge.domain.auth import Principal, WorkspaceRole


def issue_access_token(principal: Principal, settings: Settings | None = None) -> str:
    settings = settings or get_settings()
    now = datetime.now(UTC)
    payload = {
        "sub": principal.user_id,
        "email": principal.email,
        "roles": {key: value.value for key, value in principal.workspace_roles.items()},
        "iat": int(now.timestamp()),
        "exp": int((now + timedelta(minutes=settings.access_token_minutes)).timestamp()),
    }
    return jwt.encode(payload, settings.jwt_secret, algorithm=settings.jwt_algorithm)


def _local_principal(settings: Settings) -> Principal:
    return Principal(
        user_id=settings.local_user_id,
        email=settings.local_user_email,
        workspace_roles={"ai-industry": WorkspaceRole.ADMIN},
    )


def get_principal(
    authorization: Annotated[str | None, Header()] = None,
    settings: Settings = Depends(get_settings),
) -> Principal:
    if settings.auth_mode == "local":
        return _local_principal(settings)
    if not authorization or not authorization.lower().startswith("bearer "):
        raise HTTPException(status_code=401, detail="Bearer token required")
    token = authorization.split(" ", 1)[1]
    try:
        payload = jwt.decode(token, settings.jwt_secret, algorithms=[settings.jwt_algorithm])
    except jwt.PyJWTError as exc:
        raise HTTPException(status_code=401, detail="Invalid access token") from exc
    roles = {
        workspace_id: WorkspaceRole(role)
        for workspace_id, role in (payload.get("roles") or {}).items()
    }
    return Principal(
        user_id=str(payload["sub"]),
        email=str(payload.get("email") or ""),
        workspace_roles=roles,
    )


PrincipalDep = Annotated[Principal, Depends(get_principal)]


def require_workspace(principal: Principal, workspace_id: str, minimum: WorkspaceRole) -> None:
    try:
        principal.require_workspace(workspace_id, minimum)
    except PermissionError as exc:
        raise HTTPException(status_code=403, detail=str(exc)) from exc
