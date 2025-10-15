"""add brands to partners

Revision ID: 5cef832932b3
Revises: 3c37170e422f
Create Date: 2025-06-06 13:00:00.687603

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = '5cef832932b3'
down_revision: Union[str, None] = '3c37170e422f'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table('brand',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('partner_id', sa.String(length=8), nullable=False),
    sa.Column('name', sa.String(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    sa.ForeignKeyConstraint(['partner_id'], ['partners.partner_id'], ),

    op.add_column('pantry_items', sa.Column('brand_name', sa.String(), nullable=True))

def downgrade() -> None:
    op.drop_column('pantry_item', 'brand_name')
    op.drop_table('brand')
