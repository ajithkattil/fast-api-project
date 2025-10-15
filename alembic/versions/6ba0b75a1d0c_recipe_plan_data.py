"""recipe plan data

Revision ID: 6ba0b75a1d0c
Revises: f229c37e80b2
Create Date: 2025-06-10 16:00:39.882546

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.sql import table, column


# revision identifiers, used by Alembic.
revision: str = '6ba0b75a1d0c'
down_revision: Union[str, None] = 'f229c37e80b2'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


partner_recipe_plans = table(
    "partner_recipe_plans",
    column("partner_recipe_plan_id", sa.Integer),
    column("partner_id", sa.String(8)),
    column("plan_name", sa.String),
)

recipe_plan_data_sources = table(
    "recipe_plan_data_sources",
    column("partner_recipe_plan_id", sa.Integer),
    column("cabinet_plan_id", sa.Integer),
)


def upgrade() -> None:
    op.bulk_insert(
        partner_recipe_plans,
        [
            {
                "partner_recipe_plan_id": 1,
                "partner_id": "BA-MAIN",
                "plan_name": "2-Person",
            },
            {
                "partner_recipe_plan_id": 2,
                "partner_id": "BA-MAIN",
                "plan_name": "Family",
            },
            {
                "partner_recipe_plan_id": 3,
                "partner_id": "BA-MAIN",
                "plan_name": "Add-ons",
            },
            {
                "partner_recipe_plan_id": 4,
                "partner_id": "BA-MAIN",
                "plan_name": "Prepped and Ready",
            },
            {
                "partner_recipe_plan_id": 5,
                "partner_id": "BA-MAIN",
                "plan_name": "Meal Prep",
            },
        ],
    )
    
    op.bulk_insert(
        recipe_plan_data_sources,
        [
            {"partner_recipe_plan_id": 1, "cabinet_plan_id": 1},
            {"partner_recipe_plan_id": 2, "cabinet_plan_id": 3},
            {"partner_recipe_plan_id": 3, "cabinet_plan_id": 8},
            {"partner_recipe_plan_id": 4, "cabinet_plan_id": 12},
            {"partner_recipe_plan_id": 5, "cabinet_plan_id": 7},
        ],
    )

def downgrade() -> None:
    op.execute(
        "DELETE FROM recipe_plan_data_sources WHERE partner_recipe_plan_id IN (1, 2, 3, 4, 5)"
    )
    op.execute(
        "DELETE FROM partner_recipe_plans WHERE partner_recipe_plan_id IN (1, 2, 3, 4, 5) AND partner_id = 'BA-MAIN'"
    )
