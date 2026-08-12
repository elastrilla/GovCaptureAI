"""Add company profile fields

Revision ID: 7a2d3c4b5e6f
Revises: e5a135a253bb
Create Date: 2026-07-06 10:45:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "7a2d3c4b5e6f"
down_revision: Union[str, Sequence[str], None] = "e5a135a253bb"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column("companies", sa.Column("core_capabilities", sa.Text(), nullable=True))
    op.add_column("companies", sa.Column("differentiators", sa.Text(), nullable=True))
    op.add_column("companies", sa.Column("certifications", sa.Text(), nullable=True))
    op.add_column("companies", sa.Column("target_naics_codes", sa.String(length=255), nullable=True))
    op.add_column("companies", sa.Column("target_agencies", sa.Text(), nullable=True))
    op.add_column("companies", sa.Column("past_performance_summary", sa.Text(), nullable=True))


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_column("companies", "past_performance_summary")
    op.drop_column("companies", "target_agencies")
    op.drop_column("companies", "target_naics_codes")
    op.drop_column("companies", "certifications")
    op.drop_column("companies", "differentiators")
    op.drop_column("companies", "core_capabilities")
