from __future__ import annotations

import logging
import time
import uuid
from contextlib import asynccontextmanager

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from pulseforge import __version__
from pulseforge.api.router import router
from pulseforge.config import get_settings
from pulseforge.observability.logging import configure_logging, log_event
from pulseforge.observability.tracing import configure_tracing
from pulseforge.security.rate_limit import enforce_rate_limit

settings = get_settings()
configure_logging(settings.log_level)
configure_tracing(settings)
logger = logging.getLogger("pulseforge")


@asynccontextmanager
async def lifespan(app: FastAPI):
    log_event(
        logger,
        "service_started",
        version=__version__,
        demo_mode=settings.demo_mode,
        repository_mode=settings.repository_mode,
        ai_provider=settings.ai_provider,
    )
    yield
    log_event(logger, "service_stopped")


app = FastAPI(
    title="PulseForge API",
    version=__version__,
    description="Evidence-linked temporal event intelligence API",
    lifespan=lifespan,
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origin_list,
    allow_credentials=False,
    allow_methods=["GET", "POST", "PUT", "PATCH", "DELETE", "OPTIONS"],
    allow_headers=["Content-Type", "Authorization", "X-Request-ID"],
)
app.include_router(router)


@app.middleware("http")
async def request_context(request: Request, call_next):
    request_id = request.headers.get("x-request-id") or str(uuid.uuid4())
    started = time.perf_counter()
    if not request.url.path.endswith("/health") and not request.url.path.endswith("/metrics"):
        await enforce_rate_limit(request)
    try:
        response = await call_next(request)
    except Exception as exc:
        log_event(
            logger,
            "request_failed",
            request_id=request_id,
            path=request.url.path,
            error=type(exc).__name__,
        )
        raise
    response.headers["X-Request-ID"] = request_id
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["Referrer-Policy"] = "no-referrer"
    response.headers["Permissions-Policy"] = "geolocation=(), camera=(), microphone=()"
    response.headers["Content-Security-Policy"] = "default-src 'self'; frame-ancestors 'none'"
    log_event(
        logger,
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
    return {
        "status": "ok",
        "service": "pulseforge-api",
        "version": __version__,
        "demo_mode": settings.demo_mode,
    }


@app.get("/ready")
def ready():
    return {
        "status": "ready",
        "repository_mode": settings.repository_mode,
        "ai_provider": settings.ai_provider,
    }


@app.exception_handler(ValueError)
async def value_error_handler(_: Request, exc: ValueError):
    return JSONResponse(status_code=422, content={"detail": str(exc)})
