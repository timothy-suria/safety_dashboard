"""add tindaklanjut fields to inspectionk3l

Revision ID: n4c6d8e0f2a4
Revises: m3b5c7d9e1f3
Create Date: 2026-06-04

"""
from alembic import op
import sqlalchemy as sa

revision = 'n4c6d8e0f2a4'
down_revision = 'm3b5c7d9e1f3'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('reports_inspectionk3l', sa.Column('saran_perbaikan', sa.Text, nullable=True))
    op.add_column('reports_inspectionk3l', sa.Column('ditindaklanjuti_oleh', sa.String(100), nullable=True))
    op.add_column('reports_inspectionk3l', sa.Column('ditindaklanjuti_department_id', sa.Integer, sa.ForeignKey('departments.id'), nullable=True))
    op.add_column('reports_inspectionk3l', sa.Column('tanggal_tindaklanjuti', sa.DateTime, nullable=True))

    # Copy existing tindakan_perbaikan → saran_perbaikan
    op.execute("UPDATE reports_inspectionk3l SET saran_perbaikan = tindakan_perbaikan WHERE tindakan_perbaikan IS NOT NULL")
    op.execute("UPDATE reports_inspectionk3l SET tindakan_perbaikan = NULL")

    # Drop old constraint and add new one with Progress Validasi
    op.drop_constraint('reports_inspectionk3l_status_check', 'reports_inspectionk3l', type_='check')
    op.create_check_constraint(
        'reports_inspectionk3l_status_check',
        'reports_inspectionk3l',
        "status IN ('Open', 'In Progress', 'Closed', 'Progress Validasi')"
    )


def downgrade():
    op.drop_constraint('reports_inspectionk3l_status_check', 'reports_inspectionk3l', type_='check')
    op.create_check_constraint(
        'reports_inspectionk3l_status_check',
        'reports_inspectionk3l',
        "status IN ('Open', 'In Progress', 'Closed')"
    )
    op.drop_column('reports_inspectionk3l', 'saran_perbaikan')
    op.drop_column('reports_inspectionk3l', 'ditindaklanjuti_oleh')
    op.drop_column('reports_inspectionk3l', 'ditindaklanjuti_department_id')
    op.drop_column('reports_inspectionk3l', 'tanggal_tindaklanjuti')
