"""Initial PulseForge intelligence schema."""

from alembic import op

from pulseforge.persistence.schema import Base

revision = "20260912_0001"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    Base.metadata.create_all(bind=op.get_bind())


def downgrade() -> None:
    Base.metadata.drop_all(bind=op.get_bind())
