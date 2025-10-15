"""merge migration heads

Revision ID: 27adbd86857b
Revises: 5cef832932b3, c67085d9fbd1
Create Date: 2025-06-30 10:54:59.740563

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '27adbd86857b'
down_revision: Union[str, None] = ('5cef832932b3', 'c67085d9fbd1')
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
