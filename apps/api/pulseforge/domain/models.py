from __future__ import annotations

from datetime import datetime
from enum import StrEnum
from typing import Any, Literal

from pydantic import BaseModel, Field, HttpUrl


class ProcessingStage(StrEnum):
    INGESTED = "INGESTED"
    NORMALIZED = "NORMALIZED"
    DEDUPLICATED = "DEDUPLICATED"
    ENRICHED = "ENRICHED"
    ENTITY_LINKED = "ENTITY_LINKED"
    EVENT_CLUSTERED = "EVENT_CLUSTERED"
    CLAIM_EXTRACTED = "CLAIM_EXTRACTED"
    GRAPH_UPDATED = "GRAPH_UPDATED"
    SIGNAL_ANALYZED = "SIGNAL_ANALYZED"
    INDEXED = "INDEXED"


class SourceType(StrEnum):
    RSS = "rss"
    WEB = "web"
    JSON = "json"
    GITHUB = "github"
    ARXIV = "arxiv"
    HACKER_NEWS = "hacker_news"
    API = "api"
    UPLOAD = "upload"


class EntityType(StrEnum):
    PERSON = "person"
    COMPANY = "company"
    ORGANIZATION = "organization"
    PRODUCT = "product"
    TECHNOLOGY = "technology"
    LOCATION = "location"
    RESEARCH_PAPER = "research_paper"
    PROJECT = "project"
    EVENT = "event"
    CLAIM = "claim"
    TOPIC = "topic"


class ClaimKind(StrEnum):
    FACTUAL = "factual"
    FORECAST = "forecast"
    OPINION = "opinion"


class SignalType(StrEnum):
    VELOCITY = "velocity"
    NOVEL_RELATIONSHIP = "novel_relationship"
    SOURCE_DIVERGENCE = "source_divergence"
    TOPIC_EMERGENCE = "topic_emergence"
    EVENT_ESCALATION = "event_escalation"
    UNUSUAL_ACTIVITY = "unusual_activity"
    CROSS_DOMAIN_CONVERGENCE = "cross_domain_convergence"


class SourceObservations(BaseModel):
    primary_source: bool = False
    publication_history_days: int = 0
    corroborating_source_count: int = 0
    direct_quote_count: int = 0
    independent_confirmation_count: int = 0
    contradiction_count: int = 0


class Source(BaseModel):
    id: str
    workspace_id: str
    name: str
    source_type: SourceType
    source_url: HttpUrl
    canonical_url: HttpUrl
    observations: SourceObservations = Field(default_factory=SourceObservations)
    metadata: dict[str, Any] = Field(default_factory=dict)


class Document(BaseModel):
    id: str
    workspace_id: str
    source_id: str
    source_type: SourceType
    source_url: HttpUrl
    canonical_url: HttpUrl
    retrieved_at: datetime
    published_at: datetime
    content_hash: str
    title: str
    content: str
    metadata: dict[str, Any] = Field(default_factory=dict)
    stage: ProcessingStage = ProcessingStage.INGESTED
    attempt_count: int = 1
    last_error: str | None = None


class EvidenceRef(BaseModel):
    id: str
    source_id: str
    document_id: str
    source_name: str
    excerpt: str
    published_at: datetime
    retrieved_at: datetime
    canonical_url: HttpUrl
    primary_source: bool = False


class Entity(BaseModel):
    id: str
    workspace_id: str
    name: str
    entity_type: EntityType
    aliases: list[str] = Field(default_factory=list)
    description: str = ""
    external_ids: dict[str, str] = Field(default_factory=dict)
    importance: float = Field(ge=0, le=1)
    activity_velocity: float = Field(ge=0)
    first_seen: datetime
    last_seen: datetime
    locations: list[str] = Field(default_factory=list)
    topics: list[str] = Field(default_factory=list)


class Claim(BaseModel):
    id: str
    workspace_id: str
    subject_entity_id: str
    predicate: str
    object_value: str
    normalized_property: str
    kind: ClaimKind = ClaimKind.FACTUAL
    extraction_confidence: float = Field(ge=0, le=1)
    observed_at: datetime
    evidence: list[EvidenceRef]


class Event(BaseModel):
    id: str
    workspace_id: str
    title: str
    event_type: str
    first_observed: datetime
    latest_confirmation: datetime
    entity_ids: list[str]
    location: str | None = None
    latitude: float | None = None
    longitude: float | None = None
    confidence: float = Field(ge=0, le=1)
    novelty_score: float = Field(ge=0, le=1)
    impact_score: float = Field(ge=0, le=1)
    source_count: int = Field(ge=1)
    related_event_ids: list[str] = Field(default_factory=list)
    claim_ids: list[str] = Field(default_factory=list)
    evidence: list[EvidenceRef]
    explanation: str
    cluster_reasons: list[str] = Field(default_factory=list)
    topics: list[str] = Field(default_factory=list)


class TemporalRelationship(BaseModel):
    id: str
    workspace_id: str
    source_entity_id: str
    relationship_type: str
    target_entity_id: str
    valid_from: datetime
    valid_to: datetime | None = None
    source_count: int = Field(ge=1)
    confidence: float = Field(ge=0, le=1)
    evidence_ids: list[str] = Field(default_factory=list)
    strength: float = Field(default=1, ge=0)


class Contradiction(BaseModel):
    id: str
    workspace_id: str
    subject_entity_id: str
    normalized_property: str
    claim_ids: list[str]
    status: Literal["unresolved", "resolved", "superseded"] = "unresolved"
    explanation: str


class Signal(BaseModel):
    id: str
    workspace_id: str
    signal_type: SignalType
    title: str
    detected_at: datetime
    entity_ids: list[str] = Field(default_factory=list)
    event_ids: list[str] = Field(default_factory=list)
    confidence: float = Field(ge=0, le=1)
    severity: Literal["low", "medium", "high", "critical"]
    metrics: dict[str, float | int | str]
    deterministic_basis: str
    explanation: str
    evidence_ids: list[str] = Field(default_factory=list)


class GraphSnapshot(BaseModel):
    at: datetime
    entity_ids: list[str]
    relationships: list[TemporalRelationship]


class RelationshipStrengthChange(BaseModel):
    relationship_id: str
    before: float
    after: float
    delta: float


class GraphDiff(BaseModel):
    from_at: datetime
    to_at: datetime
    added_entity_ids: list[str]
    removed_entity_ids: list[str]
    added_relationships: list[TemporalRelationship]
    removed_relationships: list[TemporalRelationship]
    changed_relationships: list[RelationshipStrengthChange]
    introduced_contradiction_ids: list[str]
    accelerating_entity_ids: list[str]
    declining_entity_ids: list[str]
    emerging_topics: list[str]
    summary: str


class Workspace(BaseModel):
    id: str
    name: str
    description: str
    updated_at: datetime
    last_visited_at: datetime


class Briefing(BaseModel):
    id: str
    workspace_id: str
    title: str
    generated_at: datetime
    period_start: datetime
    period_end: datetime
    executive_summary: str
    top_developments: list[str]
    emerging_signals: list[str]
    entity_movements: list[str]
    contradictions: list[str]
    watch_list: list[str]
    evidence_ids: list[str]
    markdown: str


class AnalystQuestion(BaseModel):
    question: str = Field(min_length=2, max_length=2000)
    workspace_id: str = "ai-industry"


class AnalystCitation(BaseModel):
    kind: Literal["event", "claim", "signal", "evidence", "relationship"]
    id: str
    label: str


class AnalystAnswer(BaseModel):
    answer: str
    answer_type: Literal["fact", "inference", "prediction"] = "inference"
    tools_used: list[str]
    citations: list[AnalystCitation]
    uncertainty: str | None = None

class SourceCreate(BaseModel):
    workspace_id: str = "ai-industry"
    name: str = Field(min_length=2, max_length=120)
    source_url: HttpUrl
    source_type: SourceType = SourceType.RSS


class SourceIngestResult(BaseModel):
    source_id: str
    documents_received: int
    document_ids: list[str]
    stage: ProcessingStage
    message: str
