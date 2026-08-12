"""Add notice type to opportunities

Revision ID: a2f4c6d8e0b1
Revises: 9c8b7a6d5e4f
Create Date: 2026-07-07 10:30:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "a2f4c6d8e0b1"
down_revision: Union[str, Sequence[str], None] = "9c8b7a6d5e4f"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column(
        "opportunities",
        sa.Column("notice_type", sa.String(length=100), nullable=True),
    )
    op.create_index(op.f("ix_opportunities_notice_type"), "opportunities", ["notice_type"], unique=False)


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_index(op.f("ix_opportunities_notice_type"), table_name="opportunities")
    op.drop_column("opportunities", "notice_type")
