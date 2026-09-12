from __future__ import annotations

import hashlib
from datetime import UTC, datetime
from typing import Iterable

from pulseforge.domain.models import Event, Signal
from pulseforge.domain.watchlists import Alert, WatchCondition, WatchlistRule


def _compare(actual: float | int | str, condition: WatchCondition) -> bool:
    op = condition.operator
    expected = condition.value
    if op == "eq":
        return actual == expected
    if op == "contains":
        return str(expected).casefold() in str(actual).casefold()
    if op in {"gt", "gte", "lt", "lte"}:
        a, b = float(actual), float(expected)
        return {"gt": a > b, "gte": a >= b, "lt": a < b, "lte": a <= b}[op]
    raise ValueError(f"Unsupported watchlist operator: {op}")


def evaluate_rule(
    rule: WatchlistRule,
    *,
    events: Iterable[Event],
    signals: Iterable[Signal],
) -> list[Alert]:
    if not rule.enabled:
        return []
    matches: list[tuple[str, dict[str, float | int | str], list[str], list[str]]] = []

    target = rule.target.casefold()
    for signal in signals:
        searchable = " ".join([signal.title, signal.explanation, *signal.entity_ids]).casefold()
        if target not in searchable:
            continue
        context = {**signal.metrics, "severity": signal.severity, "confidence": signal.confidence}
        if all(_compare(context.get(c.field, ""), c) for c in rule.conditions):
            matches.append((signal.title, context, signal.evidence_ids, signal.event_ids))

    for event in events:
        searchable = " ".join([event.title, event.explanation, *event.entity_ids, *event.topics]).casefold()
        if target not in searchable:
            continue
        context = {
            "source_count": event.source_count,
            "impact_score": event.impact_score,
            "novelty_score": event.novelty_score,
            "confidence": event.confidence,
        }
        if all(_compare(context.get(c.field, ""), c) for c in rule.conditions):
            matches.append((event.title, context, [e.id for e in event.evidence], [event.id]))

    alerts: list[Alert] = []
    now = datetime.now(UTC)
    for title, metrics, evidence_ids, event_ids in matches:
        fingerprint = hashlib.sha256(f"{rule.id}|{title}".encode()).hexdigest()[:20]
        alerts.append(
            Alert(
                id=f"alert-{fingerprint}",
                workspace_id=rule.workspace_id,
                rule_id=rule.id,
                title=f"{rule.name}: {title}",
                explanation=(
                    f"Rule '{rule.name}' fired because target '{rule.target}' matched and "
                    "all deterministic threshold conditions were satisfied."
                ),
                fired_at=now,
                severity=str(metrics.get("severity", "medium")),
                metrics=metrics,
                evidence_ids=evidence_ids,
                event_ids=event_ids,
            )
        )
    return alerts
