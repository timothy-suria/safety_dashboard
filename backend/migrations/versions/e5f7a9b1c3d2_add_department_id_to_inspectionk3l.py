"""add_department_id_to_inspectionk3l

Revision ID: e5f7a9b1c3d2
Revises: c3d5e7f9a1b2
Create Date: 2026-05-20 00:00:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = 'e5f7a9b1c3d2'
down_revision: Union[str, Sequence[str], None] = 'c3d5e7f9a1b2'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column(
        'reports_inspectionk3l',
        sa.Column('department_id', sa.Integer(), nullable=True),
    )
    op.create_foreign_key(
        'reports_inspectionk3l_department_id_fkey',
        'reports_inspectionk3l', 'departments',
        ['department_id'], ['id'],
    )


def downgrade() -> None:
    op.drop_constraint(
        'reports_inspectionk3l_department_id_fkey',
        'reports_inspectionk3l',
        type_='foreignkey',
    )
    op.drop_column('reports_inspectionk3l', 'department_id')
