"""add jenis_inspeksi to inspectionk3l

Revision ID: j0e2f4a6b8c0
Revises: i9d1e3f5a7b9
Create Date: 2026-06-04

"""
from alembic import op
import sqlalchemy as sa

revision = 'j0e2f4a6b8c0'
down_revision = 'i9d1e3f5a7b9'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column(
        'reports_inspectionk3l',
        sa.Column('jenis_inspeksi', sa.String(50), nullable=True)
    )


def downgrade():
    op.drop_column('reports_inspectionk3l', 'jenis_inspeksi')
