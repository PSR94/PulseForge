from __future__ import annotations

from fastapi import APIRouter

from pulseforge.api.routes import (
    analyst,
    briefings,
    claims,
    entities,
    events,
    feed,
    graph,
    meta,
    search,
    signals,
    sources,
    watchlists,
    workspaces,
    uploads,
)

router = APIRouter(prefix="/api/v1")

for child in (
    workspaces.router,
    feed.router,
    events.router,
    entities.router,
    graph.router,
    signals.router,
    claims.router,
    sources.router,
    search.router,
    analyst.router,
    briefings.router,
    watchlists.router,
    meta.router,
    uploads.router,
):
    router.include_router(child)
