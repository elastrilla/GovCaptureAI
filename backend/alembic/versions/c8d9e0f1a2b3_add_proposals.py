"""Add proposals

Revision ID: c8d9e0f1a2b3
Revises: b7c8d9e0f1a2
Create Date: 2026-07-07 19:45:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "c8d9e0f1a2b3"
down_revision: Union[str, Sequence[str], None] = "b7c8d9e0f1a2"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table(
        "proposals",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("opportunity_id", sa.Integer(), nullable=False),
        sa.Column("company_id", sa.Integer(), nullable=False),
        sa.Column("title", sa.String(length=500), nullable=False),
        sa.Column("draft_text", sa.Text(), nullable=False),
        sa.Column("review_status", sa.String(length=50), nullable=False),
        sa.Column("readiness_score", sa.Integer(), nullable=False),
        sa.Column("review_notes", sa.Text(), nullable=True),
        sa.Column("compliance_notes", sa.Text(), nullable=True),
        sa.Column("review_gaps", sa.Text(), nullable=True),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("updated_at", sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(["company_id"], ["companies.id"]),
        sa.ForeignKeyConstraint(["opportunity_id"], ["opportunities.id"]),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_proposals_id"), "proposals", ["id"], unique=False)
    op.create_index(op.f("ix_proposals_opportunity_id"), "proposals", ["opportunity_id"], unique=False)
    op.create_index(op.f("ix_proposals_company_id"), "proposals", ["company_id"], unique=False)
    op.create_index(op.f("ix_proposals_review_status"), "proposals", ["review_status"], unique=False)


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_index(op.f("ix_proposals_review_status"), table_name="proposals")
    op.drop_index(op.f("ix_proposals_company_id"), table_name="proposals")
    op.drop_index(op.f("ix_proposals_opportunity_id"), table_name="proposals")
    op.drop_index(op.f("ix_proposals_id"), table_name="proposals")
    op.drop_table("proposals")
