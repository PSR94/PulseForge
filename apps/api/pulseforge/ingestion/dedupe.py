from __future__ import annotations

from collections.abc import Iterable

from pulseforge.domain.models import Document, ProcessingStage


def deduplicate(documents: Iterable[Document]) -> tuple[list[Document], list[str]]:
    seen: set[tuple[str, str]] = set()
    kept: list[Document] = []
    duplicate_ids: list[str] = []
    for document in documents:
        key = (document.workspace_id, document.content_hash)
        if key in seen:
            duplicate_ids.append(document.id)
            continue
        seen.add(key)
        kept.append(document.model_copy(update={"stage": ProcessingStage.DEDUPLICATED}))
    return kept, duplicate_ids
