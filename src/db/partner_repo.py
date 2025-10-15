from dateutil import parser
from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError

from src.core.exceptions import ServerError
from src.db.repo_base import RepositoryBase
from src.db.schema import (
    assembly_packaging_options,
    cost_markups,
    partner_assembly_packaging_options,
    partner_brands,
    partner_packaging_configuration_tags,
    partner_recipe_constraint_tags,
    partner_recipe_plans,
    partner_sales_channels,
    partners,
    recipe_plan_data_sources,
)
from src.interfaces.partner_repo_interface import PartnerRepoInterface
from src.services.models.partner import Brand, CostMarkup, Partner, PartnerRecipePlanMap, SalesChannel
from src.services.models.recipe import PackagingConfigurationTag, RecipeConstraintTag, TagListType


class PartnerRepo(RepositoryBase, PartnerRepoInterface):
    def find_partner_id(self, partner_id: str) -> bool:
        try:
            with self._connection() as conn:
                stmt = select(partners).where(partners.c.partner_id == partner_id)
                return bool(conn.execute(stmt).first())
        except SQLAlchemyError as e:
            raise ServerError(f"Failed to find partner {partner_id}") from e

    def get_partner_by_id(self, partner_id: str) -> Partner:
        try:
            with self._connection() as conn:
                find_partner_stmt = select(partners).where(partners.c.partner_id == partner_id)

                result = conn.execute(find_partner_stmt).mappings().first()
                if result:
                    partner = Partner(
                        name=result["name"],
                        recipe_create_cutoff_days=result["recipe_create_cutoff_days"],
                        recipe_update_cutoff_days=result["recipe_update_cutoff_days"]
                        if result.get("recipe_update_cutoff_days")
                        else None,
                        recipe_delete_cutoff_days=result["recipe_delete_cutoff_days"]
                        if result.get("recipe_delete_cutoff_days")
                        else None,
                        max_assemblies_per_recipe=result["max_assemblies_per_recipe"]
                        if result.get("max_assemblies_per_recipe")
                        else None,
                    )
                else:
                    raise ValueError(f"Partner with ID {partner_id} not found.")

                partner_cost_markups = self.get_partner_cost_markups(partner_id)
                if partner_cost_markups:
                    for cost_markup in partner_cost_markups:
                        partner.add_cost_markup(cost_markup)

                packaging_options = self.get_partner_assembly_packaging_options(partner_id)
                if packaging_options:
                    for packaging_option in packaging_options:
                        partner.add_packaging_option(packaging_option)

                return partner
        except SQLAlchemyError as e:
            raise ServerError(f"failed to get partner {partner_id}") from e

    def get_partner_cost_markups(self, partner_id: str) -> list[CostMarkup]:
        try:
            with self._connection() as conn:
                find_partner_cost_markups_stmt = select(cost_markups).where(cost_markups.c.partner_id == partner_id)
                cost_markups_result = conn.execute(find_partner_cost_markups_stmt).mappings()
                rows = cost_markups_result.fetchall()

                return [
                    CostMarkup(
                        applied_from=parser.parse(row["applied_from"]) if row.get("applied_from") else None,
                        applied_until=parser.parse(row["applied_until"]) if row.get("applied_until") else None,
                        markup_percent=row["markup_percent"],
                    )
                    for row in rows
                ]
        except SQLAlchemyError as e:
            raise ServerError(f"failed to get cost markups for partner {partner_id}") from e

    def get_partner_assembly_packaging_options(self, partner_id: str) -> list[str]:
        try:
            with self._connection() as conn:
                find_partner_packaging_options_stmt = (
                    select(assembly_packaging_options)
                    .select_from(
                        partner_assembly_packaging_options.join(
                            assembly_packaging_options,
                            partner_assembly_packaging_options.c.assembly_packaging_option_id
                            == assembly_packaging_options.c.assembly_packaging_option_id,
                        )
                    )
                    .where(partners.c.partner_id == partner_id)
                )
                result = conn.execute(find_partner_packaging_options_stmt).mappings().fetchall()

                packaging_options = [row["assembly_packaging_option_name"] for row in result]
                return packaging_options

        except SQLAlchemyError as e:
            raise ServerError(f"failed to get assembly packaging options for partner {partner_id}") from e

    def get_partner_recipe_plan_maps(self, partner_id: str) -> list[PartnerRecipePlanMap]:
        try:
            with self._connection() as conn:
                find_partner_recipe_plan_maps_stmt = (
                    select(partner_recipe_plans.c.plan_name, recipe_plan_data_sources.c.cabinet_plan_id)
                    .select_from(
                        partner_recipe_plans.join(
                            recipe_plan_data_sources,
                            partner_recipe_plans.c.partner_recipe_plan_id
                            == recipe_plan_data_sources.c.partner_recipe_plan_id,
                        ).join(
                            partners,
                            partners.c.partner_id == partner_recipe_plans.c.partner_id,
                        )
                    )
                    .where(partners.c.partner_id == partner_id)
                )

                rows = conn.execute(find_partner_recipe_plan_maps_stmt).mappings().fetchall()
                return [
                    PartnerRecipePlanMap(plan_name=row["plan_name"], cabinet_plan_id=row["cabinet_plan_id"])
                    for row in rows
                ]

        except SQLAlchemyError as e:
            raise ServerError(f"failed to get recipe plan maps for partner {partner_id}") from e

    def get_partner_recipe_constraint_tags(self, partner_id: str) -> list[RecipeConstraintTag]:
        try:
            with self._connection() as conn:
                find_partner_recipe_constraint_tags_stmt = (
                    select(
                        partner_recipe_constraint_tags.c.tag_id,
                        partner_recipe_constraint_tags.c.culops_tag_type,
                        partner_recipe_constraint_tags.c.culops_tag_value,
                    )
                    .select_from(partner_recipe_constraint_tags)
                    .where(partner_recipe_constraint_tags.c.partner_id == partner_id)
                )

                rows = conn.execute(find_partner_recipe_constraint_tags_stmt).mappings().fetchall()
                return [
                    RecipeConstraintTag(
                        tag_id=row["tag_id"],
                        tag_type=TagListType(row["culops_tag_type"]),
                        tag_value=row["culops_tag_value"],
                    )
                    for row in rows
                ]

        except SQLAlchemyError as e:
            raise ServerError(f"failed to get recipe constraint tags for partner {partner_id}") from e

    def get_partner_packaging_configuration_tags(self, partner_id: str) -> list[PackagingConfigurationTag]:
        try:
            with self._connection() as conn:
                find_partner_packaging_configuration_tags_stmt = (
                    select(
                        partner_packaging_configuration_tags.c.tag_id,
                        partner_packaging_configuration_tags.c.culops_tag_type,
                        partner_packaging_configuration_tags.c.culops_tag_value,
                    )
                    .select_from(partner_packaging_configuration_tags)
                    .where(partner_packaging_configuration_tags.c.partner_id == partner_id)
                )

                rows = conn.execute(find_partner_packaging_configuration_tags_stmt).mappings().fetchall()
                return [
                    PackagingConfigurationTag(
                        tag_id=row["tag_id"],
                        tag_type=TagListType(row["culops_tag_type"]),
                        tag_value=row["culops_tag_value"],
                    )
                    for row in rows
                ]

        except SQLAlchemyError as e:
            raise ServerError(f"failed to get packaging configuration tags for partner {partner_id}") from e

    def get_recipe_create_cutoff_days(self, partner_id: str) -> int:
        try:
            with self._connection() as conn:
                stmt = select(partners.c.recipe_create_cutoff_days).where(partners.c.partner_id == partner_id)
                result = conn.execute(stmt).mappings().fetchone()
                if not result or result["recipe_create_cutoff_days"] is None:
                    raise ServerError(f"recipe_create_cutoff_days not found for partner {partner_id}")
                return int(result["recipe_create_cutoff_days"])
        except SQLAlchemyError as e:
            raise ServerError(f"failed to get recipe_create_cutoff_days for partner {partner_id}") from e
        except ValueError as e:
            raise ServerError(f"Invalid value for recipe_create_cutoff_days for partner {partner_id}") from e

    def get_recipe_update_cutoff_days(self, partner_id: str) -> int:
        try:
            with self._connection() as conn:
                stmt = select(partners.c.recipe_update_cutoff_days).where(partners.c.partner_id == partner_id)
                result = conn.execute(stmt).mappings().fetchone()
                if not result or result["recipe_update_cutoff_days"] is None:
                    raise ServerError(f"recipe_update_cutoff_days not found for partner {partner_id}")

                return int(result["recipe_update_cutoff_days"])
        except SQLAlchemyError as e:
            raise ServerError(f"failed to get recipe_update_cutoff_days for partner {partner_id}") from e
        except ValueError as e:
            raise ServerError(f"Invalid value for recipe_update_cutoff_days for partner {partner_id}") from e

    def get_recipe_delete_cutoff_days(self, partner_id: str) -> int:
        try:
            with self._connection() as conn:
                stmt = select(partners.c.recipe_delete_cutoff_days).where(partners.c.partner_id == partner_id)
                result = conn.execute(stmt).mappings().fetchone()
                if not result or result["recipe_delete_cutoff_days"] is None:
                    raise ServerError(f"recipe_delete_cutoff_days not found for partner {partner_id}")

                return int(result["recipe_delete_cutoff_days"])
        except SQLAlchemyError as e:
            raise ServerError(f"failed to get recipe_delete_cutoff_days for partner {partner_id}") from e
        except ValueError as e:
            raise ServerError(f"Invalid value for recipe_delete_cutoff_days for partner {partner_id}") from e

    def get_branding(self, partner_id: str) -> list[Brand]:
        try:
            with self._connection() as conn:
                stmt = select(partner_brands).where(partner_brands.c.partner_id == partner_id)
                rows = conn.execute(stmt).mappings().fetchall()
                return [
                    Brand(
                        partner_id=row["partner_id"],
                        name=row["name"],
                        fes_name=row["fes_name"],
                    )
                    for row in rows
                ]
        except SQLAlchemyError as e:
            raise ServerError(f"Failed to find brands for partner {partner_id}") from e

    def get_sales_channels(self, partner_id: str) -> list[SalesChannel]:
        try:
            with self._connection() as conn:
                stmt = select(partner_sales_channels).where(partner_sales_channels.c.partner_id == partner_id)
                rows = conn.execute(stmt).mappings().fetchall()
                return [
                    SalesChannel(
                        partner_id=row["partner_id"],
                        name=row["name"],
                        fes_name=row["fes_name"],
                    )
                    for row in rows
                ]
        except SQLAlchemyError as e:
            raise ServerError(f"Failed to find sales channels for partner {partner_id}") from e
