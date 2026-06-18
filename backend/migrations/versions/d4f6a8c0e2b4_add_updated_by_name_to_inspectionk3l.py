"""add updated_by_name to reports_inspectionk3l

Revision ID: d4f6a8c0e2b4
Revises: 50c40a3d3b3b
Create Date: 2026-06-18

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'd4f6a8c0e2b4'
down_revision: Union[str, Sequence[str], None] = '50c40a3d3b3b'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column(
        'reports_inspectionk3l',
        sa.Column('updated_by_name', sa.String(length=100), nullable=True),
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_column('reports_inspectionk3l', 'updated_by_name')
