"""Add qualification recommendation to opportunities

Revision ID: 9c8b7a6d5e4f
Revises: 8b7c6d5e4f3a
Create Date: 2026-07-07 09:45:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "9c8b7a6d5e4f"
down_revision: Union[str, Sequence[str], None] = "8b7c6d5e4f3a"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column(
        "opportunities",
        sa.Column("qualification_recommendation", sa.String(length=50), nullable=True),
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_column("opportunities", "qualification_recommendation")
