from __future__ import annotations

from datetime import UTC, datetime, timedelta

from fastapi import APIRouter, HTTPException, Query

from pulseforge.api.deps import Repo
from pulseforge.domain.models import GraphDiff

router = APIRouter(tags=["graph"])


@router.get("/graph")
def graph(repo: Repo, at: datetime | None = None):
    at = at or datetime.now(UTC)
    # The deterministic demo is anchored to 2026-09-11; use its end point when querying "now".
    if at.year > 2026 or (at.year == 2026 and at.month > 9):
        at = datetime(2026, 9, 11, 15, 40, tzinfo=UTC)
    snapshot = repo.graph_at(at)
    entities = [entity for entity in repo.entities if entity.id in snapshot.entity_ids]
    return {"snapshot": snapshot, "entities": entities}


@router.get("/graph/diff", response_model=GraphDiff)
def graph_diff(
    repo: Repo,
    from_at: datetime = Query(alias="from"),
    to_at: datetime = Query(alias="to"),
):
    if to_at <= from_at:
        raise HTTPException(status_code=422, detail="to must be later than from")
    return repo.temporal_diff(from_at, to_at)


@router.get("/what-changed")
def what_changed(repo: Repo, hours: int = Query(24, ge=1, le=24 * 365)):
    after = datetime(2026, 9, 11, 15, 40, tzinfo=UTC)
    before = after - timedelta(hours=hours)
    return repo.temporal_diff(before, after)


@router.get("/timeline")
def timeline(repo: Repo):
    return sorted(repo.events, key=lambda event: event.first_observed)
