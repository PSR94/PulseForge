from __future__ import annotations

import re
from pulseforge.domain.models import Document, ProcessingStage

_WS = re.compile(r"\s+")


def normalize_document(document: Document) -> Document:
    title = _WS.sub(" ", document.title).strip()
    content = _WS.sub(" ", document.content.replace("\x00", " ")).strip()
    return document.model_copy(
        update={
            "title": title[:1000],
            "content": content,
            "stage": ProcessingStage.NORMALIZED,
        }
    )
