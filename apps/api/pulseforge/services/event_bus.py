from __future__ import annotations

import json
from collections import defaultdict
from collections.abc import AsyncIterator
from typing import Any, Protocol


class EventBus(Protocol):
    async def publish(self, subject: str, payload: dict[str, Any]) -> None: ...
    async def subscribe(self, subject: str) -> AsyncIterator[dict[str, Any]]: ...


class InMemoryEventBus:
    """Local adapter used by tests and minimal development environments."""

    def __init__(self) -> None:
        self.messages: dict[str, list[dict[str, Any]]] = defaultdict(list)

    async def publish(self, subject: str, payload: dict[str, Any]) -> None:
        self.messages[subject].append(payload)

    async def subscribe(self, subject: str) -> AsyncIterator[dict[str, Any]]:
        for payload in self.messages[subject]:
            yield payload


class NatsJetStreamEventBus:
    """NATS JetStream adapter. Import is deferred so mock mode has no runtime dependency."""

    def __init__(self, url: str, stream: str = "PULSEFORGE") -> None:
        self.url = url
        self.stream = stream
        self._connection = None
        self._js = None

    async def connect(self) -> None:
        import nats

        self._connection = await nats.connect(self.url)
        self._js = self._connection.jetstream()
        try:
            await self._js.add_stream(name=self.stream, subjects=["pulseforge.>"])
        except Exception as exc:  # stream may already exist
            if "stream name already in use" not in str(exc).lower():
                raise

    async def publish(self, subject: str, payload: dict[str, Any]) -> None:
        if self._js is None:
            await self.connect()
        await self._js.publish(subject, json.dumps(payload).encode("utf-8"))
