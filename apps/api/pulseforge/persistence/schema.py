from __future__ import annotations

from datetime import datetime
from typing import Any

from sqlalchemy import DateTime, Float, ForeignKey, Index, Integer, JSON, String, Text, UniqueConstraint
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    pass


class WorkspaceRow(Base):
    __tablename__ = "workspaces"
    id: Mapped[str] = mapped_column(String(64), primary_key=True)
    name: Mapped[str] = mapped_column(String(200))
    description: Mapped[str] = mapped_column(Text, default="")
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True))
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True))


class SourceRow(Base):
    __tablename__ = "sources"
    id: Mapped[str] = mapped_column(String(96), primary_key=True)
    workspace_id: Mapped[str] = mapped_column(ForeignKey("workspaces.id", ondelete="CASCADE"), index=True)
    source_type: Mapped[str] = mapped_column(String(40), index=True)
    source_url: Mapped[str] = mapped_column(Text)
    canonical_url: Mapped[str] = mapped_column(Text)
    name: Mapped[str] = mapped_column(String(240))
    observations: Mapped[dict[str, Any]] = mapped_column(JSON, default=dict)
    metadata_json: Mapped[dict[str, Any]] = mapped_column("metadata", JSON, default=dict)


class DocumentRow(Base):
    __tablename__ = "documents"
    __table_args__ = (
        UniqueConstraint("workspace_id", "content_hash", name="uq_document_workspace_hash"),
        Index("ix_documents_workspace_published", "workspace_id", "published_at"),
    )
    id: Mapped[str] = mapped_column(String(128), primary_key=True)
    workspace_id: Mapped[str] = mapped_column(ForeignKey("workspaces.id", ondelete="CASCADE"), index=True)
    source_id: Mapped[str] = mapped_column(ForeignKey("sources.id", ondelete="CASCADE"), index=True)
    canonical_url: Mapped[str] = mapped_column(Text)
    retrieved_at: Mapped[datetime] = mapped_column(DateTime(timezone=True))
    published_at: Mapped[datetime] = mapped_column(DateTime(timezone=True))
    content_hash: Mapped[str] = mapped_column(String(64), index=True)
    title: Mapped[str] = mapped_column(Text)
    content: Mapped[str] = mapped_column(Text)
    stage: Mapped[str] = mapped_column(String(40), index=True)
    attempt_count: Mapped[int] = mapped_column(Integer, default=1)
    last_error: Mapped[str | None] = mapped_column(Text, nullable=True)
    metadata_json: Mapped[dict[str, Any]] = mapped_column("metadata", JSON, default=dict)


class EntityRow(Base):
    __tablename__ = "entities"
    __table_args__ = (Index("ix_entities_workspace_name", "workspace_id", "normalized_name"),)
    id: Mapped[str] = mapped_column(String(96), primary_key=True)
    workspace_id: Mapped[str] = mapped_column(ForeignKey("workspaces.id", ondelete="CASCADE"), index=True)
    entity_type: Mapped[str] = mapped_column(String(60), index=True)
    name: Mapped[str] = mapped_column(String(240))
    normalized_name: Mapped[str] = mapped_column(String(240))
    aliases: Mapped[list[str]] = mapped_column(JSON, default=list)
    external_ids: Mapped[dict[str, str]] = mapped_column(JSON, default=dict)
    importance: Mapped[float] = mapped_column(Float, default=0)
    activity_velocity: Mapped[float] = mapped_column(Float, default=0)
    first_seen: Mapped[datetime] = mapped_column(DateTime(timezone=True))
    last_seen: Mapped[datetime] = mapped_column(DateTime(timezone=True))


class EventRow(Base):
    __tablename__ = "events"
    id: Mapped[str] = mapped_column(String(96), primary_key=True)
    workspace_id: Mapped[str] = mapped_column(ForeignKey("workspaces.id", ondelete="CASCADE"), index=True)
    title: Mapped[str] = mapped_column(Text)
    event_type: Mapped[str] = mapped_column(String(80), index=True)
    first_observed: Mapped[datetime] = mapped_column(DateTime(timezone=True), index=True)
    latest_confirmation: Mapped[datetime] = mapped_column(DateTime(timezone=True), index=True)
    confidence: Mapped[float] = mapped_column(Float)
    novelty_score: Mapped[float] = mapped_column(Float)
    impact_score: Mapped[float] = mapped_column(Float)
    entity_ids: Mapped[list[str]] = mapped_column(JSON, default=list)
    related_event_ids: Mapped[list[str]] = mapped_column(JSON, default=list)
    evidence: Mapped[list[dict[str, Any]]] = mapped_column(JSON, default=list)
    cluster_reasons: Mapped[list[str]] = mapped_column(JSON, default=list)


class ClaimRow(Base):
    __tablename__ = "claims"
    id: Mapped[str] = mapped_column(String(96), primary_key=True)
    workspace_id: Mapped[str] = mapped_column(ForeignKey("workspaces.id", ondelete="CASCADE"), index=True)
    subject_entity_id: Mapped[str] = mapped_column(ForeignKey("entities.id", ondelete="CASCADE"), index=True)
    predicate: Mapped[str] = mapped_column(String(160))
    object_value: Mapped[str] = mapped_column(Text)
    normalized_property: Mapped[str] = mapped_column(String(160), index=True)
    extraction_confidence: Mapped[float] = mapped_column(Float)
    observed_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), index=True)
    evidence: Mapped[list[dict[str, Any]]] = mapped_column(JSON, default=list)


class TemporalRelationshipRow(Base):
    __tablename__ = "temporal_relationships"
    __table_args__ = (Index("ix_relationship_active", "workspace_id", "valid_from", "valid_to"),)
    id: Mapped[str] = mapped_column(String(96), primary_key=True)
    workspace_id: Mapped[str] = mapped_column(ForeignKey("workspaces.id", ondelete="CASCADE"), index=True)
    source_entity_id: Mapped[str] = mapped_column(ForeignKey("entities.id", ondelete="CASCADE"), index=True)
    relationship_type: Mapped[str] = mapped_column(String(100), index=True)
    target_entity_id: Mapped[str] = mapped_column(ForeignKey("entities.id", ondelete="CASCADE"), index=True)
    valid_from: Mapped[datetime] = mapped_column(DateTime(timezone=True), index=True)
    valid_to: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True, index=True)
    source_count: Mapped[int] = mapped_column(Integer)
    confidence: Mapped[float] = mapped_column(Float)
    strength: Mapped[float] = mapped_column(Float, default=1)
    evidence_ids: Mapped[list[str]] = mapped_column(JSON, default=list)


class SignalRow(Base):
    __tablename__ = "signals"
    id: Mapped[str] = mapped_column(String(96), primary_key=True)
    workspace_id: Mapped[str] = mapped_column(ForeignKey("workspaces.id", ondelete="CASCADE"), index=True)
    signal_type: Mapped[str] = mapped_column(String(80), index=True)
    title: Mapped[str] = mapped_column(Text)
    detected_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), index=True)
    confidence: Mapped[float] = mapped_column(Float)
    severity: Mapped[str] = mapped_column(String(24), index=True)
    metrics: Mapped[dict[str, Any]] = mapped_column(JSON, default=dict)
    deterministic_basis: Mapped[str] = mapped_column(Text)
    evidence_ids: Mapped[list[str]] = mapped_column(JSON, default=list)
