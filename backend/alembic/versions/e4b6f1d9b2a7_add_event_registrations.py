"""add event registrations

Revision ID: e4b6f1d9b2a7
Revises: dce62fd7ee2b
Create Date: 2025-12-22 20:25:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql


# revision identifiers, used by Alembic.
revision: str = "e4b6f1d9b2a7"
down_revision: Union[str, Sequence[str], None] = "dce62fd7ee2b"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


registration_type_enum = postgresql.ENUM("USER", "TEAM", name="registration_type", create_type=False)


def upgrade() -> None:
    """Upgrade schema."""
    bind = op.get_bind()
    registration_type_enum.create(bind, checkfirst=True)

    op.create_table(
        "event_registrations",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("event_id", sa.Integer(), nullable=False),
        sa.Column("registered_by_user_id", sa.Integer(), nullable=False),
        sa.Column("type", registration_type_enum, nullable=False),
        sa.Column("team_name", sa.String(length=255), nullable=True),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.ForeignKeyConstraint(["event_id"], ["events.id"]),
        sa.ForeignKeyConstraint(["registered_by_user_id"], ["users.id"]),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint(
            "event_id",
            "registered_by_user_id",
            name="uq_event_registrations_event_user",
        ),
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table("event_registrations")
    bind = op.get_bind()
    registration_type_enum.drop(bind, checkfirst=True)
