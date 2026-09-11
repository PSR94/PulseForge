from __future__ import annotations

import json
import logging
import time
import uuid

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from pulseforge import __version__
from pulseforge.api.routes import router

logger = logging.getLogger("pulseforge")
logging.basicConfig(level=logging.INFO, format="%(message)s")

app = FastAPI(
    title="PulseForge API",
    version=__version__,
    description="Evidence-linked temporal event intelligence API",
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],
    allow_credentials=False,
    allow_methods=["GET", "POST", "OPTIONS"],
    allow_headers=["Content-Type", "Authorization", "X-Request-ID"],
)
app.include_router(router)


def log_json(event: str, **fields: object) -> None:
    logger.info(json.dumps({"event": event, **fields}, default=str, separators=(",", ":")))


@app.middleware("http")
async def request_context(request: Request, call_next):
    request_id = request.headers.get("x-request-id") or str(uuid.uuid4())
    started = time.perf_counter()
    try:
        response = await call_next(request)
    except Exception as exc:
        log_json("request_failed", request_id=request_id, path=request.url.path, error=type(exc).__name__)
        raise
    response.headers["X-Request-ID"] = request_id
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["Referrer-Policy"] = "no-referrer"
    log_json(
        "request_complete",
        request_id=request_id,
        method=request.method,
        path=request.url.path,
        status=response.status_code,
        duration_ms=round((time.perf_counter() - started) * 1000, 2),
    )
    return response


@app.get("/health")
def health():
    return {"status": "ok", "service": "pulseforge-api", "version": __version__}


@app.exception_handler(ValueError)
async def value_error_handler(_: Request, exc: ValueError):
    return JSONResponse(status_code=422, content={"detail": str(exc)})
