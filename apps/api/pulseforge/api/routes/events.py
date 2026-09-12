from __future__ import annotations

from fastapi import APIRouter, HTTPException

from pulseforge.api.deps import Repo

router = APIRouter(tags=["events"])


@router.get("/events/{event_id}")
def get_event(event_id: str, repo: Repo):
    result = repo.get_event(event_id)
    if result is None:
        raise HTTPException(status_code=404, detail="Event not found")
    return result


@router.get("/events/{event_id}/evidence")
def get_event_evidence(event_id: str, repo: Repo):
    event = repo.get_event(event_id)
    if event is None:
        raise HTTPException(status_code=404, detail="Event not found")
    claims = [repo.get_claim(claim_id) for claim_id in event.claim_ids]
    claims = [claim for claim in claims if claim is not None]
    return {
        "event_id": event.id,
        "claims": claims,
        "evidence": event.evidence,
        "source_count": event.source_count,
        "cluster_reasons": event.cluster_reasons,
    }


@router.get("/events/{event_id}/related")
def related_events(event_id: str, repo: Repo):
    event = repo.get_event(event_id)
    if event is None:
        raise HTTPException(status_code=404, detail="Event not found")
    return [
        related
        for related_id in event.related_event_ids
        if (related := repo.get_event(related_id)) is not None
    ]
