from __future__ import annotations

import asyncio
import json

from fastapi import APIRouter, Query
from fastapi.responses import StreamingResponse

from pulseforge.api.deps import Repo
from pulseforge.observability.metrics import ACTIVE_SSE_CLIENTS

router = APIRouter(tags=["feed"])


@router.get("/feed")
def feed(repo: Repo, limit: int = Query(25, ge=1, le=200)):
    return repo.list_events()[:limit]


@router.get("/feed/stream")
async def feed_stream(repo: Repo):
    async def generate():
        ACTIVE_SSE_CLIENTS.inc()
        try:
            for event in repo.list_events():
                payload = json.dumps(event.model_dump(mode="json"))
                yield f"event: intelligence\ndata: {payload}\n\n"
                await asyncio.sleep(0.05)
            yield 'event: heartbeat\ndata: {"status":"caught_up"}\n\n'
        finally:
            ACTIVE_SSE_CLIENTS.dec()

    return StreamingResponse(
        generate(),
        media_type="text/event-stream",
        headers={"Cache-Control": "no-cache", "X-Accel-Buffering": "no"},
    )
