"""add department_id to users

Revision ID: k1f3a5b7c9d1
Revises: j0e2f4a6b8c0
Create Date: 2026-06-04

"""
from alembic import op
import sqlalchemy as sa

revision = 'k1f3a5b7c9d1'
down_revision = 'j0e2f4a6b8c0'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column(
        'users',
        sa.Column('department_id', sa.Integer, sa.ForeignKey('departments.id'), nullable=True)
    )


def downgrade():
    op.drop_column('users', 'department_id')
