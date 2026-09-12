from __future__ import annotations

import re

from pulseforge.domain.models import Document, ProcessingStage

ORG_SUFFIXES = ("Inc", "Corp", "Corporation", "Labs", "AI", "Systems", "Technologies")
TOKEN = re.compile(r"\b[A-Z][A-Za-z0-9&.-]{1,}(?:\s+[A-Z][A-Za-z0-9&.-]{1,}){0,3}\b")


def deterministic_enrich(document: Document) -> Document:
    candidates = []
    for value in TOKEN.findall(document.title + " " + document.content[:4000]):
        if any(value.endswith(suffix) for suffix in ORG_SUFFIXES) or value in {
            "OpenAI", "NVIDIA", "Microsoft", "Google", "Meta", "Anthropic", "AWS", "GitHub"
        }:
            candidates.append(value)
    metadata = dict(document.metadata)
    metadata["entity_candidates"] = sorted(set(candidates))[:50]
    metadata["word_count"] = len(document.content.split())
    return document.model_copy(update={"metadata": metadata, "stage": ProcessingStage.ENRICHED})
