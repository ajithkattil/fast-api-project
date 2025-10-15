import enum

from sqlalchemy import (
    DECIMAL,
    TIMESTAMP,
    BigInteger,
    Boolean,
    Column,
    Enum,
    ForeignKey,
    ForeignKeyConstraint,
    Integer,
    MetaData,
    String,
    Table,
)
from sqlalchemy.dialects.postgresql import UUID

metadata = MetaData()

partners = Table(
    "partners",
    metadata,
    Column("partner_id", String(8), primary_key=True),
    Column("name", String),
    Column("recipe_create_cutoff_days", Integer, nullable=False),
    Column("recipe_update_cutoff_days", Integer, nullable=False),
    Column("recipe_delete_cutoff_days", Integer, nullable=False),
    Column("max_assemblies_per_recipe", Integer, nullable=False),
)

partner_assembly_packaging_options = Table(
    "partner_assembly_packaging_options",
    metadata,
    Column("partner_id", String(8), primary_key=True),
    Column("assembly_packaging_option_id", Integer, primary_key=True),
    ForeignKeyConstraint(["partner_id"], ["partners.partner_id"], ondelete="CASCADE"),
    ForeignKeyConstraint(
        ["assembly_packaging_option_id"],
        ["assembly_packaging_options.assembly_packaging_option_id"],
        ondelete="CASCADE",
    ),
)


class TagListType(enum.StrEnum):
    BADGE_TAG_LIST = "badge_tag_list"
    CAMPAIGN_TAG_LIST = "campaign_tag_list"


partner_packaging_configuration_tags = Table(
    "partner_packaging_configuration_tags",
    metadata,
    Column("tag_id", String, primary_key=True),
    Column(
        "culops_tag_type",
        Enum(TagListType, values_callable=lambda x: [e.value for e in x]),
        primary_key=True,
    ),
    Column("partner_id", String(8), primary_key=True),
    Column("culops_tag_value", String, nullable=False),
    ForeignKeyConstraint(["partner_id"], ["partners.partner_id"], ondelete="CASCADE"),
)


partner_recipe_constraint_tags = Table(
    "partner_recipe_constraint_tags",
    metadata,
    Column("tag_id", String, primary_key=True),
    Column(
        "culops_tag_type",
        Enum(TagListType, values_callable=lambda x: [e.value for e in x]),
        primary_key=True,
    ),
    Column("partner_id", String(8), primary_key=True),
    Column("culops_tag_value", String, nullable=False),
    ForeignKeyConstraint(["partner_id"], ["partners.partner_id"], ondelete="CASCADE"),
)


partner_recipe_plans = Table(
    "partner_recipe_plans",
    metadata,
    Column("partner_recipe_plan_id", Integer, autoincrement=True, primary_key=True),
    Column("partner_id", String(8)),
    Column("plan_name", String, nullable=False),
    ForeignKeyConstraint(["partner_id"], ["partners.partner_id"], ondelete="CASCADE"),
)


assembly_packaging_options = Table(
    "assembly_packaging_options",
    metadata,
    Column("assembly_packaging_option_id", Integer, autoincrement=True, primary_key=True),
    Column("assembly_packaging_option_name", String, nullable=False),
)

cost_markups = Table(
    "cost_markups",
    metadata,
    Column("partner_id", String(8), primary_key=True),
    Column("applied_from", String, primary_key=True, default=""),
    Column("applied_until", String, primary_key=True, default=""),
    Column("markup_percent", DECIMAL(10, 2), nullable=False),
    ForeignKeyConstraint(["partner_id"], ["partners.partner_id"]),
)

pantry_states = Table(
    "pantry_states",
    metadata,
    Column("pantry_state_id", UUID(as_uuid=True), primary_key=True),
    Column("pantry_state_timestamp", TIMESTAMP(timezone=True), nullable=False),
    Column("partner_id", String(8), ForeignKey("partners.partner_id"), nullable=False),
    Column("items_available_from", TIMESTAMP(timezone=True)),
    Column("items_available_until", TIMESTAMP(timezone=True)),
)

pantry_items = Table(
    "pantry_items",
    metadata,
    Column("pantry_item_id", UUID(as_uuid=True), primary_key=True),
    Column("pantry_state_id", UUID(as_uuid=True), nullable=False, index=True),
    Column("description", String),
    Column("units", String, nullable=False),
    Column("amount", DECIMAL(10, 2), nullable=False),
    Column("is_prepped_and_ready", Boolean, nullable=False),
    Column("brand_name", String, nullable=True),
    ForeignKeyConstraint(["pantry_state_id"], ["pantry_states.pantry_state_id"], ondelete="CASCADE"),
)

pantry_item_costs = Table(
    "pantry_item_costs",
    metadata,
    Column("pantry_item_id", UUID(as_uuid=True), primary_key=True),
    Column("applied_from", String, primary_key=True, default=""),
    Column("applied_until", String, primary_key=True, default=""),
    Column("production_cost_us_dollars", DECIMAL(10, 2), nullable=False),
    ForeignKeyConstraint(["pantry_item_id"], ["pantry_items.pantry_item_id"]),
)

pantry_item_availabilities = Table(
    "pantry_item_availabilities",
    metadata,
    Column("pantry_item_id", UUID(as_uuid=True), primary_key=True),
    Column("applied_from", String, primary_key=True, default=""),
    Column("applied_until", String, primary_key=True, default=""),
    ForeignKeyConstraint(["pantry_item_id"], ["pantry_items.pantry_item_id"], ondelete="CASCADE"),
)

pantry_item_custom_fields = Table(
    "pantry_item_custom_fields",
    metadata,
    Column("pantry_item_id", UUID(as_uuid=True), primary_key=True),
    Column("key", String, primary_key=True),
    Column("value", String),
    ForeignKeyConstraint(["pantry_item_id"], ["pantry_items.pantry_item_id"], ondelete="CASCADE"),
)

pantry_item_data_sources = Table(
    "pantry_item_data_sources",
    metadata,
    Column("pantry_item_id", UUID(as_uuid=True), primary_key=True),
    Column("culops_culinary_ingredient_id", BigInteger, nullable=False, index=True),
    Column("culops_culinary_ingredient_specification_id", BigInteger, nullable=False, index=True),
    ForeignKeyConstraint(["pantry_item_id"], ["pantry_items.pantry_item_id"], ondelete="CASCADE"),
)

assemblies = Table(
    "assemblies",
    metadata,
    Column("assembly_id", UUID(as_uuid=True), primary_key=True),
    Column("partner_id", String(8), ForeignKey("partners.partner_id"), nullable=False),
    Column("deleted_at", TIMESTAMP(timezone=True)),
)


assembly_data_sources = Table(
    "assembly_data_sources",
    metadata,
    Column("assembly_id", UUID(as_uuid=True), ForeignKey("assemblies.assembly_id"), primary_key=True),
    Column("culops_assembly_id", BigInteger, nullable=False, index=True),
)


idempotency_keys = Table(
    "idempotency_keys",
    metadata,
    Column("idempotency_key", UUID, primary_key=True),
    Column("idempotent_action", String, primary_key=True),
    Column("expires_at", TIMESTAMP(timezone=True), nullable=False),
)


partner_brands = Table(
    "partner_brands",
    metadata,
    Column("id", Integer, autoincrement=True, primary_key=True),
    Column("partner_id", String(8), nullable=False),
    Column("name", String(), nullable=False),
    Column("fes_name", String(), nullable=False),
    ForeignKeyConstraint(["partner_id"], ["partners.partner_id"], ondelete="CASCADE"),
)


partner_sales_channels = Table(
    "partner_sales_channels",
    metadata,
    Column("id", Integer, autoincrement=True, primary_key=True),
    Column("partner_id", String(8), nullable=False),
    Column("name", String(), nullable=False),
    Column("fes_name", String(), nullable=False),
    ForeignKeyConstraint(["partner_id"], ["partners.partner_id"], ondelete="CASCADE"),
)


recipes = Table(
    "recipes",
    metadata,
    Column("recipe_id", UUID(as_uuid=True), primary_key=True),
    Column("partner_id", String(8), nullable=False),
    Column("deleted_at", TIMESTAMP(timezone=True)),
    Column("externally_created", Boolean, nullable=False),
    ForeignKeyConstraint(["partner_id"], ["partners.partner_id"], ondelete="CASCADE"),
)


recipe_data_sources = Table(
    "recipe_data_sources",
    metadata,
    Column("recipe_id", UUID(as_uuid=True), primary_key=True),
    Column("culops_recipe_id", BigInteger, nullable=False, index=True),
    Column("culops_product_sku", String, nullable=False, index=True),
    ForeignKeyConstraint(
        ["recipe_id"],
        ["recipes.recipe_id"],
        ondelete="CASCADE",
    ),
)


recipe_plan_data_sources = Table(
    "recipe_plan_data_sources",
    metadata,
    Column("partner_recipe_plan_id", Integer, primary_key=True),
    Column("cabinet_plan_id", Integer, nullable=False, index=True),
    ForeignKeyConstraint(
        ["partner_recipe_plan_id"],
        ["partner_recipe_plans.partner_recipe_plan_id"],
        ondelete="CASCADE",
    ),
)
