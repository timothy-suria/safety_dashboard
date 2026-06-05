"""add tindak lanjut history table

Revision ID: q7f9a1b3c5d7
Revises: p6e8f0a2b4c6
Create Date: 2026-06-05

"""
from alembic import op
import sqlalchemy as sa

revision = 'q7f9a1b3c5d7'
down_revision = 'p6e8f0a2b4c6'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'inspection_k3l_tindak_lanjut_history',
        sa.Column('id', sa.Integer, primary_key=True, autoincrement=True),
        sa.Column('inspection_id', sa.Integer, sa.ForeignKey('reports_inspectionk3l.id', ondelete='CASCADE'), nullable=False, index=True),
        sa.Column('round_number', sa.Integer, nullable=False),
        sa.Column('tindakan_perbaikan', sa.Text, nullable=True),
        sa.Column('foto_sesudah', sa.Text, nullable=True),
        sa.Column('ditindaklanjuti_oleh', sa.String(100), nullable=True),
        sa.Column('ditindaklanjuti_department_id', sa.Integer, sa.ForeignKey('departments.id'), nullable=True),
        sa.Column('tanggal_tindaklanjuti', sa.DateTime, nullable=True),
        sa.Column('created_at', sa.DateTime, server_default=sa.func.current_timestamp()),
    )

    # Migrate existing tindak lanjut data from main table as round 1
    op.execute("""
        INSERT INTO inspection_k3l_tindak_lanjut_history
            (inspection_id, round_number, tindakan_perbaikan, foto_sesudah,
             ditindaklanjuti_oleh, ditindaklanjuti_department_id, tanggal_tindaklanjuti, created_at)
        SELECT
            id, 1, tindakan_perbaikan, NULL,
            ditindaklanjuti_oleh, ditindaklanjuti_department_id,
            tanggal_tindaklanjuti,
            COALESCE(tanggal_tindaklanjuti, NOW())
        FROM reports_inspectionk3l
        WHERE tindakan_perbaikan IS NOT NULL
    """)


def downgrade():
    op.drop_table('inspection_k3l_tindak_lanjut_history')
