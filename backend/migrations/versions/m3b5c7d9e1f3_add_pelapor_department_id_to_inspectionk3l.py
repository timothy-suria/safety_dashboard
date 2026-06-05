"""add pelapor_department_id to inspectionk3l

Revision ID: m3b5c7d9e1f3
Revises: l2a4b6c8d0e2
Create Date: 2026-06-04

"""
from alembic import op
import sqlalchemy as sa

revision = 'm3b5c7d9e1f3'
down_revision = 'l2a4b6c8d0e2'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column(
        'reports_inspectionk3l',
        sa.Column('pelapor_department_id', sa.Integer, sa.ForeignKey('departments.id'), nullable=True)
    )


def downgrade():
    op.drop_column('reports_inspectionk3l', 'pelapor_department_id')
