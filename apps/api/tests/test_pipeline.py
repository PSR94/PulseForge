import pytest

from pulseforge.domain.models import ProcessingStage
from pulseforge.services.pipeline import ProcessingRecord


def test_pipeline_requires_explicit_order_and_keeps_failure():
    record = ProcessingRecord("doc-1")
    record.advance(ProcessingStage.NORMALIZED)
    record.fail("entity service timeout")
    assert record.stage == ProcessingStage.NORMALIZED
    assert record.last_error == "entity service timeout"
    record.retry()
    assert record.attempts == 2
    assert record.last_error is None


def test_pipeline_cannot_skip_stages():
    record = ProcessingRecord("doc-1")
    with pytest.raises(ValueError):
        record.advance(ProcessingStage.ENRICHED)
