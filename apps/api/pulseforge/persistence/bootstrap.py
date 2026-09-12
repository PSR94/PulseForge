from __future__ import annotations

from datetime import UTC, datetime

from sqlalchemy import select

from pulseforge.persistence.database import get_engine, session_scope
from pulseforge.persistence.schema import Base, WorkspaceRow


def create_schema() -> None:
    Base.metadata.create_all(get_engine())


def ensure_demo_workspace() -> None:
    with session_scope() as session:
        if session.scalar(select(WorkspaceRow).where(WorkspaceRow.id == "ai-industry")):
            return
        now = datetime.now(UTC)
        session.add(
            WorkspaceRow(
                id="ai-industry",
                name="AI Industry Intelligence",
                description="Deterministic public-safe demonstration workspace.",
                created_at=now,
                updated_at=now,
            )
        )
