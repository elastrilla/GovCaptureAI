"""Backfill notice type on opportunities

Revision ID: b7c8d9e0f1a2
Revises: a2f4c6d8e0b1
Create Date: 2026-07-07 10:45:00.000000

"""
from typing import Sequence, Union

from alembic import op


# revision identifiers, used by Alembic.
revision: str = "b7c8d9e0f1a2"
down_revision: Union[str, Sequence[str], None] = "a2f4c6d8e0b1"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Backfill obvious notice types from existing solicitation/title text."""
    op.execute(
        """
        UPDATE opportunities
        SET notice_type = CASE
            WHEN concat_ws(' ', solicitation_number, title, description, sam_notice_id)
                ~* '(^|[^A-Z0-9])SOURCE[S]?[[:space:]-]+SOUGHT([^A-Z0-9]|$)'
                THEN 'Sources Sought'
            WHEN concat_ws(' ', solicitation_number, title, description, sam_notice_id)
                ~* '(^|[^A-Z0-9])RFI([^A-Z0-9]|$)'
                THEN 'RFI'
            WHEN concat_ws(' ', solicitation_number, title, description, sam_notice_id)
                ~* '(^|[^A-Z0-9])RFQ([^A-Z0-9]|$)'
                THEN 'RFQ'
            WHEN concat_ws(' ', solicitation_number, title, description, sam_notice_id)
                ~* '(^|[^A-Z0-9])RFP([^A-Z0-9]|$)'
                THEN 'RFP'
            ELSE notice_type
        END
        WHERE notice_type IS NULL OR btrim(notice_type) = ''
        """
    )


def downgrade() -> None:
    """No-op: keep backfilled notice labels if this data migration is downgraded."""
    pass
