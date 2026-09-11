from __future__ import annotations

from dataclasses import dataclass, field
from datetime import UTC, datetime

from pulseforge.domain.models import ProcessingStage


PIPELINE_ORDER = list(ProcessingStage)


@dataclass
class ProcessingRecord:
    document_id: str
    stage: ProcessingStage = ProcessingStage.INGESTED
    attempts: int = 1
    last_error: str | None = None
    history: list[tuple[ProcessingStage, datetime]] = field(default_factory=list)

    def __post_init__(self) -> None:
        if not self.history:
            self.history.append((self.stage, datetime.now(UTC)))

    def advance(self, target: ProcessingStage) -> None:
        current_index = PIPELINE_ORDER.index(self.stage)
        target_index = PIPELINE_ORDER.index(target)
        if target_index != current_index + 1:
            raise ValueError(f"Invalid pipeline transition: {self.stage} -> {target}")
        self.stage = target
        self.last_error = None
        self.history.append((target, datetime.now(UTC)))

    def fail(self, error: Exception | str) -> None:
        self.last_error = str(error)

    def retry(self) -> None:
        self.attempts += 1
        self.last_error = None
