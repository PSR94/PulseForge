from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime

from pulseforge.connectors.registry import ConnectorRegistry
from pulseforge.domain.models import Document, Source
from pulseforge.ingestion.dedupe import deduplicate
from pulseforge.ingestion.enrichment import deterministic_enrich
from pulseforge.ingestion.normalizer import normalize_document


@dataclass(slots=True)
class IngestionReport:
    source_id: str
    received: int = 0
    persisted: int = 0
    duplicates: int = 0
    failed_document_ids: list[str] = field(default_factory=list)
    stage_counts: dict[str, int] = field(default_factory=dict)


class IngestionOrchestrator:
    """Runs connector output through deterministic, persisted early pipeline stages.

    Later semantic stages are intentionally delegated to the intelligence worker so a
    transient LLM/provider failure never loses the normalized source document.
    """

    def __init__(self, registry: ConnectorRegistry):
        self.registry = registry

    async def ingest(self, source: Source, *, since: datetime | None = None) -> tuple[list[Document], IngestionReport]:
        connector = self.registry.get(source.source_type)
        raw = await connector.fetch(source, since=since)
        report = IngestionReport(source_id=source.id, received=len(raw))
        normalized = [normalize_document(document) for document in raw]
        deduped, duplicate_ids = deduplicate(normalized)
        report.duplicates = len(duplicate_ids)
        enriched = [deterministic_enrich(document) for document in deduped]
        report.persisted = len(enriched)
        for document in enriched:
            report.stage_counts[document.stage.value] = report.stage_counts.get(document.stage.value, 0) + 1
        return enriched, report
