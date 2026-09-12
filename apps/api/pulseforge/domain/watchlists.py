from __future__ import annotations

from datetime import UTC, datetime
from enum import StrEnum
from typing import Any

from pydantic import BaseModel, Field


class WatchTargetType(StrEnum):
    ENTITY = "entity"
    TOPIC = "topic"
    RELATIONSHIP = "relationship"
    KEYWORD = "keyword"
    REGION = "region"


class WatchCondition(BaseModel):
    field: str
    operator: str
    value: str | float | int | list[str]


class WatchlistCreate(BaseModel):
    workspace_id: str = "ai-industry"
    name: str = Field(min_length=2, max_length=200)
    target_type: WatchTargetType
    target: str = Field(min_length=1, max_length=500)
    conditions: list[WatchCondition] = Field(default_factory=list)
    enabled: bool = True


class WatchlistRule(WatchlistCreate):
    id: str
    created_at: datetime = Field(default_factory=lambda: datetime.now(UTC))
    last_evaluated_at: datetime | None = None


class Alert(BaseModel):
    id: str
    workspace_id: str
    rule_id: str
    title: str
    explanation: str
    fired_at: datetime
    severity: str
    metrics: dict[str, Any] = Field(default_factory=dict)
    evidence_ids: list[str] = Field(default_factory=list)
    event_ids: list[str] = Field(default_factory=list)
    acknowledged_at: datetime | None = None
