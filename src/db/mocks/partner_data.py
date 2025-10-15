from src.interfaces.partner_repo_interface import PartnerRepoInterface
from src.services.models.pantry import PartnerCostMarkup
from src.services.models.partner import Brand, CostMarkup, Partner, PartnerRecipePlanMap, SalesChannel
from src.services.models.recipe import PackagingConfigurationTag, RecipeConstraintTag, TagListType
from src.utils.datetime_helper import parse_to_datetime


class MockPartnerDB(PartnerRepoInterface):
    def find_partner_id(self, partner_id: str) -> bool:
        return partner_id in ["123", "partner_123", "BA-MAIN"]

    def get_partner_by_id(self, partner_id: str) -> Partner:
        return Partner(
            name=partner_id,
            recipe_create_cutoff_days=10,
            recipe_delete_cutoff_days=10,
            recipe_update_cutoff_days=10,
            max_assemblies_per_recipe=5,
        )

    def get_partner_cost_markups(self, partner_id: str) -> list[CostMarkup]:
        return [
            CostMarkup(
                applied_from=parse_to_datetime("2025-1-1"),
                applied_until=parse_to_datetime("2025-5-30"),
                markup_percent=5,
            ),
            CostMarkup(
                applied_from=parse_to_datetime("2025-6-1"),
                applied_until=parse_to_datetime("2025-12-30"),
                markup_percent=10,
            ),
        ]

    def get_partner_assembly_packaging_options(self, partner_id: str) -> list[str]:
        return []

    @staticmethod
    def get_pantry_cost_markups() -> list[PartnerCostMarkup]:
        return [
            PartnerCostMarkup(
                applied_from=parse_to_datetime("2025-1-1"),
                applied_until=parse_to_datetime("2025-5-30"),
                markup_percent=5,
            ),
            PartnerCostMarkup(
                applied_from=parse_to_datetime("2025-6-1"),
                applied_until=parse_to_datetime("2025-12-30"),
                markup_percent=10,
            ),
        ]

    def get_partner_recipe_plan_maps(self, partner_id: str) -> list[PartnerRecipePlanMap]:
        return []

    def get_partner_recipe_constraint_tags(self, partner_id: str) -> list[RecipeConstraintTag]:
        return [
            RecipeConstraintTag(tag_id="heatAndEat", tag_type=TagListType.CAMPAIGN_TAG_LIST, tag_value="Heat & Eat"),
            RecipeConstraintTag(
                tag_id="preparedAndReady", tag_type=TagListType.CAMPAIGN_TAG_LIST, tag_value="Prepared And Ready"
            ),
        ]

    def get_partner_packaging_configuration_tags(self, partner_id: str) -> list[PackagingConfigurationTag]:
        return [
            PackagingConfigurationTag(tag_id="wheatFree", tag_type=TagListType.BADGE_TAG_LIST, tag_value="Wheat Free"),
            PackagingConfigurationTag(tag_id="vegetarian", tag_type=TagListType.BADGE_TAG_LIST, tag_value="Vegetarian"),
        ]

    def get_branding(self, partner_id: str) -> list[Brand]:
        return [
            Brand(
                partner_id="123",
                name="samuri pizza cat",
                fes_name="samuri pizza cat",
            )
        ]

    def get_recipe_create_cutoff_days(self, partner_id: str) -> int:
        return 60

    def get_recipe_update_cutoff_days(self, partner_id: str) -> int:
        return 60

    def get_recipe_delete_cutoff_days(self, partner_id: str) -> int:
        return 60

    def get_sales_channels(self, partner_id: str) -> list[SalesChannel]:
        sc: list[SalesChannel] = []
        return sc
