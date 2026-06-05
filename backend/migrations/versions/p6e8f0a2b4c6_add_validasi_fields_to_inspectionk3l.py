"""add validasi fields to inspectionk3l

Revision ID: p6e8f0a2b4c6
Revises: o5d7e9f1a3b5
Create Date: 2026-06-05

"""
from alembic import op
import sqlalchemy as sa

revision = 'p6e8f0a2b4c6'
down_revision = 'o5d7e9f1a3b5'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('reports_inspectionk3l', sa.Column('divalidasi_oleh', sa.String(100), nullable=True))
    op.add_column('reports_inspectionk3l', sa.Column('divalidasi_department_id', sa.Integer, sa.ForeignKey('departments.id'), nullable=True))
    op.add_column('reports_inspectionk3l', sa.Column('tanggal_validasi', sa.DateTime, nullable=True))
    op.add_column('reports_inspectionk3l', sa.Column('alasan_validasi', sa.Text, nullable=True))
    op.add_column('reports_inspectionk3l', sa.Column('status_validasi', sa.String(20), nullable=True))


def downgrade():
    op.drop_column('reports_inspectionk3l', 'divalidasi_oleh')
    op.drop_column('reports_inspectionk3l', 'divalidasi_department_id')
    op.drop_column('reports_inspectionk3l', 'tanggal_validasi')
    op.drop_column('reports_inspectionk3l', 'alasan_validasi')
    op.drop_column('reports_inspectionk3l', 'status_validasi')
