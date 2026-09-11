from __future__ import annotations

from dataclasses import dataclass
from difflib import SequenceMatcher


@dataclass(frozen=True)
class ResolutionResult:
    canonical_name: str
    confidence: float
    reasons: tuple[str, ...]


def normalize_name(value: str) -> str:
    value = value.casefold().replace("&", " and ")
    for suffix in (" corporation", " corp.", " corp", " incorporated", " inc.", " inc", " ltd.", " ltd"):
        if value.endswith(suffix):
            value = value[: -len(suffix)]
    return " ".join(value.replace(".", " ").split())


def resolve_entity(candidate: str, aliases: dict[str, list[str]]) -> ResolutionResult | None:
    normalized = normalize_name(candidate)
    best: tuple[str, float, list[str]] | None = None
    for canonical, names in aliases.items():
        canonical_names = [canonical, *names]
        for alias in canonical_names:
            alias_norm = normalize_name(alias)
            if normalized == alias_norm:
                return ResolutionResult(canonical, 1.0, (f"exact normalized alias: {alias}",))
            score = SequenceMatcher(None, normalized, alias_norm).ratio()
            if score >= 0.86 and (best is None or score > best[1]):
                best = (canonical, score, [f"name similarity {score:.2f} against {alias}"])
    if best:
        return ResolutionResult(best[0], round(best[1], 3), tuple(best[2]))
    return None
