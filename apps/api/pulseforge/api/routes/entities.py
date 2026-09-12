from __future__ import annotations

from fastapi import APIRouter, HTTPException

from pulseforge.api.deps import Repo

router = APIRouter(tags=["entities"])


@router.get("/entities")
def list_entities(repo: Repo):
    return sorted(repo.entities, key=lambda entity: entity.importance, reverse=True)


@router.get("/entities/{entity_id}")
def entity_dossier(entity_id: str, repo: Repo):
    entity = repo.get_entity(entity_id)
    if entity is None:
        raise HTTPException(status_code=404, detail="Entity not found")
    return {
        "entity": entity,
        "events": [event for event in repo.events if entity_id in event.entity_ids],
        "relationships": [
            rel
            for rel in repo.relationships
            if rel.source_entity_id == entity_id or rel.target_entity_id == entity_id
        ],
        "claims": [claim for claim in repo.claims if claim.subject_entity_id == entity_id],
        "contradictions": [
            item for item in repo.contradictions if item.subject_entity_id == entity_id
        ],
        "signals": [signal for signal in repo.signals if entity_id in signal.entity_ids],
    }
