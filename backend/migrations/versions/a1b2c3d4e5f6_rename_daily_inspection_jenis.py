"""rename Daily Inspection jenis_inspeksi value to Inspeksi Harian

Revision ID: a1b2c3d4e5f6
Revises: 998d5efb1fa2
Create Date: 2026-06-15

"""
from alembic import op
import sqlalchemy as sa

revision = 'a1b2c3d4e5f6'
down_revision = '998d5efb1fa2'
branch_labels = None
depends_on = None


def upgrade():
    op.execute(
        "UPDATE reports_inspectionk3l SET jenis_inspeksi = 'Inspeksi Harian' "
        "WHERE jenis_inspeksi = 'Daily Inspection'"
    )


def downgrade():
    op.execute(
        "UPDATE reports_inspectionk3l SET jenis_inspeksi = 'Daily Inspection' "
        "WHERE jenis_inspeksi = 'Inspeksi Harian'"
    )
