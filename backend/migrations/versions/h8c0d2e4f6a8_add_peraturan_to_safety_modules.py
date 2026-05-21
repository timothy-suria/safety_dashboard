"""add peraturan to safety_modules

Revision ID: h8c0d2e4f6a8
Revises: g7b9c1d3e5f7
Create Date: 2026-05-21

"""
from alembic import op
import sqlalchemy as sa

revision = 'h8c0d2e4f6a8'
down_revision = 'g7b9c1d3e5f7'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('safety_modules', sa.Column('peraturan', sa.String(100), nullable=True))


def downgrade():
    op.drop_column('safety_modules', 'peraturan')
