from __future__ import annotations

from fastapi import APIRouter
from prometheus_client import CONTENT_TYPE_LATEST, generate_latest
from fastapi.responses import Response

from pulseforge.config import get_settings
from pulseforge.domain.auth import Principal, WorkspaceRole
from pulseforge.security.auth import issue_access_token

router = APIRouter(tags=["meta"])


@router.get("/capabilities")
def capabilities():
    settings = get_settings()
    return {
        "demo_mode": settings.demo_mode,
        "repository_mode": settings.repository_mode,
        "ai_provider": settings.ai_provider,
        "auth_mode": settings.auth_mode,
        "features": {
            "temporal_graph": True,
            "graph_diff": True,
            "contradictions": True,
            "watchlists": True,
            "alerts": True,
            "briefing_markdown": True,
            "briefing_html": True,
            "briefing_pdf": True,
            "sse_feed": True,
            "metrics": settings.enable_metrics,
        },
    }


@router.post("/auth/local-token")
def local_token():
    settings = get_settings()
    principal = Principal(
        user_id=settings.local_user_id,
        email=settings.local_user_email,
        workspace_roles={"ai-industry": WorkspaceRole.ADMIN},
    )
    return {"access_token": issue_access_token(principal, settings), "token_type": "bearer"}


@router.get("/metrics", include_in_schema=False)
def metrics():
    return Response(generate_latest(), media_type=CONTENT_TYPE_LATEST)
