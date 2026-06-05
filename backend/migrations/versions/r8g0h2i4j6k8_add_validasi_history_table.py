"""add validasi history table

Revision ID: r8g0h2i4j6k8
Revises: q7f9a1b3c5d7
Create Date: 2026-06-05

"""
from alembic import op
import sqlalchemy as sa

revision = 'r8g0h2i4j6k8'
down_revision = 'q7f9a1b3c5d7'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'inspection_k3l_validasi_history',
        sa.Column('id', sa.Integer, primary_key=True, autoincrement=True),
        sa.Column('inspection_id', sa.Integer, sa.ForeignKey('reports_inspectionk3l.id', ondelete='CASCADE'), nullable=False, index=True),
        sa.Column('round_number', sa.Integer, nullable=False),
        sa.Column('divalidasi_oleh', sa.String(100), nullable=True),
        sa.Column('divalidasi_department_id', sa.Integer, sa.ForeignKey('departments.id'), nullable=True),
        sa.Column('tanggal_validasi', sa.DateTime, nullable=True),
        sa.Column('alasan_validasi', sa.Text, nullable=True),
        sa.Column('status_validasi', sa.String(20), nullable=True),
        sa.Column('created_at', sa.DateTime, server_default=sa.func.current_timestamp()),
    )

    # Migrate existing validasi data from main table as round 1
    op.execute("""
        INSERT INTO inspection_k3l_validasi_history
            (inspection_id, round_number, divalidasi_oleh, divalidasi_department_id,
             tanggal_validasi, alasan_validasi, status_validasi, created_at)
        SELECT
            id, 1, divalidasi_oleh, divalidasi_department_id,
            tanggal_validasi, alasan_validasi, status_validasi,
            COALESCE(tanggal_validasi, NOW())
        FROM reports_inspectionk3l
        WHERE divalidasi_oleh IS NOT NULL
    """)


def downgrade():
    op.drop_table('inspection_k3l_validasi_history')
