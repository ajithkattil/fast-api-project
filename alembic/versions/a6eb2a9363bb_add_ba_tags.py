"""add BA tags

Revision ID: a6eb2a9363bb
Revises: c7ee01ead83d
Create Date: 2025-06-09 18:34:40.223796

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy import MetaData, Table


# revision identifiers, used by Alembic.
revision: str = 'a6eb2a9363bb'
down_revision: Union[str, None] = 'c7ee01ead83d'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    conn = op.get_bind()
    metadata = MetaData()
    partner_packaging_configuration_tags = Table(
        "partner_packaging_configuration_tags",
        metadata,
        autoload_with=conn
    )
   
    conn.execute(
        partner_packaging_configuration_tags.insert(),
        [
            {
                "tag_id": "heatAndEat",
                "culops_tag_type": "campaign_tag_list",
                "partner_id": "BA-MAIN",
                "culops_tag_value": "Heat & Eat"
            },
            {
                "tag_id": "preparedAndReady",
                "culops_tag_type": "campaign_tag_list",
                "partner_id": "BA-MAIN",
                "culops_tag_value": "Prepared And Ready"
            },
            {
                "tag_id": "lobsterBox",
                "culops_tag_type": "campaign_tag_list",
                "partner_id": "BA-MAIN",
                "culops_tag_value": "Lobster Box"
            },
            {
                "tag_id": "tailgatingBox",
                "culops_tag_type": "campaign_tag_list",
                "partner_id": "BA-MAIN",
                "culops_tag_value": "Tailgating Box"
            },
            {
                "tag_id": "thanksgiving",
                "culops_tag_type": "campaign_tag_list",
                "partner_id": "BA-MAIN",
                "culops_tag_value": "Thanksgiving"
            },
            {
                "tag_id": "holidayHam",
                "culops_tag_type": "campaign_tag_list",
                "partner_id": "BA-MAIN",
                "culops_tag_value": "Holiday Ham"
            },
            {
                "tag_id": "familyStyle",
                "culops_tag_type": "campaign_tag_list",
                "partner_id": "BA-MAIN",
                "culops_tag_value": "Family Style"
            },

        ]
    )
    
    partner_recipe_constraint_tags = Table(
        "partner_recipe_constraint_tags",
        metadata,
        autoload_with=conn
    )
    
    conn.execute(
        partner_recipe_constraint_tags.insert(),
        [
            {
                "tag_id": "600CaloriesOrLess",
                "culops_tag_type": "badge_tag_list",
                "partner_id": "BA-MAIN",
                "culops_tag_value": "600 Calories Or Less"
            },
            {
                "tag_id": "carbConscious",
                "culops_tag_type": "badge_tag_list",
                "partner_id": "BA-MAIN",
                "culops_tag_value": "Carb Conscious"
            },
            {
                "tag_id": "wheatFree",
                "culops_tag_type": "badge_tag_list",
                "partner_id": "BA-MAIN",
                "culops_tag_value": "Wheat Free"
            },
            {
                "tag_id": "vegetarian",
                "culops_tag_type": "badge_tag_list",
                "partner_id": "BA-MAIN",
                "culops_tag_value": "Vegetarian"
            },
            {
                "tag_id": "30gOfProtein",
                "culops_tag_type": "badge_tag_list",
                "partner_id": "BA-MAIN",
                "culops_tag_value": "30g Of Protein"
            },
            {
                "tag_id": "45gOfProtein",
                "culops_tag_type": "badge_tag_list",
                "partner_id": "BA-MAIN",
                "culops_tag_value": "45g Of Protein"
            },
            {
                "tag_id": "makeItVegetarian",
                "culops_tag_type": "campaign_tag_list",
                "partner_id": "BA-MAIN",
                "culops_tag_value": "Make It Vegetarian"
            },
            {
                "tag_id": "gameDay",
                "culops_tag_type": "campaign_tag_list",
                "partner_id": "BA-MAIN",
                "culops_tag_value": "Game Day"
            },
            {
                "tag_id": "laborDay",
                "culops_tag_type": "campaign_tag_list",
                "partner_id": "BA-MAIN",
                "culops_tag_value": "Labor Day"
            },
            {
                "tag_id": "mothersDay",
                "culops_tag_type": "campaign_tag_list",
                "partner_id": "BA-MAIN",
                "culops_tag_value": "Mother's Day"
            },
            {
                "tag_id": "memorialDay",
                "culops_tag_type": "campaign_tag_list",
                "partner_id": "BA-MAIN",
                "culops_tag_value": "Memorial Day"
            },
            {
                "tag_id": "newYears",
                "culops_tag_type": "campaign_tag_list",
                "partner_id": "BA-MAIN",
                "culops_tag_value": "New Years"
            },
            {
                "tag_id": "july4th",
                "culops_tag_type": "campaign_tag_list",
                "partner_id": "BA-MAIN",
                "culops_tag_value": "July 4th"
            },
            {
                "tag_id": "valentinesDay",
                "culops_tag_type": "campaign_tag_list",
                "partner_id": "BA-MAIN",
                "culops_tag_value": "Valentine's Day"
            },
            {
                "tag_id": "craftGameDay",
                "culops_tag_type": "campaign_tag_list",
                "partner_id": "BA-MAIN",
                "culops_tag_value": "Craft Game Day"
            },
            {
                "tag_id": "craftLaborDay",
                "culops_tag_type": "campaign_tag_list",
                "partner_id": "BA-MAIN",
                "culops_tag_value": "Craft Labor Day"
            },
            {
                "tag_id": "craftMothersDay",
                "culops_tag_type": "campaign_tag_list",
                "partner_id": "BA-MAIN",
                "culops_tag_value": "Craft Mother's Day"
            },
            {
                "tag_id": "craftMemorialDay",
                "culops_tag_type": "campaign_tag_list",
                "partner_id": "BA-MAIN",
                "culops_tag_value": "Craft Memorial Day"
            },
            {
                "tag_id": "craftNewYears",
                "culops_tag_type": "campaign_tag_list",
                "partner_id": "BA-MAIN",
                "culops_tag_value": "Craft New Years"
            },
            {
                "tag_id": "craftJuly4th",
                "culops_tag_type": "campaign_tag_list",
                "partner_id": "BA-MAIN",
                "culops_tag_value": "Craft July 4th"
            },
            {
                "tag_id": "craftValentinesDay",
                "culops_tag_type": "campaign_tag_list",
                "partner_id": "BA-MAIN",
                "culops_tag_value": "Craft Valentine's Day"
            },
            {
                "tag_id": "premiumGameDay",
                "culops_tag_type": "campaign_tag_list",
                "partner_id": "BA-MAIN",
                "culops_tag_value": "Premium Game Day"
            },
            {
                "tag_id": "premiumLaborDay",
                "culops_tag_type": "campaign_tag_list",
                "partner_id": "BA-MAIN",
                "culops_tag_value": "Premium Labor Day"
            },
            {
                "tag_id": "premiumMothersDay",
                "culops_tag_type": "campaign_tag_list",
                "partner_id": "BA-MAIN",
                "culops_tag_value": "Premium Mother's Day"
            },
            {
                "tag_id": "premiumMemorialDay",
                "culops_tag_type": "campaign_tag_list",
                "partner_id": "BA-MAIN",
                "culops_tag_value": "Premium Memorial Day"
            },
            {
                "tag_id": "premiumNewYears",
                "culops_tag_type": "campaign_tag_list",
                "partner_id": "BA-MAIN",
                "culops_tag_value": "Premium New Years"
            },
            {
                "tag_id": "premiumJuly4th",
                "culops_tag_type": "campaign_tag_list",
                "partner_id": "BA-MAIN",
                "culops_tag_value": "Premium July 4th"
            },
            {
                "tag_id": "premiumValentinesDay",
                "culops_tag_type": "campaign_tag_list",
                "partner_id": "BA-MAIN",
                "culops_tag_value": "Premium Valentine's Day"
            },
        ]
    )
    
def downgrade() -> None:
    op.execute(
        "DELETE FROM partner_packaging_configuration_tags WHERE partner_id = 'BA-MAIN'"
    )

    op.execute(
        "DELETE FROM partner_recipe_constraint_tags WHERE partner_id = 'BA-MAIN'"
    )