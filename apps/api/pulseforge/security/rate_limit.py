from __future__ import annotations

import time
from collections import defaultdict, deque
from threading import Lock

from fastapi import HTTPException, Request

from pulseforge.config import get_settings


class InMemoryRateLimiter:
    """Small local-development limiter; Redis-backed deployments can replace this adapter."""

    def __init__(self) -> None:
        self._events: dict[str, deque[float]] = defaultdict(deque)
        self._lock = Lock()

    def check(self, key: str, limit: int, window_seconds: int = 60) -> None:
        now = time.monotonic()
        cutoff = now - window_seconds
        with self._lock:
            bucket = self._events[key]
            while bucket and bucket[0] < cutoff:
                bucket.popleft()
            if len(bucket) >= limit:
                raise HTTPException(status_code=429, detail="Rate limit exceeded")
            bucket.append(now)


limiter = InMemoryRateLimiter()


async def enforce_rate_limit(request: Request) -> None:
    settings = get_settings()
    client = request.client.host if request.client else "unknown"
    limiter.check(client, settings.rate_limit_per_minute)
