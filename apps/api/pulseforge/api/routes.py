from __future__ import annotations

import asyncio
import json
from datetime import UTC, datetime, timedelta
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Query
from fastapi.responses import PlainTextResponse, StreamingResponse

from pulseforge.config import get_settings
from pulseforge.connectors.rss import RssConnector
from pulseforge.domain.models import (AnalystAnswer, AnalystQuestion, Briefing, GraphDiff, Source, SourceCreate, SourceIngestResult, SourceObservations)
from pulseforge.services.security import validate_public_url
from pulseforge.services.analyst import StructuredAnalyst
from pulseforge.services.demo_repository import DemoRepository, get_demo_repository

router = APIRouter(prefix="/api/v1")
Repo = Annotated[DemoRepository, Depends(get_demo_repository)]


@router.get("/workspaces")
def workspaces(repo: Repo):
    return [repo.workspace]


@router.get("/workspaces/{workspace_id}")
def workspace(workspace_id: str, repo: Repo):
    if workspace_id != repo.workspace.id:
        raise HTTPException(status_code=404, detail="Workspace not found")
    return repo.workspace


@router.get("/feed")
def feed(repo: Repo, limit: int = Query(25, ge=1, le=200)):
    return repo.list_events()[:limit]


@router.get("/feed/stream")
async def feed_stream(repo: Repo):
    async def generate():
        for event in repo.list_events():
            payload = json.dumps(event.model_dump(mode="json"))
            yield f"event: intelligence\ndata: {payload}\n\n"
            await asyncio.sleep(0.05)
        yield "event: heartbeat\ndata: {\"status\":\"caught_up\"}\n\n"

    return StreamingResponse(generate(), media_type="text/event-stream")


@router.get("/events/{event_id}")
def event(event_id: str, repo: Repo):
    result = repo.get_event(event_id)
    if result is None:
        raise HTTPException(status_code=404, detail="Event not found")
    return result


@router.get("/entities/{entity_id}")
def entity(entity_id: str, repo: Repo):
    result = repo.get_entity(entity_id)
    if result is None:
        raise HTTPException(status_code=404, detail="Entity not found")
    return {
        "entity": result,
        "events": [event for event in repo.events if entity_id in event.entity_ids],
        "relationships": [
            rel for rel in repo.relationships
            if rel.source_entity_id == entity_id or rel.target_entity_id == entity_id
        ],
        "claims": [claim for claim in repo.claims if claim.subject_entity_id == entity_id],
        "contradictions": [item for item in repo.contradictions if item.subject_entity_id == entity_id],
        "signals": [signal for signal in repo.signals if entity_id in signal.entity_ids],
    }


@router.get("/graph")
def graph(repo: Repo, at: datetime | None = None):
    at = at or datetime(2026, 9, 11, 15, 40, tzinfo=UTC)
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


@router.get("/timeline")
def timeline(repo: Repo):
    return sorted(repo.events, key=lambda event: event.first_observed)


@router.get("/signals")
def signals(repo: Repo):
    return sorted(repo.signals, key=lambda signal: signal.detected_at, reverse=True)


@router.get("/claims")
def claims(repo: Repo):
    return repo.claims


@router.get("/claims/conflicts")
def conflicts(repo: Repo):
    return [
        {
            "contradiction": contradiction,
            "claims": [repo.get_claim(claim_id) for claim_id in contradiction.claim_ids],
        }
        for contradiction in repo.contradictions
    ]


@router.get("/sources")
def sources(repo: Repo):
    return repo.sources


@router.post("/sources", response_model=Source)
def add_source(payload: SourceCreate, repo: Repo):
    if payload.workspace_id != repo.workspace.id:
        raise HTTPException(status_code=404, detail="Workspace not found")
    validate_public_url(str(payload.source_url), resolve_dns=False)
    source_id = "src-user-" + str(abs(hash(str(payload.source_url))))[:10]
    existing = next((item for item in repo.sources if item.id == source_id), None)
    if existing:
        return existing
    source = Source(
        id=source_id, workspace_id=payload.workspace_id, name=payload.name, source_type=payload.source_type,
        source_url=payload.source_url, canonical_url=payload.source_url, observations=SourceObservations(),
        metadata={"user_added": True},
    )
    repo.sources.append(source)
    return source


@router.post("/sources/{source_id}/ingest", response_model=SourceIngestResult)
async def ingest_source(source_id: str, repo: Repo):
    source = next((item for item in repo.sources if item.id == source_id), None)
    if source is None:
        raise HTTPException(status_code=404, detail="Source not found")
    if source.source_type.value != "rss":
        raise HTTPException(status_code=422, detail="Only RSS/Atom ingestion is enabled in the first vertical slice")
    documents = await RssConnector(get_settings()).fetch(source)
    return SourceIngestResult(
        source_id=source.id, documents_received=len(documents), document_ids=[doc.id for doc in documents],
        stage="INGESTED",
        message="Documents were fetched with bounded SSRF-safe ingestion. Downstream demo intelligence remains deterministic until a durable repository is configured.",
    )


@router.get("/search")
def search(q: str, repo: Repo):
    return repo.search(q)


@router.post("/analyst/ask", response_model=AnalystAnswer)
def ask_analyst(payload: AnalystQuestion, repo: Repo):
    return StructuredAnalyst(repo).answer(payload.question)


@router.get("/analyst/tools")
def analyst_tools(repo: Repo):
    analyst = StructuredAnalyst(repo)
    return [{"name": tool.name, "description": tool.description} for tool in analyst.tools.values()]


@router.get("/briefings", response_model=list[Briefing])
def briefings(repo: Repo):
    return [repo.build_briefing()]


@router.post("/briefings/generate", response_model=Briefing)
def generate_briefing(repo: Repo):
    return repo.build_briefing()


@router.get("/briefings/{briefing_id}/markdown", response_class=PlainTextResponse)
def briefing_markdown(briefing_id: str, repo: Repo):
    briefing = repo.build_briefing()
    if briefing_id != briefing.id:
        raise HTTPException(status_code=404, detail="Briefing not found")
    return briefing.markdown


@router.get("/what-changed")
def what_changed(repo: Repo, hours: int = Query(24, ge=1, le=24 * 365)):
    after = datetime(2026, 9, 11, 15, 40, tzinfo=UTC)
    before = after - timedelta(hours=hours)
    return repo.temporal_diff(before, after)
