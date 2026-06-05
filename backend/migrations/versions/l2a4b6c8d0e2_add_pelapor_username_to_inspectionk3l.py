"""add pelapor_username to inspectionk3l

Revision ID: l2a4b6c8d0e2
Revises: k1f3a5b7c9d1
Create Date: 2026-06-04

"""
from alembic import op
import sqlalchemy as sa

revision = 'l2a4b6c8d0e2'
down_revision = 'k1f3a5b7c9d1'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column(
        'reports_inspectionk3l',
        sa.Column('pelapor_username', sa.String(100), nullable=True)
    )


def downgrade():
    op.drop_column('reports_inspectionk3l', 'pelapor_username')
