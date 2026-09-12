from __future__ import annotations

import hashlib

from fastapi import APIRouter, HTTPException

from pulseforge.api.deps import Repo
from pulseforge.domain.watchlists import WatchlistCreate, WatchlistRule
from pulseforge.services.watchlist_store import get_watchlist_store
from pulseforge.services.watchlists import evaluate_rule

router = APIRouter(tags=["watchlists"])


@router.get("/watchlists")
def list_watchlists(workspace_id: str = "ai-industry"):
    return get_watchlist_store().list_rules(workspace_id)


@router.post("/watchlists", response_model=WatchlistRule)
def create_watchlist(payload: WatchlistCreate):
    fingerprint = hashlib.sha256(
        f"{payload.workspace_id}|{payload.name}|{payload.target_type}|{payload.target}".encode()
    ).hexdigest()[:20]
    rule = WatchlistRule(id=f"watch-{fingerprint}", **payload.model_dump())
    return get_watchlist_store().put_rule(rule)


@router.delete("/watchlists/{rule_id}", status_code=204)
def delete_watchlist(rule_id: str):
    if not get_watchlist_store().delete_rule(rule_id):
        raise HTTPException(status_code=404, detail="Watchlist not found")
    return None


@router.post("/watchlists/{rule_id}/evaluate")
def evaluate_watchlist(rule_id: str, repo: Repo):
    store = get_watchlist_store()
    rule = next((item for item in store.rules if item.id == rule_id), None)
    if rule is None:
        raise HTTPException(status_code=404, detail="Watchlist not found")
    alerts = evaluate_rule(rule, events=repo.events, signals=repo.signals)
    store.add_alerts(alerts)
    return {"rule": rule, "alerts": alerts}


@router.get("/alerts")
def list_alerts(workspace_id: str = "ai-industry"):
    return get_watchlist_store().list_alerts(workspace_id)
