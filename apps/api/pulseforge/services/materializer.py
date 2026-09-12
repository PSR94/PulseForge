from __future__ import annotations

import hashlib
import re
from collections import Counter
from datetime import timedelta
from itertools import combinations

from pulseforge.domain.models import (
    Document,
    Entity,
    EntityType,
    Event,
    EvidenceRef,
    Signal,
    SignalType,
    TemporalRelationship,
)
from pulseforge.services.demo_repository import DemoRepository

_WORD = re.compile(r"[a-z0-9]{3,}")
_STOP = {"the", "and", "for", "with", "from", "into", "that", "this", "will", "new", "its"}


def _tokens(value: str) -> set[str]:
    return {token for token in _WORD.findall(value.casefold()) if token not in _STOP}


def _jaccard(a: str, b: str) -> float:
    left, right = _tokens(a), _tokens(b)
    if not left or not right:
        return 0.0
    return len(left & right) / len(left | right)


def _event_type(title: str) -> str:
    lowered = title.casefold()
    rules = [
        ("acquisition", ("acquires", "acquisition", "buys", "merger")),
        ("partnership", ("partners", "partnership", "collaboration", "alliance")),
        ("release", ("releases", "launches", "announces", "ships", "introduces")),
        ("security_incident", ("breach", "vulnerability", "exploit", "incident")),
        ("research", ("paper", "research", "benchmark", "study")),
        ("financial", ("earnings", "guidance", "revenue", "forecast")),
    ]
    for event_type, terms in rules:
        if any(term in lowered for term in terms):
            return event_type
    return "development"


def _entity_type(name: str) -> EntityType:
    if any(word in name.casefold() for word in ("runtime", "model", "gpu", "platform")):
        return EntityType.TECHNOLOGY
    return EntityType.ORGANIZATION


class LiveMaterializer:
    """Materialize real connector documents into inspectable intelligence.

    This path is intentionally deterministic in mock/local mode. It does not claim that
    co-mentions establish a factual relationship; those edges are explicitly typed
    CO_OCCURS_WITH and remain observational.
    """

    def materialize(self, documents: list[Document], repo: DemoRepository) -> list[Event]:
        materialized: list[Event] = []
        for document in sorted(documents, key=lambda item: item.published_at):
            entity_ids = self._upsert_entities(document, repo)
            evidence = self._evidence(document)
            existing = self._best_event(document, entity_ids, repo)
            if existing is not None:
                existing.source_count += 1
                existing.latest_confirmation = max(existing.latest_confirmation, document.retrieved_at)
                existing.confidence = min(0.98, 0.55 + 0.08 * existing.source_count)
                existing.evidence.append(evidence)
                existing.entity_ids = sorted(set(existing.entity_ids) | set(entity_ids))
                existing.cluster_reasons = sorted(
                    set(existing.cluster_reasons)
                    | {"title/token similarity", "shared extracted entities", "temporal proximity"}
                )
                materialized.append(existing)
                event = existing
            else:
                digest = hashlib.sha256(
                    (document.workspace_id + "|" + document.title.casefold()).encode()
                ).hexdigest()[:20]
                event = Event(
                    id=f"evt-live-{digest}",
                    workspace_id=document.workspace_id,
                    title=document.title,
                    event_type=_event_type(document.title),
                    first_observed=document.published_at,
                    latest_confirmation=document.retrieved_at,
                    entity_ids=entity_ids,
                    confidence=0.63,
                    novelty_score=0.88,
                    impact_score=min(0.9, 0.42 + 0.07 * len(entity_ids)),
                    source_count=1,
                    related_event_ids=[],
                    claim_ids=[],
                    evidence=[evidence],
                    explanation=(
                        "Live connector materialization: a source document introduced a "
                        "new event candidate. Confidence increases only with corroborating documents."
                    ),
                    cluster_reasons=["new normalized event candidate"],
                    topics=sorted(_tokens(document.title))[:6],
                )
                repo.events.append(event)
                materialized.append(event)
            self._update_observational_graph(event, evidence, repo)

        self._update_related_events(repo)
        self._refresh_velocity_signals(repo)
        return list({event.id: event for event in materialized}.values())

    def _upsert_entities(self, document: Document, repo: DemoRepository) -> list[str]:
        entity_ids: list[str] = []
        candidates = list(document.metadata.get("entity_candidates") or [])
        for name in candidates[:20]:
            normalized = str(name).strip()
            if not normalized:
                continue
            existing = next(
                (
                    entity
                    for entity in repo.entities
                    if normalized.casefold() == entity.name.casefold()
                    or normalized.casefold() in {alias.casefold() for alias in entity.aliases}
                ),
                None,
            )
            if existing:
                existing.last_seen = max(existing.last_seen, document.published_at)
                entity_ids.append(existing.id)
                continue
            digest = hashlib.sha256(normalized.casefold().encode()).hexdigest()[:18]
            entity = Entity(
                id=f"ent-live-{digest}",
                workspace_id=document.workspace_id,
                name=normalized,
                entity_type=_entity_type(normalized),
                aliases=[],
                description="Discovered through live ingestion; description awaits corroborated enrichment.",
                external_ids={},
                importance=0.35,
                activity_velocity=1.0,
                first_seen=document.published_at,
                last_seen=document.published_at,
                locations=[],
                topics=sorted(_tokens(document.title))[:5],
            )
            repo.entities.append(entity)
            entity_ids.append(entity.id)
        return sorted(set(entity_ids))

    @staticmethod
    def _evidence(document: Document) -> EvidenceRef:
        excerpt = document.content[:700].strip() or document.title
        return EvidenceRef(
            id=f"ev-{document.id}",
            source_id=document.source_id,
            document_id=document.id,
            source_name=document.metadata.get("source_name", document.source_id),
            excerpt=excerpt,
            published_at=document.published_at,
            retrieved_at=document.retrieved_at,
            canonical_url=document.canonical_url,
            primary_source=bool(document.metadata.get("primary_source", False)),
        )

    def _best_event(
        self, document: Document, entity_ids: list[str], repo: DemoRepository
    ) -> Event | None:
        best: tuple[float, Event] | None = None
        doc_entities = set(entity_ids)
        for event in repo.events:
            hours = abs((document.published_at - event.latest_confirmation).total_seconds()) / 3600
            if hours > 72:
                continue
            title_score = _jaccard(document.title, event.title)
            shared = len(doc_entities & set(event.entity_ids))
            entity_score = shared / max(1, len(doc_entities | set(event.entity_ids)))
            score = 0.7 * title_score + 0.3 * entity_score
            if score >= 0.52 and (best is None or score > best[0]):
                best = (score, event)
        return best[1] if best else None

    def _update_observational_graph(
        self, event: Event, evidence: EvidenceRef, repo: DemoRepository
    ) -> None:
        for left, right in combinations(sorted(event.entity_ids), 2):
            existing = next(
                (
                    rel
                    for rel in repo.relationships
                    if rel.source_entity_id == left
                    and rel.target_entity_id == right
                    and rel.relationship_type == "CO_OCCURS_WITH"
                    and rel.valid_to is None
                ),
                None,
            )
            if existing:
                existing.source_count += 1
                existing.confidence = min(0.99, 0.45 + 0.1 * existing.source_count)
                existing.strength = min(1.0, existing.strength + 0.1)
                existing.evidence_ids = sorted(set(existing.evidence_ids) | {evidence.id})
                continue
            digest = hashlib.sha256(f"{left}|{right}|cooccurs".encode()).hexdigest()[:18]
            repo.relationships.append(
                TemporalRelationship(
                    id=f"rel-live-{digest}",
                    workspace_id=event.workspace_id,
                    source_entity_id=left,
                    relationship_type="CO_OCCURS_WITH",
                    target_entity_id=right,
                    valid_from=event.first_observed,
                    source_count=1,
                    confidence=0.55,
                    evidence_ids=[evidence.id],
                    strength=0.4,
                )
            )

    @staticmethod
    def _update_related_events(repo: DemoRepository) -> None:
        recent = sorted(repo.events, key=lambda item: item.latest_confirmation, reverse=True)[:100]
        for event in recent:
            related = []
            for other in recent:
                if event.id == other.id:
                    continue
                shared = set(event.entity_ids) & set(other.entity_ids)
                if shared or _jaccard(event.title, other.title) >= 0.35:
                    related.append(other.id)
            event.related_event_ids = related[:8]

    @staticmethod
    def _refresh_velocity_signals(repo: DemoRepository) -> None:
        if not repo.events:
            return
        anchor = max(event.latest_confirmation for event in repo.events)
        current_start = anchor - timedelta(hours=6)
        baseline_start = current_start - timedelta(hours=24)
        current = Counter()
        baseline = Counter()
        for event in repo.events:
            bucket = current if event.latest_confirmation >= current_start else baseline
            if event.latest_confirmation < baseline_start:
                continue
            for entity_id in event.entity_ids:
                bucket[entity_id] += 1

        for entity in repo.entities:
            recent_rate = current[entity.id] / 6
            baseline_rate = baseline[entity.id] / 24
            multiplier = recent_rate / max(0.05, baseline_rate)
            entity.activity_velocity = round(max(entity.activity_velocity, multiplier), 2)
            if current[entity.id] < 3 or multiplier < 4:
                continue
            signal_id = f"sig-live-velocity-{entity.id}"
            signal = next((item for item in repo.signals if item.id == signal_id), None)
            metrics = {
                "multiplier": round(multiplier, 2),
                "mentions_current_window": current[entity.id],
                "baseline_mentions": baseline[entity.id],
            }
            if signal:
                signal.metrics = metrics
                signal.detected_at = anchor
                continue
            repo.signals.append(
                Signal(
                    id=signal_id,
                    workspace_id=entity.workspace_id,
                    signal_type=SignalType.VELOCITY,
                    title=f"{entity.name} activity spike",
                    detected_at=anchor,
                    entity_ids=[entity.id],
                    event_ids=[
                        event.id
                        for event in repo.events
                        if entity.id in event.entity_ids and event.latest_confirmation >= current_start
                    ],
                    confidence=0.82,
                    severity="high",
                    metrics=metrics,
                    deterministic_basis=(
                        "Six-hour event appearance rate divided by the preceding 24-hour baseline "
                        "exceeded the configured 4× threshold with at least three current events."
                    ),
                    explanation=(
                        f"{entity.name} is appearing materially more often than its trailing baseline. "
                        "The threshold was calculated from stored event state, not generated by an LLM."
                    ),
                    evidence_ids=[],
                )
            )
