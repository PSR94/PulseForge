from __future__ import annotations

from functools import lru_cache

from pulseforge.domain.models import Document


class LiveDocumentStore:
    def __init__(self) -> None:
        self.documents: dict[str, Document] = {}

    def put_many(self, documents: list[Document]) -> None:
        for document in documents:
            self.documents[document.id] = document

    def list(self, workspace_id: str) -> list[Document]:
        return sorted(
            [doc for doc in self.documents.values() if doc.workspace_id == workspace_id],
            key=lambda doc: doc.published_at,
            reverse=True,
        )


@lru_cache
def get_live_document_store() -> LiveDocumentStore:
    return LiveDocumentStore()
