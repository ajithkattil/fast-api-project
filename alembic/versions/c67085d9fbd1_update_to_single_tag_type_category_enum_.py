"""update to single tag type category enum type

Revision ID: c67085d9fbd1
Revises: 6ba0b75a1d0c
Create Date: 2025-06-11 10:52:20.327456

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = 'c67085d9fbd1'
down_revision: Union[str, None] = '6ba0b75a1d0c'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Create the new unified enum type
    tag_list_enum = sa.Enum('badge_tag_list', 'campaign_tag_list', name='taglisttype')
    tag_list_enum.create(bind=op.get_bind(), checkfirst=True)

    # Update both tag tables to use the new enum type
    op.alter_column('partner_packaging_configuration_tags', 'culops_tag_type',
        existing_type=postgresql.ENUM('badge_tag_list', 'campaign_tag_list', name='partnerpackagingconfigurationtag'),
        type_=sa.Enum('badge_tag_list', 'campaign_tag_list', name='taglisttype'),
        postgresql_using='culops_tag_type::text::taglisttype',
        existing_nullable=False)

    op.alter_column('partner_recipe_constraint_tags', 'culops_tag_type',
        existing_type=postgresql.ENUM('badge_tag_list', 'campaign_tag_list', name='partnerrecipeconstrainttag'),
        type_=sa.Enum('badge_tag_list', 'campaign_tag_list', name='taglisttype'),
        postgresql_using='culops_tag_type::text::taglisttype',
        existing_nullable=False)

    # Drop the old enum types
    sa.Enum(name='partnerpackagingconfigurationtag').drop(op.get_bind(), checkfirst=True)
    sa.Enum(name='partnerrecipeconstrainttag').drop(op.get_bind(), checkfirst=True)


def downgrade() -> None:
    # If downgrading, we need to recreate the old enum types and revert the columns
    partner_packaging_enum = sa.Enum('badge_tag_list', 'campaign_tag_list', name='partnerpackagingconfigurationtag')
    partner_packaging_enum.create(bind=op.get_bind(), checkfirst=True)

    partner_recipe_enum = sa.Enum('badge_tag_list', 'campaign_tag_list', name='partnerrecipeconstrainttag')
    partner_recipe_enum.create(bind=op.get_bind(), checkfirst=True)

    # Revert columns back to old enum types
    op.alter_column('partner_recipe_constraint_tags', 'culops_tag_type',
        existing_type=sa.Enum('badge_tag_list', 'campaign_tag_list', name='taglisttype'),
        type_=partner_recipe_enum,
        postgresql_using='culops_tag_type::text::partnerrecipeconstrainttag',
        existing_nullable=False)

    op.alter_column('partner_packaging_configuration_tags', 'culops_tag_type',
        existing_type=sa.Enum('badge_tag_list', 'campaign_tag_list', name='taglisttype'),
        type_=partner_packaging_enum,
        postgresql_using='culops_tag_type::text::partnerpackagingconfigurationtag',
        existing_nullable=False)

    # Drop the new unified enum type
    sa.Enum(name='taglisttype').drop(op.get_bind(), checkfirst=True)
