"""merge chat-attachments and safety-modules branches

Revision ID: c1e3f5a7b9d2
Revises: b9d2f4a6c8e0, h8c0d2e4f6a8
Create Date: 2026-05-21 03:00:00.000000

"""
from typing import Sequence, Union

# revision identifiers, used by Alembic.
revision: str = 'c1e3f5a7b9d2'
down_revision: Union[str, Sequence[str], None] = ('b9d2f4a6c8e0', 'h8c0d2e4f6a8')
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
