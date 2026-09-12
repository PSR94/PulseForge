from __future__ import annotations

import hashlib
from datetime import UTC, datetime

from fastapi import APIRouter, File, Form, HTTPException, UploadFile

from pulseforge.api.deps import Repo
from pulseforge.config import get_settings
from pulseforge.domain.models import Document, Source, SourceObservations, SourceType
from pulseforge.ingestion.enrichment import deterministic_enrich
from pulseforge.ingestion.normalizer import normalize_document
from pulseforge.services.live_store import get_live_document_store
from pulseforge.services.materializer import LiveMaterializer

router = APIRouter(tags=["uploads"])

TEXT_TYPES = {"text/plain", "text/markdown", "application/json"}


@router.post("/documents/upload")
async def upload_document(
    repo: Repo,
    file: UploadFile = File(...),
    title: str | None = Form(default=None),
):
    settings = get_settings()
    content_type = (file.content_type or "application/octet-stream").split(";")[0].lower()
    if content_type not in TEXT_TYPES:
        raise HTTPException(
            status_code=415,
            detail=f"Upload type {content_type} is not enabled; use plain text, Markdown, or JSON",
        )
    body = await file.read(settings.upload_max_bytes + 1)
    if len(body) > settings.upload_max_bytes:
        raise HTTPException(status_code=413, detail="Upload exceeds configured byte limit")
    try:
        text = body.decode("utf-8")
    except UnicodeDecodeError as exc:
        raise HTTPException(status_code=422, detail="Upload must be UTF-8 text") from exc

    source = next((item for item in repo.sources if item.id == "src-manual-upload"), None)
    if source is None:
        source = Source(
            id="src-manual-upload",
            workspace_id=repo.workspace.id,
            name="Manual uploads",
            source_type=SourceType.UPLOAD,
            source_url="https://pulseforge.local/uploads",
            canonical_url="https://pulseforge.local/uploads",
            observations=SourceObservations(primary_source=True),
            metadata={"internal": True},
        )
        repo.sources.append(source)

    now = datetime.now(UTC)
    digest = hashlib.sha256(body).hexdigest()
    document = Document(
        id=f"doc-upload-{digest[:24]}",
        workspace_id=repo.workspace.id,
        source_id=source.id,
        source_type=SourceType.UPLOAD,
        source_url=source.source_url,
        canonical_url=f"https://pulseforge.local/uploads/{digest[:24]}",
        retrieved_at=now,
        published_at=now,
        content_hash=digest,
        title=title or file.filename or "Uploaded intelligence document",
        content=text,
        metadata={
            "source_name": source.name,
            "primary_source": True,
            "uploaded_filename": file.filename,
            "content_type": content_type,
        },
    )
    document = deterministic_enrich(normalize_document(document))
    get_live_document_store().put_many([document])
    events = LiveMaterializer().materialize([document], repo)
    return {
        "document": document,
        "event_ids": [event.id for event in events],
        "message": "Upload normalized, enriched, materialized into workspace state, and indexed.",
    }
