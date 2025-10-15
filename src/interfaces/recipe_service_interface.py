from typing import Protocol, TypeVar

from pydantic import BaseModel

from src.api.routes.v1.models import RecipePatchRequest, RecipePostRequest, RecipeResponse

T = TypeVar("T", bound=BaseModel)


class RecipeServiceInterface(Protocol):
    def get_recipes(self, partner_id: str, cycle_date: str, recipe_ids: list[str] | None) -> list[RecipeResponse]: ...

    def get_all_recipes(self, partner_id: str) -> list[RecipeResponse]: ...

    def get_recipe_ids_by_skus(self, partner_id: str, product_skus: list[str]) -> list[T]: ...

    def update_recipe(
        self, partner_id: str, recipe_id: str, recipe_data: RecipePatchRequest
    ) -> RecipeResponse | None: ...

    def create_recipe(self, partner_id: str, recipe_data: RecipePostRequest) -> RecipeResponse: ...

    def delete_recipe(self, partner_id: str, recipe_id: str) -> None: ...
