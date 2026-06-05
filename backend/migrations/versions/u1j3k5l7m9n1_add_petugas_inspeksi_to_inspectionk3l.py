"""add petugas_inspeksi to inspectionk3l

Revision ID: u1j3k5l7m9n1
Revises: t0i2j4k6l8m0
Create Date: 2026-06-05

"""
from alembic import op
import sqlalchemy as sa

revision = 'u1j3k5l7m9n1'
down_revision = 't0i2j4k6l8m0'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('reports_inspectionk3l',
        sa.Column('petugas_inspeksi', sa.Text, nullable=True)
    )


def downgrade():
    op.drop_column('reports_inspectionk3l', 'petugas_inspeksi')
