from __future__ import annotations

from fastapi import APIRouter, HTTPException

from pulseforge.api.deps import Repo

router = APIRouter(tags=["signals"])


@router.get("/signals")
def signals(repo: Repo):
    return sorted(repo.signals, key=lambda signal: signal.detected_at, reverse=True)


@router.get("/signals/{signal_id}")
def signal(signal_id: str, repo: Repo):
    result = next((item for item in repo.signals if item.id == signal_id), None)
    if result is None:
        raise HTTPException(status_code=404, detail="Signal not found")
    evidence = []
    for event_id in result.event_ids:
        event = repo.get_event(event_id)
        if event:
            evidence.extend(event.evidence)
    return {"signal": result, "evidence": evidence}
