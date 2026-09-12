from __future__ import annotations

from functools import lru_cache

from pulseforge.config import get_settings
from pulseforge.connectors.registry import ConnectorRegistry
from pulseforge.ingestion.orchestrator import IngestionOrchestrator


@lru_cache
def connector_registry() -> ConnectorRegistry:
    return ConnectorRegistry(get_settings())


@lru_cache
def ingestion_orchestrator() -> IngestionOrchestrator:
    return IngestionOrchestrator(connector_registry())
