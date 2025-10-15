from src.api.routes.v1.models import RecipeTags
from src.interfaces.partner_repo_interface import PartnerRepoInterface
from src.interfaces.partner_service_interface import PartnerServiceInterface
from src.services.models.partner import Brand, CostMarkup, Partner, SalesChannel
from src.services.models.recipe import TagListType
from src.utils.logger import ServiceLogger

logger = ServiceLogger().get_logger(__name__)


class PartnerService(PartnerServiceInterface):
    def __init__(
        self,
        partner_id: str,
        partner_db: PartnerRepoInterface,
    ) -> None:
        self._partner_id = partner_id
        self.partner_db = partner_db

    @property
    def partner_id(self) -> str:
        """Access the partner ID for use in route handlers and service method calls."""
        return self._partner_id

    def validate_partner_id(self) -> bool:
        return bool(self.partner_db.find_partner_id(partner_id=self.partner_id))

    def get_partner(self) -> Partner:
        return self.partner_db.get_partner_by_id(self.partner_id)

    def get_partner_cost_markups(self) -> list[CostMarkup]:
        return self.partner_db.get_partner_cost_markups(self.partner_id)

    def get_partner_assembly_packaging_options(self) -> list[str]:
        return self.partner_db.get_partner_assembly_packaging_options(self.partner_id)

    def get_branding(self) -> list[Brand]:
        return self.partner_db.get_branding(self.partner_id)

    def map_tag_ids_to_values(self, tags: RecipeTags) -> tuple[list[str], list[str]]:
        """Returns a tuple of str lists, with the first list being badge-tags and the second list of campaign-tags"""
        recipe_constraint_tags = self.partner_db.get_partner_recipe_constraint_tags(self.partner_id)
        packaging_configuration_tags = self.partner_db.get_partner_packaging_configuration_tags(self.partner_id)

        all_tags = recipe_constraint_tags + packaging_configuration_tags
        tag_lookup = {tag.tag_id: tag for tag in all_tags}

        badge_values = []
        campaign_values = []
        for tag_id in (tags.recipe_constraint_tags if tags.recipe_constraint_tags else []) + (
            tags.packaging_configuration_tags if tags.packaging_configuration_tags else []
        ):
            tag = tag_lookup.get(tag_id)
            if tag:
                if tag.tag_type == TagListType.BADGE_TAG_LIST:
                    badge_values.append(tag.tag_value)
                elif tag.tag_type == TagListType.CAMPAIGN_TAG_LIST:
                    campaign_values.append(tag.tag_value)

        return badge_values, campaign_values

    def validate_tags(self, tags: RecipeTags) -> bool:
        recipe_constraint_tags = self.partner_db.get_partner_recipe_constraint_tags(self.partner_id)
        packaging_configuration_tags = self.partner_db.get_partner_packaging_configuration_tags(self.partner_id)

        valid_constraint_values = {tag.tag_id for tag in recipe_constraint_tags}
        valid_config_values = {tag.tag_id for tag in packaging_configuration_tags}

        is_valid_constraint = all(tag in valid_constraint_values for tag in (tags.recipe_constraint_tags or []))
        is_valid_config = all(tag in valid_config_values for tag in (tags.packaging_configuration_tags or []))

        if not is_valid_constraint and tags.recipe_constraint_tags:
            logger.error(f"Invalid Constraint Tag(s): {tags.recipe_constraint_tags}")
        if not is_valid_config and tags.packaging_configuration_tags:
            logger.error(f"Invalid Configuration Tag(s): {tags.packaging_configuration_tags}")

        return is_valid_constraint and is_valid_config

    def get_sales_channels(self) -> list[SalesChannel]:
        return self.partner_db.get_sales_channels(self.partner_id)
