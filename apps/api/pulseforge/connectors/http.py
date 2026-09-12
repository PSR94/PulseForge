from __future__ import annotations

import httpx

from pulseforge.config import Settings
from pulseforge.services.security import validate_public_url


async def fetch_bounded(
    url: str,
    settings: Settings,
    *,
    accept: str = "*/*",
) -> tuple[bytes, httpx.Response]:
    current = url
    async with httpx.AsyncClient(
        timeout=settings.ingestion_timeout_seconds,
        follow_redirects=False,
        headers={"User-Agent": "PulseForge/0.2 (+https://github.com/PSR94/PulseForge)", "Accept": accept},
    ) as client:
        for _ in range(settings.max_redirects + 1):
            validate_public_url(current, resolve_dns=True)
            async with client.stream("GET", current) as response:
                if response.status_code in {301, 302, 303, 307, 308}:
                    location = response.headers.get("location")
                    if not location:
                        raise ValueError("Redirect did not include Location")
                    current = str(response.url.join(location))
                    continue
                response.raise_for_status()
                content_type = response.headers.get("content-type", "").split(";")[0].strip().lower()
                if content_type and content_type not in settings.content_types:
                    raise ValueError(f"Unsupported content type: {content_type}")
                chunks: list[bytes] = []
                total = 0
                async for chunk in response.aiter_bytes():
                    total += len(chunk)
                    if total > settings.max_download_bytes:
                        raise ValueError("Download exceeded configured byte limit")
                    chunks.append(chunk)
                return b"".join(chunks), response
    raise ValueError("Too many redirects")
