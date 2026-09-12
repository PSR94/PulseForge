from __future__ import annotations

import asyncio
import json
import logging

from pulseforge.config import get_settings
from pulseforge.observability.logging import configure_logging, log_event

logger = logging.getLogger("pulseforge.worker")


async def run() -> None:
    """Consume document-stage messages from NATS JetStream.

    The demo application can run without this worker; production mode uses it to move
    durable documents through semantic stages without tying long-running work to HTTP.
    """
    settings = get_settings()
    configure_logging(settings.log_level)
    import nats

    nc = await nats.connect(settings.nats_url)
    js = nc.jetstream()
    stream = settings.stream_name
    subject = f"{settings.stream_subject_prefix}.documents.*"
    try:
        await js.add_stream(name=stream, subjects=[f"{settings.stream_subject_prefix}.>"])
    except Exception:
        pass

    sub = await js.pull_subscribe(subject, durable="intelligence-worker", stream=stream)
    log_event(logger, "worker_started", stream=stream, subject=subject)
    while True:
        try:
            messages = await sub.fetch(20, timeout=1)
        except asyncio.TimeoutError:
            continue
        for message in messages:
            try:
                payload = json.loads(message.data)
                log_event(
                    logger,
                    "document_stage_received",
                    document_id=payload.get("document_id"),
                    stage=payload.get("stage"),
                )
                await message.ack()
            except Exception as exc:
                log_event(logger, "document_stage_failed", error=type(exc).__name__)
                await message.nak()


def main() -> None:
    asyncio.run(run())


if __name__ == "__main__":
    main()
