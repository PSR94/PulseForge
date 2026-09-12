from datetime import UTC, datetime

from pulseforge.domain.models import Claim, ClaimKind
from pulseforge.services.contradictions import detect_contradictions


def make_claim(claim_id: str, value: str, minute: int) -> Claim:
    return Claim(
        id=claim_id,
        workspace_id="w",
        subject_entity_id="entity",
        predicate="launches",
        object_value=value,
        normalized_property="launch_date",
        kind=ClaimKind.FACTUAL,
        extraction_confidence=0.9,
        observed_at=datetime(2026, 9, 12, 10, minute, tzinfo=UTC),
        evidence=[],
    )


def test_conflicting_normalized_values_create_contradiction():
    items = detect_contradictions([make_claim("a", "October 2026", 0), make_claim("b", "January 2027", 2)])
    assert len(items) == 1
    assert items[0].claim_ids == ["a", "b"]
    assert items[0].status == "unresolved"


def test_matching_values_do_not_create_contradiction():
    assert detect_contradictions([make_claim("a", "October 2026", 0), make_claim("b", " october 2026 ", 1)]) == []
