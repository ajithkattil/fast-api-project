from datetime import datetime, timedelta
from typing import TypeVar
from uuid import UUID, uuid4

from pydantic import BaseModel

from src.api.routes.v1.models import (
    RecipeIngredient,
    RecipePatchRequest,
    RecipePostRequest,
    RecipeResponse,
    RecipeSku,
    RecipeTags,
)
from src.core.constants import blue_apron_partner_id
from src.core.exceptions import (
    NotFoundException,
    RecipeAlreadyDeletedError,
    RecipeNotFoundError,
    ServerError,
)
from src.interfaces.cabinet_client_interface import CabinetClientInterface
from src.interfaces.culops_client_interface import CulopsClientInterface
from src.interfaces.pantry_db_interface import PantryDBInterface
from src.interfaces.partner_repo_interface import PartnerRepoInterface
from src.interfaces.recipe_service_interface import RecipeServiceInterface
from src.interfaces.recipes_repo_interface import RecipesRepoInterface
from src.services.models.pantry import (
    PantryItemAvailability,
    PantryItemCulinaryIngredientSpecification,
    PantryItemStatus,
)
from src.services.models.recipe import (
    PackagingConfigurationTag,
    PartnerRecipePlan,
    PartnerRecipePlanSlots,
    PartnerRecipeSlot,
    Recipe,
    RecipeConstraintTag,
    RecipePantryItemData,
    RecipeTag,
)
from src.utils.datetime_helper import parse_from_datetime
from src.utils.logger import ServiceLogger

# Optional Rollbar usage (assumes it’s initialized elsewhere)
try:
    import rollbar  # type: ignore
except Exception:  # pragma: no cover - best-effort import
    rollbar = None  # type: ignore

logger = ServiceLogger().get_logger(__name__)

T = TypeVar("T", bound=BaseModel)


class RecipeService(RecipeServiceInterface):
    def __init__(
        self,
        partner_repo: PartnerRepoInterface,
        pantry_repo: PantryDBInterface,
        recipes_repo: RecipesRepoInterface,
        culops_client: CulopsClientInterface,
        cabinet_client: CabinetClientInterface,
    ) -> None:
        self._partner_repo = partner_repo
        self._pantry_repo = pantry_repo
        self._recipes_repo = recipes_repo
        self._culops_client = culops_client
        self._cabinet_client = cabinet_client

    def get_recipes(self, partner_id: str, cycle_date: str, recipe_ids: list[str] | None) -> list[RecipeResponse]:
        req_cycle_date = datetime.strptime(cycle_date, "%Y-%m-%d")
        try:
            if not self._cabinet_client.find_cycle(req_cycle_date):
                raise ValueError(f"Cycle date {cycle_date} is not a valid cycle date")
        except ServerError as e:
            raise ServerError(f"Failed to validate cycle for cycle date: {cycle_date}") from e

        culops_recipe_ids: list[int] = []
        if recipe_ids:
            for recipe_id in recipe_ids:
                try:
                    recipe_id_uuid = UUID(recipe_id)
                except ValueError as e:
                    raise ValueError(f"Recipe id {recipe_id} is not a valid UUID") from e
                culops_recipe_ref = self._recipes_repo.get_culops_recipe_ref_by_id(partner_id, recipe_id_uuid)
                if culops_recipe_ref:
                    if culops_recipe_ref.deleted:
                        raise RecipeAlreadyDeletedError(f"Recipe {recipe_id} has been deleted")
                    culops_recipe_ids.append(culops_recipe_ref.culops_recipe_id)
                else:
                    raise RecipeNotFoundError(f"Recipe {recipe_id} not found")

        try:
            cycle_recipes = self._culops_client.get_cycle_recipes(
                partner_id, req_cycle_date, culops_recipe_ids if culops_recipe_ids else None
            )
        except (ServerError, ValueError) as e:
            if isinstance(e, RecipeNotFoundError):
                if e.recipe_id:
                    recipe_uuid = self._recipes_repo.get_recipe_id_by_culops_recipe_id(int(e.recipe_id))
                else:
                    recipe_uuid = None

                recipe_ref_uuid = "unknown_id"
                if recipe_uuid:
                    recipe_ref_uuid = str(recipe_uuid)

                raise RecipeAlreadyDeletedError(f"Recipe {recipe_ref_uuid} has been deleted", recipe_ref_uuid) from e
            else:
                raise ServerError(f"Failed to get cycle recipes for cycle date: {cycle_date}") from e

        recipe_responses: list[RecipeResponse] = []

        for recipe in cycle_recipes:
            recipe_ingredients: list[RecipeIngredient] = []
            for pantry_item in recipe.pantry_items:
                try:
                    recipe_ingredient = RecipeIngredient(
                        pantry_item_id=pantry_item.pantry_item_id,
                    )
                except Exception as e:
                    raise ServerError(
                        f"Failed to create recipe ingredient for recipe {recipe.recipe_id} "
                        f"from pantry item {pantry_item.pantry_item_id}: {e!s}"
                    ) from e

                recipe_ingredients.append(recipe_ingredient)

            recipe_card_ids: list[str] = []
            for recipe_card in recipe.recipe_card_assignments:
                recipe_card_ids.append(recipe_card.card_id)

            packaging_configuration_tags: list[str] = []
            for packaging_configuration_tag in recipe.packaging_configuration_tags:
                packaging_configuration_tags.append(packaging_configuration_tag.tag_value)

            recipe_constraint_tags: list[str] = []
            for recipe_constraint_tag in recipe.recipe_constraint_tags:
                recipe_constraint_tags.append(recipe_constraint_tag.tag_value)

            recipe_tags: RecipeTags = RecipeTags(
                recipe_constraint_tags=recipe_constraint_tags,
                packaging_configuration_tags=packaging_configuration_tags,
            )

            recipe_response = RecipeResponse(
                recipeId=str(recipe.recipe_id),
                cycleDate=recipe.cycle_date.strftime("%Y-%m-%d"),
                title=recipe.title,
                subtitle=recipe.subtitle,
                pantryItems=recipe_ingredients,
                servings=recipe.servings,
                isAddOn=recipe.add_on,
                recipeCardIds=recipe_card_ids,
                recipeTags=recipe_tags,
            )
            recipe_responses.append(recipe_response)

        return recipe_responses

    def get_all_recipes(self, partner_id: str) -> list[RecipeResponse]:
        """Get all recipes for a partner regardless of cycle date."""
        try:
            # Get all recipe references for this partner from the database
            all_recipe_refs = self._recipes_repo.get_all_recipe_refs_by_partner(partner_id)

            if not all_recipe_refs:
                return []

            recipe_responses: list[RecipeResponse] = []

            for recipe_ref in all_recipe_refs:
                if recipe_ref.deleted:
                    continue

                try:
                    # Get recipe details from CulOps
                    culops_recipe = self._culops_client.get_recipe(
                        culops_recipe_id=recipe_ref.culops_recipe_id,
                        partner_id=partner_id
                    )

                    recipe_ingredients: list[RecipeIngredient] = []
                    for pantry_item in culops_recipe.pantry_items:
                        recipe_ingredients.append(
                            RecipeIngredient(pantry_item_id=pantry_item.pantry_item_id)
                        )

                    recipe_card_ids = [card.card_id for card in culops_recipe.recipe_card_assignments]
                    packaging_configuration_tags = [tag.tag_value for tag in culops_recipe.packaging_configuration_tags]
                    recipe_constraint_tags = [tag.tag_value for tag in culops_recipe.recipe_constraint_tags]

                    recipe_tags = RecipeTags(
                        recipe_constraint_tags=recipe_constraint_tags,
                        packaging_configuration_tags=packaging_configuration_tags,
                    )

                    recipe_response = RecipeResponse(
                        recipeId=str(culops_recipe.recipe_id),
                        cycleDate=culops_recipe.cycle_date.strftime("%Y-%m-%d"),
                        title=culops_recipe.title,
                        subtitle=culops_recipe.subtitle,
                        pantryItems=recipe_ingredients,
                        servings=culops_recipe.servings,
                        isAddOn=culops_recipe.add_on,
                        recipeCardIds=recipe_card_ids,
                        recipeTags=recipe_tags,
                    )
                    recipe_responses.append(recipe_response)

                except (RecipeNotFoundError, ServerError) as e:
                    logger.warning(f"Skipping recipe {recipe_ref.recipe_id}: {e}")
                    continue

            return recipe_responses

        except ServerError as e:
            raise ServerError(f"Failed to get all recipes for partner {partner_id}") from e

    def get_recipe_ids_by_skus(self, partner_id: str, product_skus: list[str]) -> list[T]:
        # Batch fetch all recipe refs by SKUs in a single query
        recipe_refs = self._recipes_repo.get_culops_recipe_refs_by_skus(partner_id=partner_id, skus=product_skus)

        # Check if we found all SKUs
        found_skus = {ref.culops_product_sku for ref in recipe_refs}
        missing_skus = set(product_skus) - found_skus
        if missing_skus:
            raise NotFoundException(f"Failed to find recipes for SKUs: {', '.join(sorted(missing_skus))}")

        return [RecipeSku(id=str(ref.recipe_id), sku=ref.culops_product_sku) for ref in recipe_refs]

    def create_recipe(
        self,
        partner_id: str,
        recipe_data: RecipePostRequest,
    ) -> RecipeResponse:
        cycle_date = datetime.strptime(recipe_data.cycle_date, "%Y-%m-%d")
        if not self._cycle_date_is_valid(cycle_date):
            raise ValueError(f"Cycle date {recipe_data.cycle_date} is not valid")

        cutoff_days = self._partner_repo.get_recipe_create_cutoff_days(partner_id)
        cutoff_date = datetime.now() + timedelta(days=cutoff_days)
        if cycle_date < cutoff_date:
            raise ValueError(
                f"Cycle date {recipe_data.cycle_date} is before cutoff date {cutoff_date.strftime('%Y-%m-%d')}"
            )

        recipe_constraint_tag_objects: list[RecipeConstraintTag] = []
        if recipe_data.recipe_tags:
            constraint_tags = recipe_data.recipe_tags.recipe_constraint_tags or []
            recipe_constraint_tag_objects = self._validate_and_map_recipe_constraint_tags(partner_id, constraint_tags)

        packaging_config_tag_objects: list[PackagingConfigurationTag] = []
        if recipe_data.recipe_tags:
            packaging_tags = recipe_data.recipe_tags.packaging_configuration_tags or []
            packaging_config_tag_objects = self._validate_and_map_packaging_config_tags(partner_id, packaging_tags)

        pantry_item_ids = [str(item.pantry_item_id) for item in recipe_data.pantry_items]

        # ====== LOGGING FOCUS AREA (was around line ~255) ======
        logger.info(
            "create_recipe: fetching pantry_item_data_sources",
            extra={"partner_id": partner_id, "pantry_item_ids": pantry_item_ids},
        )
        if rollbar:
            try:
                rollbar.report_message(
                    "create_recipe: fetching pantry_item_data_sources",
                    level="info",
                    extra_data={"partner_id": partner_id, "pantry_item_ids": pantry_item_ids},
                )
            except Exception:
                pass

        pantry_item_data_sources = self._pantry_repo.get_pantry_item_data_sources(pantry_item_ids)

        # Log what was resolved (keys are UUIDs)
        resolved_keys = [str(k) for k in pantry_item_data_sources.keys()]
        logger.info(
            "create_recipe: pantry_item_data_sources resolved",
            extra={
                "requested_count": len(pantry_item_ids),
                "resolved_count": len(resolved_keys),
                "resolved_uuids": resolved_keys,
            },
        )
        if rollbar:
            try:
                rollbar.report_message(
                    "create_recipe: pantry_item_data_sources resolved",
                    level="info",
                    extra_data={
                        "requested_count": len(pantry_item_ids),
                        "resolved_count": len(resolved_keys),
                        "resolved_uuids": resolved_keys,
                    },
                )
            except Exception:
                pass
        # ====== END LOGGING FOCUS AREA ======

        missing_pantry_item_ids = [
            str(item.pantry_item_id)
            for item in recipe_data.pantry_items
            if item.pantry_item_id not in pantry_item_data_sources
        ]

        if missing_pantry_item_ids:
            logger.warning(
                "create_recipe: pantry items missing in DB",
                extra={"missing_pantry_item_ids": missing_pantry_item_ids},
            )
            if rollbar:
                try:
                    rollbar.report_message(
                        "create_recipe: pantry items missing in DB",
                        level="warning",
                        extra_data={"missing_pantry_item_ids": missing_pantry_item_ids},
                    )
                except Exception:
                    pass
            raise ValueError(f"Pantry item IDs not found in pantry: {missing_pantry_item_ids}")

        try:
            pantry_item_statuses = self._culops_client.get_recipe_pantry_item_data(
                [source.culops_culinary_ingredient_specification_id for source in pantry_item_data_sources.values()]
            )
        except ServerError as e:
            raise ServerError(
                f"Failed to get pantry item data for recipe {recipe_data.title} with items "
                + f"{pantry_item_data_sources.values()}"
            ) from e

        recipe_pantry_items_details: list[RecipePantryItemData] = []

        for item_id in pantry_item_ids:
            try:
                item_status = self._get_item_status(item_id, pantry_item_data_sources, pantry_item_statuses)
                self._validate_recipe_item_availability(cycle_date, item_status)

                recipe_pantry_items_details.append(
                    RecipePantryItemData(
                        pantry_item_id=item_id,
                        is_prepped_and_ready=item_status.is_prepped_and_ready,
                    )
                )

            except Exception as e:
                raise ValueError(f"Unable to process item {item_id}: {e!s}") from e

        recipe_card_id = recipe_data.title

        prepped_and_ready_items = [item for item in recipe_pantry_items_details if item.is_prepped_and_ready]

        if len(prepped_and_ready_items) == len(recipe_pantry_items_details):
            if len(prepped_and_ready_items) == 1:
                recipe_card_id = ""
            else:
                raise ValueError(f"Multiple prepped and ready pantry items: {pantry_item_ids}")
        elif len(prepped_and_ready_items) != 0:
            raise ValueError(f"Mixed prepped and ready and standard pantry items: {pantry_item_ids}")

        recipe = Recipe(
            partner_id=partner_id,
            recipe_id=uuid4(),
            title=recipe_data.title,
            subtitle=recipe_data.subtitle,
            add_on=recipe_data.is_add_on,
            cycle_date=cycle_date,
            servings=recipe_data.servings,
            pantry_items=recipe_pantry_items_details,
            recipe_constraint_tags=recipe_constraint_tag_objects,
            packaging_configuration_tags=packaging_config_tag_objects,
        )

        recipe_plan = PartnerRecipePlan.from_partner_recipe(recipe)
        recipe_plan_name = recipe_plan.plan_name()

        slot_assignment_service = RecipeSlotAssignmentService(
            self._partner_repo, self._culops_client, self._cabinet_client
        )
        try:
            slot_code = slot_assignment_service.assign_recipe_slot(recipe)
        except ServerError as e:
            raise ServerError(
                f"Failed to assign recipe slot for recipe {recipe_data.title} with items {pantry_item_ids}"
            ) from e

        all_recipe_tags: list[RecipeTag] = [*recipe_constraint_tag_objects, *packaging_config_tag_objects]

        badge_tags = self._get_culops_badge_tags(all_recipe_tags)
        campaign_tags = self._get_culops_campaign_tags(all_recipe_tags)

        culops_recipe_id = None

        try:
            try:
                recipe_create_response = self._culops_client.create_recipe(
                    cycle_date=cycle_date,
                    title=recipe_data.title,
                    subtitle=recipe_data.subtitle,
                    servings=recipe_data.servings,
                    recipe_plan_name=recipe_plan_name,
                    recipe_short_code=slot_code,
                    recipe_card_id=recipe_card_id,
                    badge_tags=badge_tags,
                    campaign_tags=campaign_tags,
                )
            except (ServerError, ValueError) as e:
                raise ServerError(f"Failed to create recipe {recipe_data.title} with items {pantry_item_ids}") from e

            culops_recipe_id = recipe_create_response.recipe_id
            culops_recipe_sku = recipe_create_response.recipe_sku

            try:
                self._recipes_repo.store_recipe_source(
                    partner_id, recipe.recipe_id, culops_recipe_id, culops_recipe_sku
                )
            except ServerError as e:
                raise ServerError(
                    f"Failed to store recipe source for recipe {recipe_data.title} with items {pantry_item_ids}"
                ) from e

            try:
                ingredients_to_add = [
                    pantry_item_data_sources[UUID(item_id)]
                    for item_id in pantry_item_ids
                    if UUID(item_id) in pantry_item_data_sources
                ]
                self._culops_client.add_recipe_ingredients(
                    culops_recipe_id,
                    ingredients_to_add,
                )
            except ServerError as e:
                raise ServerError(
                    f"Failed to add recipe ingredients for recipe {recipe_data.title} with items {pantry_item_ids}  "
                ) from e
        except ServerError as e:
            delete_recipe_error = None

            if culops_recipe_id:
                try:
                    self._culops_client.delete_recipe(culops_recipe_id)
                except ServerError as e:
                    delete_recipe_error = "Failed to delete recipe for recipe creation failure "
                    delete_recipe_error += f"{recipe_data.title} with items {pantry_item_ids} with error {e}"
            raise ServerError(
                f"Failed to create recipe {recipe_data.title} with items {pantry_item_ids}"
                f"{' and error ' + delete_recipe_error if delete_recipe_error else ''}"
            ) from e

        return RecipeResponse(
            recipeId=str(recipe.recipe_id),
            cycleDate=recipe_data.cycle_date,
            title=recipe_data.title,
            subtitle=recipe_data.subtitle,
            pantryItems=recipe_data.pantry_items,
            servings=recipe_data.servings,
            isAddOn=recipe_data.is_add_on,
            recipeCardIds=[recipe_card_id],
            recipeTags=RecipeTags(
                recipeConstraintTags=[tag.tag_id for tag in recipe_constraint_tag_objects],
                packagingConfigurationTags=[tag.tag_id for tag in packaging_config_tag_objects],
            ),
        )

    def update_recipe(self, partner_id: str, recipe_id: str, recipe_data: RecipePatchRequest) -> RecipeResponse | None:
        try:
            culops_recipe_data = self._recipes_repo.get_culops_recipe_ref_by_id(partner_id, UUID(recipe_id))

            if not culops_recipe_data or not culops_recipe_data.culops_recipe_id:
                raise RecipeNotFoundError(f"Recipe {recipe_id} not found")
            if culops_recipe_data.deleted:
                raise RecipeAlreadyDeletedError(f"Recipe {recipe_id} has been deleted")

            recipe = self._culops_client.get_recipe(culops_recipe_data.culops_recipe_id, partner_id)

            if not recipe:
                raise RecipeNotFoundError(f"Recipe {recipe_id} not found in culops")
            if not self._cycle_date_is_valid(recipe.cycle_date):
                raise ValueError(f"Cycle date {parse_from_datetime(recipe.cycle_date)} is not valid")

            cutoff_days = self._partner_repo.get_recipe_update_cutoff_days(partner_id)
            cutoff_date = datetime.now() + timedelta(days=cutoff_days)
            if recipe.cycle_date < cutoff_date:
                raise ValueError(
                    f"Cycle date {parse_from_datetime(recipe.cycle_date)} is within cutoff date "
                    + f"{cutoff_date.strftime('%Y-%m-%d')}"
                )

            if recipe_data.recipe_tags or recipe_data.title or recipe_data.subtitle:
                recipe_constraint_tag_objects: list[RecipeConstraintTag] = []
                if recipe_data.recipe_tags:
                    constraint_tags = recipe_data.recipe_tags.recipe_constraint_tags or []
                    recipe_constraint_tag_objects = self._validate_and_map_recipe_constraint_tags(
                        partner_id, constraint_tags
                    )

                packaging_config_tag_objects: list[PackagingConfigurationTag] = []
                if recipe_data.recipe_tags:
                    packaging_tags = recipe_data.recipe_tags.packaging_configuration_tags or []
                    packaging_config_tag_objects = self._validate_and_map_packaging_config_tags(
                        partner_id, packaging_tags
                    )

                all_recipe_tags: list[RecipeTag] = [*recipe_constraint_tag_objects, *packaging_config_tag_objects]

                self._culops_client.update_recipe(
                    recipe_id=culops_recipe_data.culops_recipe_id,
                    title=recipe_data.title or None,
                    subtitle=recipe_data.subtitle or None,
                    badge_tags=self._get_culops_badge_tags(all_recipe_tags),
                    campaign_tags=self._get_culops_campaign_tags(all_recipe_tags),
                )

            if recipe_data.pantry_items:
                recipe_ingredient_ids = [str(pantry_item.pantry_item_id) for pantry_item in recipe_data.pantry_items or []]
                pantry_item_data_sources = self._pantry_repo.get_pantry_item_data_sources(recipe_ingredient_ids)
                original_list = [(item.pantry_item_id, item.ingredient_id) for item in recipe.pantry_items or []]

                try:
                    pantry_item_statuses = self._culops_client.get_recipe_pantry_item_data(
                        [
                            source.culops_culinary_ingredient_specification_id
                            for source in pantry_item_data_sources.values()
                        ]
                    )
                except ServerError as e:
                    raise ServerError(
                        f"Failed to get pantry item data for recipe {'recipe_data.title'} with items "
                        + f"{pantry_item_data_sources.values()}"
                    ) from e

                recipe_pantry_items_details: list[RecipePantryItemData] = []

                for item_id in recipe_ingredient_ids:
                    try:
                        item_status = self._get_item_status(item_id, pantry_item_data_sources, pantry_item_statuses)
                        self._validate_recipe_item_availability(recipe.cycle_date, item_status)

                        recipe_pantry_items_details.append(
                            RecipePantryItemData(
                                pantry_item_id=item_id,
                                is_prepped_and_ready=item_status.is_prepped_and_ready,
                            )
                        )

                    except Exception as e:
                        raise ValueError(f"Unable to process item {item_id}: {e!s}") from e

                prepped_and_ready_items = [item for item in recipe_pantry_items_details if item.is_prepped_and_ready]

                if 0 < len(prepped_and_ready_items) < len(recipe_pantry_items_details):
                    raise ValueError(f"Mixed prepped and ready and standard pantry items: {recipe_ingredient_ids}")
                elif (
                    len(prepped_and_ready_items) == len(recipe_pantry_items_details)
                    and len(prepped_and_ready_items) > 1
                ):
                    raise ValueError(f"Multiple prepped and ready pantry items: {recipe_ingredient_ids}")
                items_to_add = list(set(recipe_ingredient_ids) - set([item[0] for item in original_list]))
                items_to_remove: list[str] = []
                for item in original_list:
                    if item[0] not in recipe_ingredient_ids:
                        items_to_remove.append(item[1])

                if items_to_remove:
                    self._culops_client.remove_recipe_ingredients(culops_recipe_data.culops_recipe_id, items_to_remove)

                if items_to_add:
                    ingredients_to_add = [
                        pantry_item_data_sources[UUID(item_id)]
                        for item_id in items_to_add
                        if UUID(item_id) in pantry_item_data_sources
                    ]
                    self._culops_client.add_recipe_ingredients(culops_recipe_data.culops_recipe_id, ingredients_to_add)

            return RecipeResponse(
                recipeId=recipe_id,
                cycleDate=parse_from_datetime(recipe.cycle_date),
                title=recipe_data.title or recipe.title or "",
                subtitle=recipe_data.subtitle or recipe.subtitle or "",
                pantryItems=recipe_data.pantry_items or recipe.pantry_items,
                servings=recipe.servings,
                isAddOn=recipe.add_on,
                recipeCardIds=[assignment.card_id for assignment in recipe.recipe_card_assignments or []],
                recipeTags=recipe_data.recipe_tags
                or RecipeTags(
                    recipeConstraintTags=recipe.recipe_constraint_tags or [],
                    packagingConfigurationTags=recipe.packaging_configuration_tags or [],
                ),
            )

        except Exception:
            raise

    def delete_recipe(self, partner_id: str, recipe_id: str) -> None:
        try:
            recipe_uuid = UUID(recipe_id)
        except ValueError as e:
            raise ValueError(f"Invalid recipe ID format: {recipe_id}") from e

        culops_recipe_ref = self._recipes_repo.get_culops_recipe_ref_by_id(partner_id, recipe_uuid)
        if not culops_recipe_ref:
            raise RecipeNotFoundError(f"Recipe with ID {recipe_id} not found for partner {partner_id}")

        if culops_recipe_ref.deleted:
            raise RecipeAlreadyDeletedError(f"Recipe with ID {recipe_id} is already deleted")

        try:
            culops_recipe = self._culops_client.get_recipe(culops_recipe_ref.culops_recipe_id, partner_id)
            if not culops_recipe:
                self._recipes_repo.mark_recipe_as_deleted(partner_id, recipe_uuid)
                raise RecipeAlreadyDeletedError(f"Recipe with ID {recipe_id} not found in CulOps")
        except ServerError as e:
            raise ServerError(f"Failed to get Culops recipe before deleting {recipe_id} from CulOps") from e

        cutoff_days = self._partner_repo.get_recipe_delete_cutoff_days(partner_id)
        cutoff_date = datetime.now() + timedelta(days=cutoff_days)
        if culops_recipe.cycle_date.date() <= cutoff_date.date():
            raise ValueError(
                f"Recipe cycle date {culops_recipe.cycle_date.strftime('%Y-%m-%d')} is in delete cutoff window"
            )

        def delete_recipe_callback() -> None:
            try:
                self._culops_client.delete_recipe(culops_recipe_ref.culops_recipe_id)
            except (ServerError, ValueError) as e:
                raise ServerError(f"Failed to delete recipe {recipe_id} from CulOps") from e

        self._recipes_repo.mark_recipe_as_deleted(partner_id, recipe_uuid, delete_recipe_callback)

    def _validate_and_map_recipe_constraint_tags(
        self, partner_id: str, tag_ids: list[str]
    ) -> list[RecipeConstraintTag]:
        supported_tags = self._partner_repo.get_partner_recipe_constraint_tags(partner_id)
        supported_tag_ids = {tag.tag_id for tag in supported_tags}

        invalid_tags = [tag_id for tag_id in tag_ids if tag_id not in supported_tag_ids]
        if invalid_tags:
            raise ValueError(f"Invalid recipe constraint tags: {invalid_tags}")

        return [tag for tag in supported_tags if tag.tag_id in tag_ids]

    def _validate_and_map_packaging_config_tags(
        self, partner_id: str, tag_ids: list[str]
    ) -> list[PackagingConfigurationTag]:
        supported_tags = self._partner_repo.get_partner_packaging_configuration_tags(partner_id)
        supported_tag_ids = {tag.tag_id for tag in supported_tags}

        invalid_tags = [tag_id for tag_id in tag_ids if tag_id not in supported_tag_ids]
        if invalid_tags:
            raise ValueError(f"Invalid packaging configuration tags: {invalid_tags}")

        return [tag for tag in supported_tags if tag.tag_id in tag_ids]

    @staticmethod
    def _is_available_in_cycle(cycle_date: datetime, item_availabilities: list[PantryItemAvailability]) -> bool:
        return any(
            availability.available_from is None or cycle_date >= availability.available_from
            for availability in item_availabilities
        )

    @staticmethod
    def _cycle_date_is_valid(cycle_date: datetime) -> bool:
        return cycle_date.date() >= datetime.now().date() and cycle_date.weekday() == 0

    @staticmethod
    def _get_culops_badge_tags(recipe_tags: list[RecipeTag]) -> list[str]:
        return [tag.tag_value for tag in recipe_tags if tag.tag_type == "badge_tag_list"]

    @staticmethod
    def _get_culops_campaign_tags(recipe_tags: list[RecipeTag]) -> list[str]:
        return [tag.tag_value for tag in recipe_tags if tag.tag_type == "campaign_tag_list"]

    @staticmethod
    def _get_item_status(
        item_id: str,
        pantry_item_data_sources: dict[UUID, PantryItemCulinaryIngredientSpecification],
        pantry_item_statuses: dict[int, PantryItemStatus],
    ) -> PantryItemStatus:
        spec_id = next(
            (
                source.culops_culinary_ingredient_specification_id
                for source in pantry_item_data_sources.values()
                if source.pantry_item_id == UUID(item_id)
            ),
            None,
        )

        if not spec_id:
            raise ValueError("No CulOps specification found")

        item_status = pantry_item_statuses.get(spec_id, None)
        if not item_status:
            raise ValueError("CulOps pantry item data not found")
        return item_status

    def _validate_recipe_item_availability(self, cycle_date: datetime, item_status: PantryItemStatus) -> None:
        item_availabilities = item_status.availabilities

        if not item_availabilities:
            return

        if not self._is_available_in_cycle(cycle_date, item_availabilities):
            raise ValueError(f"Not available for cycle date {cycle_date.strftime('%Y-%m-%d')}")


class RecipeSlotAssignmentService:
    def __init__(
        self,
        partner_repo: PartnerRepoInterface,
        culops_client: CulopsClientInterface,
        cabinet_client: CabinetClientInterface,
    ) -> None:
        self._partner_repo = partner_repo
        self._culops_client = culops_client
        self._cabinet_client = cabinet_client

    def assign_recipe_slot(self, recipe: Recipe) -> str:
        """Assign a recipe slot using Culops as the source of truth."""
        recipe_plan = PartnerRecipePlan.from_partner_recipe(recipe)
        recipe_plan_name = recipe_plan.plan_name()

        # Get all valid slot codes from Culops for this plan
        try:
            all_valid_slots = self._culops_client.get_available_recipe_slots(recipe_plan_name)
        except ServerError as e:
            raise ServerError(f"Failed to get available recipe slots from Culops for plan '{recipe_plan_name}'") from e

        if not all_valid_slots:
            raise ValueError(f"No valid slot codes found in Culops for plan '{recipe_plan_name}'")

        # Get all recipes for this cycle to determine which slots are taken
        try:
            all_cycle_recipes = self._culops_client.get_cycle_recipes(
                recipe.partner_id, recipe.cycle_date, recipe_ids=None
            )
        except ServerError as e:
            raise ServerError(
                f"Failed to get recipes from Culops for cycle {recipe.cycle_date.strftime('%Y-%m-%d')}"
            ) from e

        # Collect all taken slot codes
        taken_slot_codes = {
            er.recipe_slot_short_code
            for er in all_cycle_recipes
            if er.recipe_slot_short_code is not None
        }

        # Find first available slot
        for slot_code in all_valid_slots:
            if slot_code not in taken_slot_codes:
                return slot_code

        # No available slots found
        raise ValueError(
            f"No available slots found for plan '{recipe_plan_name}' on cycle {recipe.cycle_date.strftime('%Y-%m-%d')}. "
            f"All {len(all_valid_slots)} slots are taken."
        )

    def _get_partner_slot_plans(self, recipe: Recipe) -> list[PartnerRecipePlanSlots]:
        plan_list = self._partner_repo.get_partner_recipe_plan_maps(recipe.partner_id)

        recipe_plan_slots_list: list[PartnerRecipePlanSlots] = []

        for plan in plan_list:
            recipe_plan = PartnerRecipePlan.from_partner_recipe(recipe)
            plan_slots = PartnerRecipePlanSlots(recipe.partner_id, plan.cabinet_plan_id, plan.plan_name, recipe_plan)
            recipe_plan_slots_list.append(plan_slots)

        return recipe_plan_slots_list


class PartnerCycleSlots:
    def __init__(self, partner_id: str, recipe_plan_slots_list: list[PartnerRecipePlanSlots]) -> None:
        self._partner_id = partner_id
        self._recipe_plan_slots_list = recipe_plan_slots_list

    def assign_recipe_slot(self, recipe: Recipe) -> str:
        plan_name = PartnerRecipePlan.from_partner_recipe(recipe).plan_name()
        recipe_plan_slots = self.get_recipe_plan_slots_by_name(plan_name)

        if recipe_plan_slots is None:
            raise ValueError(f"No recipe plan slots found for plan name: {plan_name}")

        # Allow a partner to provide a non-default way of assigning a recipe slot
        code = self._get_code_with_partner_presort_rules(plan_name, recipe, recipe_plan_slots)
        if code is not None:
            return code

        sorted_slots = self._sort_plan_slots(recipe_plan_slots)

        for slot in sorted_slots:
            if slot.recipe_assignment_id is not None:
                continue

            if not self._does_recipe_meet_partner_slot_constraints(slot, recipe):
                continue

            slot.recipe_assignment_id = recipe.recipe_id
            return slot.slot_code

        raise ValueError(f"No available slots for recipe: {recipe.recipe_id}")

    def get_recipe_plan_slots_by_name(self, plan_name: str) -> PartnerRecipePlanSlots | None:
        for item in self._recipe_plan_slots_list:
            if item.plan_name == plan_name:
                return item
        return None

    def get_recipe_plan_slots_by_cabinet_id(self, cabinet_id: int) -> PartnerRecipePlanSlots | None:
        for item in self._recipe_plan_slots_list:
            if item.cabinet_plan_id == cabinet_id:
                return item
        return None

    def _get_code_with_partner_presort_rules(
        self, plan_name: str, recipe: Recipe, recipe_plan_slots: PartnerRecipePlanSlots
    ) -> str | None:
        """
        Applies partner-specific presort rules for a given recipe and plan. Depending on the partner's
        rules, it may determine if a variant of the given plan is applicable and assign a suitable recipe
        slot for the recipe within its plan.

        Args:
            plan_name: The name of the recipe plan to check against preset rules.
            recipe: The Recipe object to evaluate and potentially assign to a slot.
            recipe_plan_slots: The PartnerRecipePlanSlots object containing available recipe slots.

        Returns:
            A string representing the slot code where the recipe was assigned if an assignment
            occurred, otherwise None.
        """
        return None

    def _does_recipe_meet_partner_slot_constraints(self, slot: PartnerRecipeSlot, recipe: Recipe) -> bool:
        """
        Allows a specific partner to define additional constraints on the slot assignment. Passing up
        an otherwise valid slot

        Args:
            slot (PartnerRecipeSlot): The slot object associated with the partner
            recipe (Recipe): The recipe object to check against the specified slot,

        Returns:
            bool: False if an additional constraint is met and the slot should NOT be used with the recipe,
            otherwise True.
        """
        if self._partner_id == blue_apron_partner_id:
            if slot.slot_code == "F" or slot.slot_code == "FF":
                return False
            if slot.slot_code == "P" or slot.slot_code == "FP":
                return False
            if slot.slot_code == "M" or slot.slot_code == "FM":
                return False
            if slot.slot_code == "V" or slot.slot_code == "FV":
                return False
            if slot.slot_code == "FR":
                return False
            if slot.slot_code == "PX":
                return False
            if slot.slot_code == "MP":
                return False
            if slot.slot_code == "WC":
                return False
        return True

    @staticmethod
    def _sort_plan_slots(plan_slots: PartnerRecipePlanSlots) -> list[PartnerRecipeSlot]:
        slots = plan_slots.recipe_slots

        def sort_key(slot: PartnerRecipeSlot) -> tuple[int, int | str]:
            code = slot.slot_code
            numeric_part = "".join(filter(str.isdigit, code))

            if numeric_part:
                # Group codes with numbers together.
                # Sort them by their numeric value.
                return 1, int(numeric_part)
            else:
                # Group codes without numbers together.
                # Sort them alphabetically.
                return 0, code

        return sorted(slots, key=sort_key)