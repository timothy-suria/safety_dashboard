"""add business_unit_id and plant_id to report_case_incidents

Revision ID: z6o8p0q2r4s6
Revises: y5n7o9p1q3r5
Create Date: 2026-06-08

"""
from alembic import op
import sqlalchemy as sa

revision = 'z6o8p0q2r4s6'
down_revision = 'y5n7o9p1q3r5'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('report_case_incidents', sa.Column('business_unit_id', sa.Integer(), nullable=True))
    op.add_column('report_case_incidents', sa.Column('plant_id', sa.Integer(), nullable=True))
    op.create_foreign_key(
        'report_case_incidents_business_unit_id_fkey',
        'report_case_incidents', 'business_units', ['business_unit_id'], ['id'],
    )
    op.create_foreign_key(
        'report_case_incidents_plant_id_fkey',
        'report_case_incidents', 'plants', ['plant_id'], ['id'],
    )


def downgrade():
    op.drop_constraint('report_case_incidents_plant_id_fkey', 'report_case_incidents', type_='foreignkey')
    op.drop_constraint('report_case_incidents_business_unit_id_fkey', 'report_case_incidents', type_='foreignkey')
    op.drop_column('report_case_incidents', 'plant_id')
    op.drop_column('report_case_incidents', 'business_unit_id')
