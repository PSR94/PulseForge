from __future__ import annotations

from prometheus_client import Counter, Gauge, Histogram

DOCUMENTS_PROCESSED = Counter(
    "pulseforge_documents_processed_total", "Documents processed", ["stage", "source_type"]
)
PROCESSING_FAILURES = Counter(
    "pulseforge_processing_failures_total", "Processing failures", ["stage"]
)
LLM_LATENCY = Histogram(
    "pulseforge_llm_latency_seconds", "LLM request latency", ["provider", "operation"]
)
LLM_COST_USD = Counter(
    "pulseforge_llm_cost_usd_total", "Estimated LLM cost in USD", ["provider", "model"]
)
EVENT_CLUSTERS = Counter(
    "pulseforge_event_clusters_created_total", "Normalized event clusters created", ["event_type"]
)
ENTITY_RESOLUTION_CONFIDENCE = Histogram(
    "pulseforge_entity_resolution_confidence", "Entity resolution confidence"
)
SIGNALS_GENERATED = Counter(
    "pulseforge_signals_generated_total", "Signals generated", ["signal_type", "severity"]
)
INGESTION_DELAY = Histogram(
    "pulseforge_source_ingestion_delay_seconds", "Source publication to ingestion delay", ["source_type"]
)
ACTIVE_SSE_CLIENTS = Gauge("pulseforge_active_sse_clients", "Connected live-feed clients")
