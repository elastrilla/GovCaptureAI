"""Add pilot document file storage

Revision ID: e0f1a2b3c4d5
Revises: d9e0f1a2b3c4
"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = "e0f1a2b3c4d5"
down_revision: Union[str, Sequence[str], None] = "d9e0f1a2b3c4"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column("documents", sa.Column("mime_type", sa.String(length=120), nullable=True))
    op.add_column("documents", sa.Column("file_size", sa.Integer(), nullable=True))
    op.add_column("documents", sa.Column("file_data", sa.Text(), nullable=True))


def downgrade() -> None:
    op.drop_column("documents", "file_data")
    op.drop_column("documents", "file_size")
    op.drop_column("documents", "mime_type")
