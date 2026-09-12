from __future__ import annotations

import hashlib
from collections import defaultdict

from pulseforge.domain.models import Claim, Contradiction


def detect_contradictions(claims: list[Claim]) -> list[Contradiction]:
    """Find conflicting values for the same subject/property.

    This is deliberately deterministic: the model may normalize a property upstream, but
    whether distinct stored values conflict is decided by persisted system state.
    """
    grouped: dict[tuple[str, str], list[Claim]] = defaultdict(list)
    for claim in claims:
        grouped[(claim.subject_entity_id, claim.normalized_property)].append(claim)

    contradictions: list[Contradiction] = []
    for (subject_id, prop), group in grouped.items():
        values = {claim.object_value.strip().casefold() for claim in group}
        if len(values) < 2:
            continue
        ordered = sorted(group, key=lambda claim: claim.observed_at)
        fingerprint = hashlib.sha256(
            (subject_id + "|" + prop + "|" + "|".join(sorted(values))).encode()
        ).hexdigest()[:20]
        contradictions.append(
            Contradiction(
                id=f"ctr-{fingerprint}",
                workspace_id=ordered[-1].workspace_id,
                subject_entity_id=subject_id,
                normalized_property=prop,
                claim_ids=[claim.id for claim in ordered],
                explanation=(
                    f"Stored claims disagree on {prop}; PulseForge preserves all values "
                    "and does not silently choose one."
                ),
            )
        )
    return contradictions
