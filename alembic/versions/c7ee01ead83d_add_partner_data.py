"""add partner data

Revision ID: c7ee01ead83d
Revises: 493bb38d2ed4
Create Date: 2025-06-09 18:31:28.421916

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.sql import table, column


# revision identifiers, used by Alembic.
revision: str = 'c7ee01ead83d'
down_revision: Union[str, None] = '493bb38d2ed4'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


partners = table('partners',
    column('partner_id', sa.String(length=8)),
    column('name', sa.String()),
    column('recipe_create_cutoff_days', sa.Integer()),
    column('recipe_update_cutoff_days', sa.Integer()),
    column('recipe_delete_cutoff_days', sa.Integer()),
    column('max_assemblies_per_recipe', sa.Integer())
)


def upgrade() -> None:
    op.bulk_insert(
        partners,
        [
            {
                "partner_id": "BA-MAIN", 
                "name": "Blue Apron", 
                "recipe_create_cutoff_days": 42, 
                "recipe_update_cutoff_days": 42, 
                "recipe_delete_cutoff_days": 42, 
                "max_assemblies_per_recipe": 42
            }
        ]
    )


def downgrade() -> None:
    op.execute(
        "DELETE FROM partners WHERE partner_id  = 'BA-MAIN'"
    )
