from __future__ import annotations

from dataclasses import dataclass
from typing import Any


@dataclass(slots=True)
class SearchHit:
    kind: str
    id: str
    title: str
    score: float
    metadata: dict[str, Any]


def rank_demo_results(query: str, rows: list[dict[str, Any]]) -> list[SearchHit]:
    terms = {term for term in query.casefold().split() if term}
    hits: list[SearchHit] = []
    for row in rows:
        haystack = " ".join(str(v) for v in row.values()).casefold()
        matched = sum(1 for term in terms if term in haystack)
        if not matched:
            continue
        score = matched / max(1, len(terms))
        hits.append(
            SearchHit(
                kind=str(row.get("kind", "unknown")),
                id=str(row.get("id", "")),
                title=str(row.get("title") or row.get("name") or row.get("id")),
                score=score,
                metadata=row,
            )
        )
    return sorted(hits, key=lambda hit: (-hit.score, hit.title))
