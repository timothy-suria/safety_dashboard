"""widen foto_sebelum and foto_sesudah to Text

Revision ID: o5d7e9f1a3b5
Revises: n4c6d8e0f2a4
Create Date: 2026-06-05

"""
from alembic import op
import sqlalchemy as sa

revision = 'o5d7e9f1a3b5'
down_revision = 'n4c6d8e0f2a4'
branch_labels = None
depends_on = None


def upgrade():
    op.alter_column('reports_inspectionk3l', 'foto_sebelum',
                    existing_type=sa.String(500), type_=sa.Text, existing_nullable=True)
    op.alter_column('reports_inspectionk3l', 'foto_sesudah',
                    existing_type=sa.String(500), type_=sa.Text, existing_nullable=True)


def downgrade():
    op.alter_column('reports_inspectionk3l', 'foto_sebelum',
                    existing_type=sa.Text, type_=sa.String(500), existing_nullable=True)
    op.alter_column('reports_inspectionk3l', 'foto_sesudah',
                    existing_type=sa.Text, type_=sa.String(500), existing_nullable=True)
