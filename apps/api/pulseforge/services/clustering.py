from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime


@dataclass(frozen=True)
class ClusterFeatures:
    shared_entity_ratio: float
    semantic_similarity: float
    topic_similarity: float
    location_match: float
    event_type_match: float
    hours_apart: float


@dataclass(frozen=True)
class ClusterDecision:
    grouped: bool
    score: float
    reasons: tuple[str, ...]


def decide_cluster(features: ClusterFeatures, threshold: float = 0.68) -> ClusterDecision:
    temporal = max(0.0, 1.0 - min(features.hours_apart, 72.0) / 72.0)
    weighted = (
        0.28 * features.shared_entity_ratio
        + 0.30 * features.semantic_similarity
        + 0.12 * features.topic_similarity
        + 0.08 * features.location_match
        + 0.12 * features.event_type_match
        + 0.10 * temporal
    )
    reasons: list[str] = []
    if features.shared_entity_ratio >= 0.5:
        reasons.append(f"shared entities {features.shared_entity_ratio:.0%}")
    if features.semantic_similarity >= 0.75:
        reasons.append(f"semantic similarity {features.semantic_similarity:.2f}")
    if temporal >= 0.8:
        reasons.append(f"temporal proximity {features.hours_apart:.1f}h")
    if features.event_type_match >= 1:
        reasons.append("same event type")
    return ClusterDecision(grouped=weighted >= threshold, score=round(weighted, 3), reasons=tuple(reasons))


def hours_between(a: datetime, b: datetime) -> float:
    return abs((a - b).total_seconds()) / 3600
