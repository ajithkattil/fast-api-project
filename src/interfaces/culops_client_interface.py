from collections.abc import Iterator
from datetime import datetime
from typing import Protocol

from src.services.models.pantry import PantryItem, PantryItemCulinaryIngredientSpecification, PantryItemStatus
from src.services.models.recipe import CreateCulopsRecipeResponse, CulopsRecipe, Recipe


class CulopsClientInterface(Protocol):
    def get_partner_culops_pantry_data(
        self,
        available_from: datetime | None = None,
        available_until: datetime | None = None,
        partner_id: str = "",
        brand_name: str = "",
        page: int | None = None,
        page_size: int | None = None,
    ) -> Iterator[tuple[list[PantryItem], bool]]: ...

    def get_recipe_pantry_item_data(
        self,
        item_ids: list[int],
    ) -> dict[int, PantryItemStatus]: ...

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
    ) -> CreateCulopsRecipeResponse: ...

    def add_recipe_ingredients(
        self,
        recipe_id: int,
        ingredients: list[PantryItemCulinaryIngredientSpecification],
    ) -> list[str]: ...

    def get_recipe(
        self,
        recipe_id: int,
        partner_id: str,
    ) -> CulopsRecipe: ...

    def get_cycle_recipes_by_plan(
        self, partner_id: str, cycle_date: datetime, plan_name: str
    ) -> list[CulopsRecipe]: ...

    def get_cycle_recipes(
        self, partner_id: str, cycle_date: datetime, recipe_ids: list[int] | None = None
    ) -> list[CulopsRecipe]: ...

    def get_available_recipe_slots(self, plan_name: str) -> list[str]: ...

    def update_recipe(
        self,
        recipe_id: int,
        title: str | None,
        subtitle: str | None,
        badge_tags: list[str] | None,
        campaign_tags: list[str] | None,
    ) -> tuple[Recipe, list[str], list[str]]: ...

    def remove_recipe_ingredients(self, recipe_id: int, items_to_remove: list[str]) -> None: ...

    def delete_recipe(
        self,
        recipe_id: int,
    ) -> None: ...
