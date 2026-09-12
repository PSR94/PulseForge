from datetime import UTC, datetime

from pulseforge.domain.models import Document, ProcessingStage, SourceType
from pulseforge.ingestion.dedupe import deduplicate
from pulseforge.ingestion.enrichment import deterministic_enrich
from pulseforge.ingestion.normalizer import normalize_document


def document(doc_id="d1"):
    return Document(
        id=doc_id,
        workspace_id="w",
        source_id="s",
        source_type=SourceType.WEB,
        source_url="https://example.com",
        canonical_url="https://example.com/a",
        retrieved_at=datetime.now(UTC),
        published_at=datetime.now(UTC),
        content_hash="same",
        title="  NVIDIA   announces   accelerator ",
        content=" NVIDIA   Systems   expands infrastructure. ",
    )


def test_deterministic_early_pipeline_advances_and_deduplicates():
    normalized = [normalize_document(document("a")), normalize_document(document("b"))]
    assert all(item.stage == ProcessingStage.NORMALIZED for item in normalized)
    kept, duplicates = deduplicate(normalized)
    assert len(kept) == 1
    assert duplicates == ["b"]
    enriched = deterministic_enrich(kept[0])
    assert enriched.stage == ProcessingStage.ENRICHED
    assert "NVIDIA" in enriched.metadata["entity_candidates"]
