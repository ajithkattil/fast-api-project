from collections.abc import Iterator
from datetime import UTC, datetime, timedelta
from enum import Enum
from uuid import uuid4

import requests
from pydantic import ValidationError
from requests.exceptions import HTTPError, RequestException

from src.clients.culops.models.culops_pantry import (
    CulinaryIngredientBrand,
    CulinaryIngredientSpecificationCostAttribute,
    CulopsData,
)
from src.clients.culops.models.culops_recipe import (
    CulinaryIngredientSpecificationRelationships,
    CulopsRecipeListResponse,
    CulopsRecipeUpdateResponse,
    IngredientRelationships,
    ResourceIdentifier,
)
from src.core.config import settings
from src.core.constants import PREPPED_AND_READY_CATEGORY
from src.core.exceptions import RecipeNotFoundError, ServerError
from src.interfaces.culops_client_interface import CulopsClientInterface
from src.interfaces.pantry_db_interface import PantryDBInterface
from src.interfaces.partner_repo_interface import PartnerRepoInterface
from src.interfaces.recipes_repo_interface import RecipesRepoInterface
from src.interfaces.token_service_interface import TokenServiceInterface
from src.services.models.pantry import (
    PantryItem,
    PantryItemAvailability,
    PantryItemCost,
    PantryItemCulinaryIngredientSpecification,
    PantryItemCustomField,
    PantryItemDataSource,
    PantryItemStatus,
)
from src.services.models.recipe import (
    CreateCulopsRecipeResponse,
    CulopsRecipe,
    CulopsRecipePantryItemData,
    PackagingConfigurationTag,
    Recipe,
    RecipeCardAssignment,
    RecipeConstraintTag,
    TagListType,
)
from src.services.token import TokenName
from src.utils.datetime_helper import parse_to_datetime
from src.utils.logger import ServiceLogger
from src.utils.validation import validate_cycle_datetime

# Optional Rollbar import (safe if not installed/initialized)
try:
    import rollbar  # type: ignore
except Exception:
    rollbar = None  # type: ignore[assignment]

log = ServiceLogger().get_logger(__name__)


class CulOpsService(CulopsClientInterface):
    def __init__(
        self,
        partner_repo: PartnerRepoInterface,
        recipe_repo: RecipesRepoInterface,
        pantry_repo: PantryDBInterface,
        token_svc: TokenServiceInterface,
    ) -> None:
        self.host = settings.CULOPS_API_HOST
        self.api_path = "/api"
        self.session = requests.Session()
        self.token_svc = token_svc
        self.partner_repo = partner_repo
        self.recipe_repo = recipe_repo
        self.pantry_repo = pantry_repo
        self.fetch_size = settings.CULOPS_PANTRY_FETCH_SIZE

    def get_partner_culops_pantry_data(
        self,
        available_from: datetime | None = None,
        available_until: datetime | None = None,
        partner_id: str = "",
        brand_name: str = "",
        page: int | None = None,
        page_size: int | None = None,
    ) -> Iterator[tuple[list[PantryItem], bool]]:
        token = self._get_culops_token()

        # If page is specified, fetch only that page. Otherwise fetch all pages.
        fetch_all_pages = page is None
        current_page = page if page is not None else 1
        actual_page_size = page_size if page_size is not None else self.fetch_size

        log.info(
            "culops get pantry: starting fetch",
            extra={
                "partner_id": partner_id,
                "brand_name": brand_name,
                "available_from": available_from.isoformat() if available_from else None,
                "available_until": available_until.isoformat() if available_until else None,
                "page_size": actual_page_size,
                "page": current_page,
                "fetch_all_pages": fetch_all_pages,
            },
        )
        if rollbar:
            try:
                rollbar.report_message(
                    "culops get pantry: starting fetch",
                    level="info",
                    extra_data={
                        "partner_id": partner_id,
                        "brand_name": brand_name,
                        "available_from": available_from.isoformat() if available_from else None,
                        "available_until": available_until.isoformat() if available_until else None,
                        "page_size": self.fetch_size,
                    },
                )
            except Exception:
                pass

        while True:
            url = f"https://{self.host}{self.api_path}/culinary-ingredient-specifications"

            try:
                res = self.session.get(
                    url=url,
                    headers={"Authorization": f"Bearer {token}"},
                    params={
                        # NOTE: CulOps API does not support these filters - they are silently ignored
                        # Filtering is done client-side in _map_pantry_items() instead
                        # "brand_name": brand_name,
                        # "available_from": available_from.strftime("%Y-%m-%d") if available_from else None,
                        # "available_until": available_until.strftime("%Y-%m-%d") if available_until else None,
                        "include": "culinary-ingredient,culinary-ingredient-specification-costs",
                        "page[number]": current_page,
                        "page[size]": actual_page_size,
                    },
                )

                res.raise_for_status()
                res_json = res.json()

            except (HTTPError, RequestException) as e:
                err_msg = "failed to fetch culinary ingredient specifications for partner pantry request"
                if getattr(e, "response", None) is not None:
                    status_code = e.response.status_code
                    message = e.response.text
                    err_msg += f" with status code {status_code} and message: {message}"
                raise ServerError(err_msg) from e

            try:
                culops_pantry_data = CulopsData.model_validate(res_json)
                pantry_items = self._map_pantry_items(culops_pantry_data, available_from, available_until)

                log.info(
                    f"culops get pantry: fetched page {current_page}",
                    extra={
                        "partner_id": partner_id,
                        "page": current_page,
                        "items_count": len(pantry_items),
                        "has_next": bool(res_json.get("links", {}).get("next")),
                    },
                )
                if rollbar:
                    try:
                        rollbar.report_message(
                            f"culops get pantry: fetched page {current_page}",
                            level="info",
                            extra_data={
                                "partner_id": partner_id,
                                "page": current_page,
                                "items_count": len(pantry_items),
                                "has_next": bool(res_json.get("links", {}).get("next")),
                            },
                        )
                    except Exception:
                        pass

                has_next = bool(res_json.get("links", {}).get("next"))
                yield pantry_items, has_next
            except ValidationError as e:
                raise ServerError("Failed to parse culinary ingredient specifications response data") from e

            # If we're only fetching a specific page, stop after yielding it
            if not fetch_all_pages:
                break

            # Otherwise, continue to next page if it exists
            if not has_next:
                break

            current_page += 1
        return

    def get_recipe_pantry_item_data(
        self,
        item_ids: list[int],
    ) -> dict[int, PantryItemStatus]:
        if not item_ids:
            return {}

        token = self._get_culops_token()
        page: int = 1

        url = f"https://{self.host}{self.api_path}/culinary-ingredient-specifications"

        item_statuses: dict[int, PantryItemStatus] = {}

        params: dict[str, str | int] = {
            "filter[id]": ",".join(map(str, item_ids)),
            "include": "culinary-ingredient,culinary-ingredient-specification-costs",
            "page[number]": page,
            "page[size]": self.fetch_size,
        }

        try:
            while True:
                res = self.session.get(url=url, headers={"Authorization": f"Bearer {token}"}, params=params)
                res.raise_for_status()

                res_json = res.json()

                try:
                    culops_pantry_data = CulopsData.model_validate(res_json)
                except ValidationError as e:
                    raise ServerError("Failed to parse culinary ingredient specifications response data") from e
                included = culops_pantry_data.included
                data = culops_pantry_data.data

                for item in data:
                    availabilities = []

                    item_ingredient_id = item.relationships.culinary_ingredient.data.id
                    ingredients = list(filter(lambda i: i.id == item_ingredient_id, included))
                    ingredient = ingredients[0]

                    if not ingredient:
                        raise ValueError(f"Culops data missing culinary-ingredient: {item_ingredient_id}")

                    is_prepped_and_ready = ingredient.attributes.category.lower() == PREPPED_AND_READY_CATEGORY

                    availability_data = item.relationships.culinary_ingredient_specification_availabilities
                    if availability_data:
                        for availability in availability_data.data:
                            availability_id = availability.id
                            if availability_id in included:
                                pantry_item_availability = PantryItemAvailability(
                                    available_from=included[availability_id].get("available_from"),
                                    available_until=included[availability_id].get("available_until"),
                                )
                                availabilities.append(pantry_item_availability)

                    item_statuses[int(item.id)] = PantryItemStatus(
                        availabilities=availabilities,
                        is_prepped_and_ready=is_prepped_and_ready,
                    )

                if not res_json.get("links", {}).get("next"):
                    break

                page += 1

            return item_statuses

        except HTTPError as e:
            err_msg = f"failed to fetch culinary ingredient specifications for items {item_ids}"
            if getattr(e, "response", None) is not None:
                status_code = e.response.status_code
                message = e.response.text
                err_msg += f" with status code {status_code} and message: {message}"
            raise ServerError(err_msg) from e

    def create_recipe(
        self,
        cycle_date: datetime,
        title: str,
        servings: int,
        recipe_plan_name: str,
        recipe_short_code: str,
        recipe_card_id: str | None = None,
        badge_tags: list[str] | None = None,
        campaign_tags: list[str] | None = None,
        subtitle: str | None = None,
    ) -> CreateCulopsRecipeResponse:
        cycle_date_day = cycle_date.strftime("%Y-%m-%d")
        cycle_id = self._get_culops_cycle_id(cycle_date_day)

        token = self._get_culops_token()
        url = f"https://{self.host}{self.api_path}/recipes"

        attributes: dict[str, object] = {
            "cycle-date": cycle_date.strftime("%Y-%m-%d"),
            "title": title,
            "servings": servings,
            "recipe-slot-plan": recipe_plan_name.value if isinstance(recipe_plan_name, Enum) else recipe_plan_name,
            "recipe-slot-short-code": recipe_short_code,
        }

        if subtitle:
            attributes["sub-title"] = subtitle

        if badge_tags:
            attributes["badge-tag-list"] = badge_tags

        if campaign_tags:
            attributes["campaign-tag-list"] = campaign_tags

        data: dict[str, object] = {
            "type": "recipes",
            "attributes": attributes,
        }
        try:
            payload = {"data": data}
            res = self.session.post(
                url=url,
                headers={
                    "Authorization": f"Bearer {token}",
                    "Content-Type": "application/vnd.api+json",
                },
                json=payload,
            )
            res.raise_for_status()
        except HTTPError as e:
            if getattr(e, "response", None) is not None:
                status_code = e.response.status_code
                message = e.response.text
                if 400 <= status_code < 500:
                    raise ValueError(f"Failed to create recipe {title} invalid create request: {message}") from e
            raise ServerError(f"Failed to create recipe {title}") from e

        res_json = res.json()

        recipe_id = res_json.get("data", {}).get("id")
        recipe_sku = res_json.get("data", {}).get("attributes", {}).get("sku")
        if not recipe_id or not recipe_sku:
            raise ServerError(f"Failed to correctly parse create recipe response for {title}: {res_json}")

        try:
            self._set_recipe_cycle(recipe_id, cycle_id)
        except RecipeNotFoundError as e:
            raise ServerError(f"Recipe {title} not found for cycle assignment") from e
        except ServerError as e:
            try:
                self.delete_recipe(recipe_id)
            except ServerError as e:
                raise ServerError(f"Failed to delete recipe {title} after failed cycle assignment") from e
            raise ServerError(f"Failed to set recipe cycle for recipe {title}") from e

        return CreateCulopsRecipeResponse(recipe_id=recipe_id, recipe_sku=recipe_sku)

    def add_recipe_ingredients(
        self,
        recipe_id: int,
        ingredients: list[PantryItemCulinaryIngredientSpecification],
    ) -> list[str]:
        token = self._get_culops_token()
        url = f"https://{self.host}{self.api_path}/ingredients"

        created_ids = []

        for ingredient in ingredients:
            culinary_ingredient_id = ingredient.culops_culinary_ingredient_id
            culinary_ingredient_specification_id = ingredient.culops_culinary_ingredient_specification_id

            try:
                res = self.session.post(
                    url=url,
                    headers={"Authorization": f"Bearer {token}", "Content-Type": "application/vnd.api+json"},
                    json={
                        "data": {
                            "type": "ingredients",
                            "relationships": {
                                "culinary-ingredient": {
                                    "data": {"type": "culinary-ingredients", "id": culinary_ingredient_id}
                                },
                                "culinary-ingredient-specification": {
                                    "data": {
                                        "type": "culinary-ingredient-specifications",
                                        "id": culinary_ingredient_specification_id,
                                    }
                                },
                                "recipe": {"data": {"type": "recipes", "id": recipe_id}},
                            },
                        }
                    },
                )

                res.raise_for_status()
                res_json = res.json()

            except HTTPError as e:
                status_code = e.response.status_code if getattr(e, "response", None) else None
                response_text = e.response.text if getattr(e, "response", None) else "No response"
                if status_code == 404:
                    raise RecipeNotFoundError(f"Recipe with ID {recipe_id} not found.") from e
                err_msg = f"Failed to create culops recipe ingredient {culinary_ingredient_id}"
                err_msg += f" (cul_ing_spec_id: {culinary_ingredient_specification_id}, recipe_id: {recipe_id})"
                if status_code:
                    err_msg += f" - Status {status_code}: {response_text}"
                logger.error(
                    f"Culops ingredient creation failed: {err_msg}",
                    extra={
                        "culinary_ingredient_id": culinary_ingredient_id,
                        "culinary_ingredient_specification_id": culinary_ingredient_specification_id,
                        "recipe_id": recipe_id,
                        "status_code": status_code,
                        "response": response_text,
                    },
                )
                raise ServerError(err_msg) from e

            if "data" not in res_json:
                raise RuntimeError("Invalid response structure: Missing 'data' field.")

            res_data = res_json.get("data", {})
            created_id = res_data.get("id")
            if created_id:
                created_ids.append(created_id)

        return created_ids

    def get_recipe(
        self,
        culops_recipe_id: int,
        partner_id: str,
    ) -> CulopsRecipe:
        if not culops_recipe_id:
            raise ValueError("Failed to get culops recipe, culops recipe_id required.")
        recipes = self._get_recipes(partner_id=partner_id, recipe_ids=[culops_recipe_id])
        if not recipes:
            raise RecipeNotFoundError(f"CulOps recipe {culops_recipe_id} not found", recipe_id=culops_recipe_id)
        return recipes[0]

    def get_cycle_recipes_by_plan(self, partner_id: str, cycle_date: datetime, plan_name: str) -> list[CulopsRecipe]:
        if not validate_cycle_datetime(cycle_date):
            raise ValueError(f"Cycle date {cycle_date} must be a Monday")
        if not plan_name:
            raise ValueError("Failed to get cycle recipes by plan, plan_name required.")
        return self._get_recipes(partner_id=partner_id, cycle_date=cycle_date, plan_name=plan_name)

    def get_cycle_recipes(
        self, partner_id: str, cycle_date: datetime, recipe_ids: list[int] | None = None
    ) -> list[CulopsRecipe]:
        if not validate_cycle_datetime(cycle_date):
            raise ValueError(f"Cycle date {cycle_date} must be a Monday")

        recipes = self._get_recipes(partner_id=partner_id, cycle_date=cycle_date, recipe_ids=recipe_ids)

        if recipe_ids:
            recipe_ids_returned = [r.culops_recipe_id for r in recipes]
            for rid in recipe_ids:
                if str(rid) not in recipe_ids_returned:
                    raise RecipeNotFoundError(f"CulOps recipe {rid} not found", recipe_id=rid)

        return recipes

    def get_available_recipe_slots(self, plan_name: str) -> list[str]:
        """Get all available recipe slot codes from Culops for a given plan."""
        token = self._get_culops_token()
        url = f"https://{self.host}{self.api_path}/recipe-slots"
        params = {"page[size]": 1000}
        headers = {"Authorization": f"Bearer {token}"}

        try:
            res = self.session.get(url=url, headers=headers, params=params, timeout=15)
            res.raise_for_status()
            res_json = res.json()
        except HTTPError as e:
            raise ServerError(f"Failed to fetch recipe slots from Culops: HTTP {e.response.status_code}") from e
        except RequestException as e:
            raise ServerError(f"Failed to fetch recipe slots from Culops: {e}") from e

        # Extract slot codes for the specified plan
        slot_codes = []
        for slot in res_json.get("data", []):
            attrs = slot.get("attributes", {})
            if attrs.get("plan-description") == plan_name:
                slot_codes.append(attrs.get("short-code"))

        return sorted([code for code in slot_codes if code])

    def delete_recipe(
        self,
        recipe_id: int,
    ) -> None:
        if not recipe_id:
            raise ValueError("Failed to delete culops recipe, culops recipe_id required.")

        token = self._get_culops_token()

        deactivate_url = f"https://{self.host}{self.api_path}/recipes/{recipe_id}"
        deactivate_body = {
            "data": {
                "id": f"{recipe_id}",
                "type": "recipes",
                "attributes": {
                    "cycle-date": None,
                    "recipe-slot-short-code": None,
                },
            },
        }

        headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/vnd.api+json",
            "Accept": "application/vnd.api+json",
        }

        try:
            deactivate_res = self.session.patch(url=deactivate_url, headers=headers, json=deactivate_body)
            deactivate_res.raise_for_status()
        except HTTPError as e:
            assert isinstance(e.response.status_code, int)
            status = e.response.status_code
            msg = e.response.text if e.response else ""
            if status == 404:
                raise RecipeNotFoundError(f"CulOps recipe {recipe_id} not found for deactivation") from e
            if 400 <= status < 500:
                raise ValueError(
                    f"CulOps rejected deactivation request for recipe {recipe_id}: [{status}] {msg}"
                ) from e
            raise ServerError(f"Failed to deactivate recipe {recipe_id} in CulOps (status {status}) - {msg}") from e
        except RequestException as e:
            raise ServerError(f"Failed to deactivate recipe {recipe_id} in CulOps") from e

        archive_token = self._get_culops_token()

        archive_url = f"https://{self.host}{self.api_path}/recipes/{recipe_id}/archive"

        try:
            archive_res = self.session.put(url=archive_url, headers={"Authorization": f"Bearer {archive_token}"})
            archive_res.raise_for_status()
        except HTTPError as e:
            assert isinstance(e.response.status_code, int)
            status = e.response.status_code
            msg = e.response.text if e.response else ""
            if status == 404:
                raise RecipeNotFoundError(f"CulOps recipe {recipe_id} not found for archiving") from e
            if 400 <= status < 500:
                raise ValueError(f"CulOps rejected archiving request for recipe {recipe_id}: [{status}] {msg}") from e
            raise ServerError(f"Failed to archive recipe {recipe_id} in CulOps (status {status}) - {msg}") from e
        except RequestException as e:
            raise ServerError(f"Failed to archive recipe {recipe_id} in CulOps") from e

    def update_recipe(
        self,
        recipe_id: int,
        title: str | None = None,
        subtitle: str | None = None,
        badge_tags: list[str] | None = None,
        campaign_tags: list[str] | None = None,
    ) -> tuple[Recipe, list[str], list[str]]:
        token = self._get_culops_token()

        url = f"https://{self.host}{self.api_path}/recipes/{recipe_id}"
        attributes = {
            k: v
            for k, v in {
                "title": title,
                "sub-title": subtitle,
                "badge-tag-list": badge_tags,
                "campaign-tag-list": campaign_tags,
            }.items()
            if v is not None
        }

        try:
            data = {
                "id": recipe_id,
                "type": "recipes",
                "attributes": attributes,
            }
            payload = {"data": data}
            res = self.session.patch(
                url=url,
                headers={
                    "Authorization": f"Bearer {token}",
                    "Content-Type": "application/vnd.api+json",
                },
                json=payload,
            )
            res.raise_for_status()
            res_json = res.json()

            recipe = CulopsRecipeUpdateResponse.model_validate(res_json)
        except HTTPError as e:
            assert isinstance(e.response.status_code, int)
            status = e.response.status_code
            if status in (404, 410):
                raise RecipeNotFoundError("CulOps recipe request failed, not found") from e
            if 400 <= status < 500:
                raise ValueError(
                    f"CulOps recipe request failed: [{status}] {e.response.text if e.response else ''}"
                ) from e
            raise ServerError(f"Failed to fetch recipes from CulOps (status {status})") from e
        except RequestException as e:
            raise ServerError("Failed to fetch recipes from CulOps") from e
        except ValidationError as e:
            raise ServerError("Failed to parse recipes response data") from e

        badge_tag_list = recipe.data.attributes.badge_tag_list
        campaign_tag_list = recipe.data.attributes.campaign_tag_list
        raw_title = recipe.data.attributes.title
        raw_subtitle = recipe.data.attributes.sub_title

        return (
            Recipe(
                recipe_id=recipe.data.id,
                partner_id="",
                title=raw_title,
                subtitle=raw_subtitle if isinstance(raw_subtitle, str) else None,
                add_on="AD" in recipe.data.attributes.recipe_slot_short_code,
                cycle_date=recipe.data.attributes.cycle_date,
                servings=recipe.data.attributes.servings,
                pantry_items=[],
                recipe_constraint_tags=[],
                packaging_configuration_tags=[],
                recipe_card_assignments=[],
                deleted_at=None,
            ),
            badge_tag_list,
            campaign_tag_list,
        )

    def remove_recipe_ingredients(self, recipe_id: int, ingredient_ids: list[str]) -> None:
        token = self._get_culops_token()
        url = f"https://{self.host}{self.api_path}/recipes/{recipe_id}/delete_ingredients"

        data = {
            "ingredient_ids": ingredient_ids,
        }

        try:
            res = self.session.delete(url=url, headers={"Authorization": f"Bearer {token}"}, json=data)
            res.raise_for_status()
        except HTTPError as e:
            if getattr(e, "response", None) is not None:
                status_code = e.response.status_code
                message = e.response.text
                if status_code == 404:
                    raise RecipeNotFoundError(f"CulOps recipe {recipe_id} not found") from e
                if 400 <= status_code < 500:
                    raise ValueError(f"Failed to remove recipe ingredients from CulOps: {message}") from e
            raise ServerError("Failed to remove recipe ingredients from CulOps") from e

    def _get_culops_token(self) -> str:
        return self.token_svc.get_token(TokenName.CUL_OPS_ACCESS_TOKEN)

    def _get_culops_cycle_id(self, cycle_date: str) -> str:
        token = self._get_culops_token()
        url = f"https://{self.host}{self.api_path}/cycles"
        params = {"filter[cycle-date]": cycle_date}
        try:
            res = self.session.get(url=url, headers={"Authorization": f"Bearer {token}"}, params=params)
            res.raise_for_status()
            res_json = res.json()
        except HTTPError as e:
            assert isinstance(e.response.status_code, int)
            status = e.response.status_code
            if 400 <= status < 500:
                raise ValueError(
                    f"CulOps cycle request failed: [{status}] {e.response.text if e.response else ''}"
                ) from e
            raise ServerError(f"Failed to fetch cycles from CulOps (status {status})") from e
        except RequestException as e:
            raise ServerError("Failed to fetch cycles from CulOps") from e

        data = res_json.get("data")
        if not isinstance(data, list) or not data or not isinstance(data[0], dict) or "id" not in data[0]:
            raise ValueError(f"CulOps cycle not found for date {cycle_date}")
        return str(data[0]["id"])

    def _set_recipe_cycle(self, recipe_id: int, cycle_id: str) -> None:
        token = self._get_culops_token()
        url = f"https://{self.host}{self.api_path}/recipes/{recipe_id}/relationships/cycles"
        headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/vnd.api+json",
        }
        payload = {"data": [{"type": "cycles", "id": str(cycle_id)}]}

        try:
            res = self.session.post(url=url, headers=headers, json=payload)
            res.raise_for_status()
        except HTTPError as e:
            assert isinstance(e.response.status_code, int)
            status = e.response.status_code
            msg = e.response.text if e.response else ""
            if status == 404:
                raise RecipeNotFoundError(f"CulOps recipe {recipe_id} not found for cycle assignment") from e
            else:
                raise ServerError(
                    f"Failed to set cycle for recipe {recipe_id} in CulOps (status {status}) - {msg}"
                ) from e
        except RequestException as e:
            raise ServerError(f"Failed to set cycle for recipe {recipe_id} in CulOps") from e

    def _get_recipes(
        self,
        partner_id: str,
        cycle_date: datetime | None = None,
        recipe_ids: list[int] | None = None,
        plan_name: str | None = None,
    ) -> list[CulopsRecipe]:
        token = self._get_culops_token()
        url = f"https://{self.host}{self.api_path}/recipes"
        params: dict[str, str] = {"include": "ingredients.culinary-ingredient-specification"}
        if cycle_date is not None:
            params["filter[cycle-date]"] = cycle_date.strftime("%Y-%m-%d")
        if plan_name is not None:
            params["filter[recipe-slot-plan]"] = plan_name
        if recipe_ids:
            # Major requirement: explicit logging of applying recipe_ids to params
            params_before = params.copy()
            for rid in recipe_ids:
                params.setdefault("filter[id][]", str(rid))
            log.info(
                "culops list recipes: applying id filters",
                extra={
                    "partner_id": partner_id,
                    "recipe_ids": list(map(int, recipe_ids)),
                    "params_before": params_before,
                    "params_after": params,
                },
            )
            if rollbar:
                try:
                    rollbar.report_message(
                        "culops list recipes: applying id filters",
                        level="info",
                        extra_data={
                            "partner_id": partner_id,
                            "recipe_ids": list(map(int, recipe_ids)),
                            "params_after": params,
                        },
                    )
                except Exception:
                    # Never block request on telemetry
                    pass

        try:
            res = self.session.get(url=url, headers={"Authorization": f"Bearer {token}"}, params=params)
            res.raise_for_status()
            res_json = res.json()

            recipes_response = CulopsRecipeListResponse.model_validate(res_json)
        except HTTPError as e:
            assert isinstance(e.response.status_code, int)
            status = e.response.status_code
            if 400 <= status < 500:
                raise ValueError(
                    f"CulOps recipe request failed: [{status}] {e.response.text if e.response else ''}"
                ) from e
            raise ServerError(f"Failed to fetch recipes from CulOps (status {status})") from e
        except RequestException as e:
            raise ServerError("Failed to fetch recipes from CulOps") from e
        except ValidationError as e:
            raise ServerError("Failed to parse recipes response data") from e

        included = recipes_response.included or []
        included_lookup = {(item.type, item.id): item for item in included}

        if recipe_ids:
            recipe_ids_returned = [r.id for r in recipes_response.data]
            for rid in recipe_ids:
                if str(rid) not in recipe_ids_returned:
                    raise RecipeNotFoundError(f"CulOps recipe {rid} not found", recipe_id=rid)

        results: list[CulopsRecipe] = []
        for item in recipes_response.data:
            culops_recipe_id = int(item.id)
            attributes = item.attributes

            recipe_uuid = self.recipe_repo.get_recipe_id_by_culops_recipe_id(culops_recipe_id)
            if not recipe_uuid:
                recipe_uuid = uuid4()
                self.recipe_repo.store_recipe_source(partner_id, recipe_uuid, int(item.id), item.attributes.sku, True)

            pantry_item_data_source_ids: list[tuple[int, int]] = []
            ingredients_rel = item.relationships.ingredients
            if ingredients_rel and ingredients_rel.data and isinstance(ingredients_rel.data, list):
                for ingredient_rel in ingredients_rel.data:
                    ingredient_id = ingredient_rel.id
                    inc_ingredient = included_lookup.get(("ingredients", ingredient_id))

                    if (
                        inc_ingredient
                        and isinstance(inc_ingredient.relationships, IngredientRelationships)
                        and isinstance(
                            inc_ingredient.relationships.culinary_ingredient_specification.data, ResourceIdentifier
                        )
                    ):
                        spec_inc_id = inc_ingredient.relationships.culinary_ingredient_specification.data.id

                        spec_inc = included_lookup.get(("culinary-ingredient-specifications", spec_inc_id))

                        if spec_inc and isinstance(
                            spec_inc.relationships, CulinaryIngredientSpecificationRelationships
                        ):
                            pantry_item_data_source_ids.append(
                                (int(spec_inc.id), spec_inc.attributes.culinary_ingredient_id)
                            )

            recipe_pantry_items_data: list[CulopsRecipePantryItemData] = []
            for culinary_specification_id, culinary_ingredient_id in pantry_item_data_source_ids:
                pantry_item_data = (
                    self.pantry_repo.get_pantry_item_data_by_culops_culinary_ingredient_and_specification_id(
                        culinary_specification_id, culinary_ingredient_id
                    )
                )

                if pantry_item_data:
                    culops_recipe_pantry_item_data = CulopsRecipePantryItemData(
                        pantry_item_id=pantry_item_data.pantry_item_id,
                        is_prepped_and_ready=pantry_item_data.is_prepped_and_ready,
                        ingredient_id=ingredient_id,
                    )
                    recipe_pantry_items_data.append(culops_recipe_pantry_item_data)
                else:
                    # See note in original code re: archived specs/ingredients.
                    cul_spec_ingredient = included_lookup.get(
                        ("culinary-ingredient-specifications", culinary_specification_id)
                    )
                    cul_spec_archived = cul_spec_ingredient and cul_spec_ingredient.attributes.is_archived

                    cul_ingredient = included_lookup.get(("culinary-ingredients", culinary_ingredient_id))
                    cul_ingredient_archived = cul_ingredient and cul_ingredient.attributes.is_archived

                    possible_issue_msg = "."
                    possible_issue_msgs: list[str] = []
                    if cul_spec_archived:
                        possible_issue_msgs.append(
                            f"Culinary ingredient specification {culinary_specification_id} is archived"
                        )
                    if cul_ingredient_archived:
                        possible_issue_msgs.append(f"Culinary ingredient {culinary_ingredient_id} is archived")
                    if possible_issue_msgs:
                        possible_issue_msg = ": " + " , ".join(possible_issue_msgs)

                    log.error(
                        f"Failed to match recipe {culops_recipe_id} ingredient "
                        f"{culinary_ingredient_id} with specification "
                        f"{culinary_specification_id} to pantry item data{possible_issue_msg}"
                    )

            badge_tags = set(attributes.badge_tag_list)
            campaign_tags = set(attributes.campaign_tag_list)

            partner_constraint_tags = self.partner_repo.get_partner_recipe_constraint_tags(partner_id)
            partner_packaging_config_tags = self.partner_repo.get_partner_packaging_configuration_tags(partner_id)

            badge_constraint_tags = self._match_recipe_constraint_tags(
                badge_tags, partner_constraint_tags, TagListType.BADGE_TAG_LIST
            )

            remaining_badge = badge_tags - set(badge_constraint_tags.keys())

            badge_packaging_configuration_tags = self._match_recipe_packaging_configuration_tags(
                remaining_badge, partner_packaging_config_tags, TagListType.BADGE_TAG_LIST
            )

            unmatched_recipe_badge_tags = (
                badge_tags - set(badge_constraint_tags.keys()) - set(badge_packaging_configuration_tags.keys())
            )

            for badge_tag in unmatched_recipe_badge_tags:
                log.warning(f"Unmatched recipe {item.id} badge tag: {badge_tag}")

            campaign_constraint_tags = self._match_recipe_constraint_tags(
                campaign_tags, partner_constraint_tags, TagListType.CAMPAIGN_TAG_LIST
            )

            remaining_campaign = campaign_tags - set(campaign_constraint_tags.keys())

            campaign_packaging_configuration_tags = self._match_recipe_packaging_configuration_tags(
                remaining_campaign, partner_packaging_config_tags, TagListType.CAMPAIGN_TAG_LIST
            )

            unmatched_recipe_campaign_tags = (
                campaign_tags - set(campaign_constraint_tags.keys()) - set(campaign_packaging_configuration_tags.keys())
            )

            for campaign_tag in unmatched_recipe_campaign_tags:
                log.warning(f"Unmatched recipe {item.id} campaign tag: {campaign_tag}")

            constraint_tags = list(badge_constraint_tags.values()) + list(campaign_constraint_tags.values())

            packaging_configuration_tags = list(badge_packaging_configuration_tags.values()) + list(
                campaign_packaging_configuration_tags.values()
            )

            recipe_card_assignments = [RecipeCardAssignment(card_id=cid) for cid in attributes.recipe_card_ids]
            recipe_cycle_date = datetime.strptime(attributes.cycle_date, "%Y-%m-%d")
            add_on = "AD" in (attributes.recipe_slot_short_code or "")

            results.append(
                CulopsRecipe(
                    partner_id=partner_id,
                    recipe_id=recipe_uuid,
                    culops_recipe_id=culops_recipe_id,
                    title=attributes.title,
                    subtitle=attributes.sub_title,
                    add_on=add_on,
                    cycle_date=recipe_cycle_date,
                    servings=attributes.servings,
                    pantry_items=recipe_pantry_items_data,
                    recipe_constraint_tags=constraint_tags,
                    packaging_configuration_tags=packaging_configuration_tags,
                    recipe_card_assignments=recipe_card_assignments,
                    recipe_slot_plan=attributes.recipe_slot_plan,
                    recipe_slot_short_code=attributes.recipe_slot_short_code,
                )
            )

        return results

    @staticmethod
    def _map_pantry_items(
        culops_data: CulopsData,
        available_from: datetime | None,
        available_until: datetime | None,
    ) -> list[PantryItem]:
        pantry_items: list[PantryItem] = []
        included_lookup = {(item.type, item.id): item for item in culops_data.included or []}

        items_with_cost_rels = 0
        items_without_cost_rels = 0
        items_using_fallback = 0

        for item in culops_data.data:
            brand_name: str | None = ""
            availabilities: list[PantryItemAvailability] = []
            costs: list[PantryItemCost] = []
            custom_field_data: list[PantryItemCustomField] = []

            if not item.relationships or not item.relationships.culinary_ingredient:
                continue
            ingredient_ref = item.relationships.culinary_ingredient.data
            ingredient = included_lookup.get((ingredient_ref.type, ingredient_ref.id))
            if not ingredient:
                raise ValueError(
                    f"Culops data missing culinary-ingredient: "
                    f"{item.relationships.culinary_ingredient.data.id} for "
                    f"culinary-ingredient-specification: {item.id}"
                )
            description = ingredient.attributes.display_name if ingredient.attributes.display_name else "Unknown"
            category = ingredient.attributes.category.strip().lower()

            # Use cost relationship data if available, otherwise fallback to attributes.cost
            if item.relationships.culinary_ingredient_specification_costs and item.relationships.culinary_ingredient_specification_costs.data:
                items_with_cost_rels += 1
                item_cost_ids = [
                    cost.id
                    for cost in item.relationships.culinary_ingredient_specification_costs.data
                    if cost.type == "culinary-ingredient-specification-costs"
                ]
                item_costs = [
                    included_lookup.get(("culinary-ingredient-specification-costs", cost_id)) for cost_id in item_cost_ids
                ]
                # Don't filter by date - return all costs regardless of cycle date
                valid_item_costs = [
                    cost
                    for cost in item_costs
                    if cost is not None
                    and isinstance(cost.attributes, CulinaryIngredientSpecificationCostAttribute)
                ]

                # Convert all available costs without date range filtering
                for cost in valid_item_costs:
                    cycle_start = cost.attributes.get_cycle_start_date()
                    costs.append(
                        PantryItemCost(
                            production_cost_us_dollars=cost.attributes.cost,
                            start_date=cycle_start,
                            end_date=cycle_start + timedelta(days=7),
                        )
                    )
            else:
                items_without_cost_rels += 1

            # Fallback to item.attributes.cost if no cost relationships
            if not costs and item.attributes.cost is not None:
                items_using_fallback += 1
                costs.append(
                    PantryItemCost(
                        production_cost_us_dollars=item.attributes.cost,
                        start_date=datetime.now(UTC),
                        end_date=datetime.now(UTC) + timedelta(days=7),
                    )
                )

            if item.relationships.culinary_ingredient_specification_availabilities:
                for availability_ref in item.relationships.culinary_ingredient_specification_availabilities.data:
                    availability_entry = included_lookup.get((availability_ref.type, availability_ref.id))
                    if availability_entry:
                        availability_attr = availability_entry.attributes
                        availabilities.append(
                            PantryItemAvailability(
                                available_until=parse_to_datetime(availability_attr.end)
                                if availability_attr.end
                                else None,
                                available_from=parse_to_datetime(availability_attr.start)
                                if availability_attr.start
                                else None,
                            )
                        )

            if item.custom_fields:
                for custom_field in item.custom_fields:
                    custom_field_data.append(
                        PantryItemCustomField(
                            key=custom_field.key,
                            value=custom_field.value,
                        )
                    )

            if item.relationships and item.relationships.culinary_ingredient_brand:
                brand_ref = item.relationships.culinary_ingredient_brand.data
                included_item = included_lookup.get((brand_ref.type, brand_ref.id))

                if included_item and isinstance(included_item.attributes, CulinaryIngredientBrand):
                    brand_name = included_item.attributes.name

            is_prepped_and_ready = category == PREPPED_AND_READY_CATEGORY

            pantry_item = PantryItem(
                id=str(uuid4()),
                description=description,
                amount=item.attributes.amount,
                units=item.attributes.unit,
                availability=availabilities,
                cost=costs,
                custom_fields=custom_field_data,
                is_prepped_and_ready=is_prepped_and_ready,
                pantry_item_data_source=PantryItemDataSource(
                    culops_culinary_ingredient_id=int(ingredient.id if ingredient else "0"),
                    culops_culinary_ingredient_specification_id=int(item.id),
                ),
                brand_name=brand_name,
            )

            pantry_items.append(pantry_item)

        log.info(
            f"_map_pantry_items: processed {len(culops_data.data)} items from CulOps, "
            f"returning {len(pantry_items)} items",
            extra={
                "culops_items_count": len(culops_data.data),
                "items_with_cost_rels": items_with_cost_rels,
                "items_without_cost_rels": items_without_cost_rels,
                "items_using_fallback": items_using_fallback,
                "returned_items": len(pantry_items),
            },
        )

        return pantry_items

    @staticmethod
    def _match_recipe_constraint_tags(
        recipe_tags: set[str],
        partner_constraint_tags: list[RecipeConstraintTag],
        match_tag_type: TagListType,
    ) -> dict[str, RecipeConstraintTag]:
        constraint_tags: dict[str, RecipeConstraintTag] = {}
        for tag in recipe_tags:
            for partner_constraint_tag in partner_constraint_tags:
                if (
                    partner_constraint_tag.tag_type == match_tag_type
                    and partner_constraint_tag.tag_value.lower() == tag.lower()
                ):
                    constraint_tags[tag] = partner_constraint_tag
                    break

        return constraint_tags

    @staticmethod
    def _match_recipe_packaging_configuration_tags(
        recipe_tags: set[str],
        partner_packaging_config_tags: list[PackagingConfigurationTag],
        match_tag_type: TagListType,
    ) -> dict[str, PackagingConfigurationTag]:
        packaging_configuration_tags: dict[str, PackagingConfigurationTag] = {}
        for tag in recipe_tags:
            for partner_packaging_config_tag in partner_packaging_config_tags:
                if (
                    partner_packaging_config_tag.tag_type == match_tag_type
                    and partner_packaging_config_tag.tag_value.lower() == tag.lower()
                ):
                    packaging_configuration_tags[tag] = partner_packaging_config_tag
                    break
        return packaging_configuration_tags
