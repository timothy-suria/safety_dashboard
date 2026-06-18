"""add updated_by_name to reports_hse_daily and report_case_incidents

Revision ID: e6a8c0e2b4d6
Revises: d4f6a8c0e2b4
Create Date: 2026-06-18

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'e6a8c0e2b4d6'
down_revision: Union[str, Sequence[str], None] = 'd4f6a8c0e2b4'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column(
        'reports_hse_daily',
        sa.Column('updated_by_name', sa.String(length=100), nullable=True),
    )
    op.add_column(
        'report_case_incidents',
        sa.Column('updated_by_name', sa.String(length=100), nullable=True),
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_column('report_case_incidents', 'updated_by_name')
    op.drop_column('reports_hse_daily', 'updated_by_name')
