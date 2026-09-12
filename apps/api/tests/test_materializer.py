from datetime import UTC, datetime

from pulseforge.domain.models import Document, SourceType
from pulseforge.services.demo_repository import DemoRepository
from pulseforge.services.materializer import LiveMaterializer


def live_document(doc_id: str, title: str, source_id: str) -> Document:
    now = datetime(2026, 9, 12, 10, 0, tzinfo=UTC)
    return Document(
        id=doc_id,
        workspace_id="ai-industry",
        source_id=source_id,
        source_type=SourceType.RSS,
        source_url="https://example.com/feed",
        canonical_url=f"https://example.com/{doc_id}",
        retrieved_at=now,
        published_at=now,
        content_hash=doc_id * 8,
        title=title,
        content=f"{title}. NVIDIA Systems and Nebula Cloud announced details.",
        metadata={"entity_candidates": ["NVIDIA", "Nebula Cloud"], "source_name": source_id},
    )


def test_live_documents_converge_into_normalized_event_and_graph():
    repo = DemoRepository()
    before_events = len(repo.events)
    before_relationships = len(repo.relationships)
    docs = [
        live_document("a1", "NVIDIA and Nebula Cloud announce inference expansion", "Source A"),
        live_document("b2", "NVIDIA and Nebula Cloud announce inference expansion", "Source B"),
    ]
    materialized = LiveMaterializer().materialize(docs, repo)
    assert len(repo.events) >= before_events
    event = materialized[-1]
    assert event.source_count == 2
    assert len(event.evidence) == 2
    assert len(repo.relationships) >= before_relationships + 1
    assert any(rel.relationship_type == "CO_OCCURS_WITH" for rel in repo.relationships)
