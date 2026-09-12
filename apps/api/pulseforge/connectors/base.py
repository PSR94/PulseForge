from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass
from datetime import datetime
from typing import Any

from pulseforge.domain.models import Document, Source, SourceType


@dataclass(slots=True)
class ConnectorCapabilities:
    supports_polling: bool = True
    supports_backfill: bool = False
    supports_webhook: bool = False
    content_types: tuple[str, ...] = ()


class Connector(ABC):
    source_type: SourceType
    capabilities = ConnectorCapabilities()

    @abstractmethod
    async def fetch(self, source: Source, *, since: datetime | None = None) -> list[Document]:
        raise NotImplementedError


class ConnectorError(RuntimeError):
    def __init__(self, message: str, *, retryable: bool = True, details: dict[str, Any] | None = None):
        super().__init__(message)
        self.retryable = retryable
        self.details = details or {}
