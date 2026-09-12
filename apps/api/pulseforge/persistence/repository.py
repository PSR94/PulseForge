from __future__ import annotations

from datetime import datetime

from sqlalchemy import select
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.orm import Session

from pulseforge.domain.models import Document, ProcessingStage, Source, SourceObservations, SourceType
from pulseforge.persistence.schema import DocumentRow, SourceRow


class SqlIntelligenceRepository:
    def __init__(self, session: Session):
        self.session = session

    def get_source(self, source_id: str) -> Source | None:
        row = self.session.get(SourceRow, source_id)
        if row is None:
            return None
        return Source(
            id=row.id,
            workspace_id=row.workspace_id,
            name=row.name,
            source_type=SourceType(row.source_type),
            source_url=row.source_url,
            canonical_url=row.canonical_url,
            observations=SourceObservations.model_validate(row.observations or {}),
            metadata=row.metadata_json or {},
        )

    def save_documents(self, documents: list[Document]) -> list[Document]:
        persisted: list[Document] = []
        for document in documents:
            values = {
                "id": document.id,
                "workspace_id": document.workspace_id,
                "source_id": document.source_id,
                "source_type": document.source_type.value,
                "source_url": str(document.source_url),
                "canonical_url": str(document.canonical_url),
                "retrieved_at": document.retrieved_at,
                "published_at": document.published_at,
                "content_hash": document.content_hash,
                "title": document.title,
                "content": document.content,
                "stage": document.stage.value,
                "attempt_count": document.attempt_count,
                "last_error": document.last_error,
                "metadata_json": document.metadata,
            }
            stmt = (
                insert(DocumentRow)
                .values(**values)
                .on_conflict_do_nothing(index_elements=["workspace_id", "content_hash"])
            )
            result = self.session.execute(stmt)
            if result.rowcount:
                persisted.append(document)
        return persisted

    def mark_document_stage(
        self, document_id: str, stage: str, *, error: str | None = None
    ) -> None:
        row = self.session.get(DocumentRow, document_id)
        if row is None:
            raise KeyError(document_id)
        row.stage = stage
        row.last_error = error
        if error:
            row.attempt_count += 1

    def documents_between(
        self, workspace_id: str, start: datetime, end: datetime
    ) -> list[Document]:
        rows = self.session.scalars(
            select(DocumentRow)
            .where(DocumentRow.workspace_id == workspace_id)
            .where(DocumentRow.published_at >= start)
            .where(DocumentRow.published_at < end)
            .order_by(DocumentRow.published_at.desc())
        ).all()
        return [self._document(row) for row in rows]

    @staticmethod
    def _document(row: DocumentRow) -> Document:
        return Document(
            id=row.id,
            workspace_id=row.workspace_id,
            source_id=row.source_id,
            source_type=SourceType(row.source_type),
            source_url=row.source_url,
            canonical_url=row.canonical_url,
            retrieved_at=row.retrieved_at,
            published_at=row.published_at,
            content_hash=row.content_hash,
            title=row.title,
            content=row.content,
            metadata=row.metadata_json or {},
            stage=ProcessingStage(row.stage),
            attempt_count=row.attempt_count,
            last_error=row.last_error,
        )
