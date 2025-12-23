"""add registration contact fields

Revision ID: 1a6f0b7f8e2c
Revises: e4b6f1d9b2a7
Create Date: 2025-12-22 21:05:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "1a6f0b7f8e2c"
down_revision: Union[str, Sequence[str], None] = "e4b6f1d9b2a7"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column(
        "event_registrations",
        sa.Column(
            "contact_email",
            sa.String(length=320),
            nullable=False,
            server_default="",
        ),
    )
    op.add_column(
        "event_registrations",
        sa.Column(
            "contact_phone",
            sa.String(length=32),
            nullable=False,
            server_default="",
        ),
    )
    op.alter_column("event_registrations", "contact_email", server_default=None)
    op.alter_column("event_registrations", "contact_phone", server_default=None)


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_column("event_registrations", "contact_phone")
    op.drop_column("event_registrations", "contact_email")
