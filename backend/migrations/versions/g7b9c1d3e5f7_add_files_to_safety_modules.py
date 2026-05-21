"""add files column to safety_modules

Revision ID: g7b9c1d3e5f7
Revises: f6a8b0c2d4e6
Create Date: 2026-05-20

"""
from alembic import op
import sqlalchemy as sa

revision = 'g7b9c1d3e5f7'
down_revision = 'f6a8b0c2d4e6'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('safety_modules', sa.Column('files', sa.Text(), nullable=True))


def downgrade():
    op.drop_column('safety_modules', 'files')
