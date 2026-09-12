from __future__ import annotations

from pulseforge.domain.models import ProcessingStage

ORDER = [
    ProcessingStage.INGESTED,
    ProcessingStage.NORMALIZED,
    ProcessingStage.DEDUPLICATED,
    ProcessingStage.ENRICHED,
    ProcessingStage.ENTITY_LINKED,
    ProcessingStage.EVENT_CLUSTERED,
    ProcessingStage.CLAIM_EXTRACTED,
    ProcessingStage.GRAPH_UPDATED,
    ProcessingStage.SIGNAL_ANALYZED,
    ProcessingStage.INDEXED,
]

_NEXT = {stage: ORDER[index + 1] for index, stage in enumerate(ORDER[:-1])}


def next_stage(stage: ProcessingStage) -> ProcessingStage | None:
    return _NEXT.get(stage)


def can_advance(current: ProcessingStage, target: ProcessingStage) -> bool:
    return ORDER.index(target) == ORDER.index(current) + 1
