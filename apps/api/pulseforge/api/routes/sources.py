from __future__ import annotations

from fastapi import APIRouter, HTTPException

from pulseforge.api.deps import Repo
from pulseforge.domain.models import (
    ProcessingStage,
    Source,
    SourceCreate,
    SourceIngestResult,
    SourceObservations,
)
from pulseforge.runtime import connector_registry, ingestion_orchestrator
from pulseforge.services.live_store import get_live_document_store
from pulseforge.services.materializer import LiveMaterializer
from pulseforge.services.security import validate_public_url

router = APIRouter(tags=["sources"])


@router.get("/connectors")
def connectors():
    registry = connector_registry()
    return {
        "supported": registry.supported_types(),
        "production_note": (
            "RSS, JSON, web, GitHub releases, arXiv, and Hacker News have concrete "
            "connectors. API/upload connectors use the same Source/Document contract."
        ),
    }


@router.get("/sources")
def sources(repo: Repo):
    return repo.sources


@router.get("/documents")
def documents(repo: Repo):
    return get_live_document_store().list(repo.workspace.id)


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
        id=source_id,
        workspace_id=payload.workspace_id,
        name=payload.name,
        source_type=payload.source_type,
        source_url=payload.source_url,
        canonical_url=payload.source_url,
        observations=SourceObservations(),
        metadata={"user_added": True},
    )
    repo.sources.append(source)
    return source


@router.post("/sources/{source_id}/ingest", response_model=SourceIngestResult)
async def ingest_source(source_id: str, repo: Repo):
    source = next((item for item in repo.sources if item.id == source_id), None)
    if source is None:
        raise HTTPException(status_code=404, detail="Source not found")
    try:
        documents, report = await ingestion_orchestrator().ingest(source)
    except ValueError as exc:
        raise HTTPException(status_code=422, detail=str(exc)) from exc

    for document in documents:
        document.metadata["source_name"] = source.name
        document.metadata["primary_source"] = source.observations.primary_source

    get_live_document_store().put_many(documents)
    materialized = LiveMaterializer().materialize(documents, repo)

    return SourceIngestResult(
        source_id=source.id,
        documents_received=report.received,
        document_ids=[document.id for document in documents],
        stage=ProcessingStage.INDEXED,
        message=(
            f"Fetched {report.received} documents, removed {report.duplicates} duplicates, "
            f"materialized {len(materialized)} normalized event clusters, updated the temporal "
            "graph, recalculated velocity signals, and indexed the result in the live workspace."
        ),
    )
