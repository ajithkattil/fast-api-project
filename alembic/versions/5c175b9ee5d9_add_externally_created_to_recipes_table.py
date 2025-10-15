"""add externally_created to recipes table

Revision ID: 5c175b9ee5d9
Revises: ed6ea01230ed
Create Date: 2025-09-18 15:26:07.570435

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = '5c175b9ee5d9'
down_revision: Union[str, None] = 'ed6ea01230ed'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('recipes', sa.Column("externally_created", sa.Boolean(), nullable=False, server_default=sa.false()),)


def downgrade() -> None:
    op.drop_column('recipes', 'externally_created')
