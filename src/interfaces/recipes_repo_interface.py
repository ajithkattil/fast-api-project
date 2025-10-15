from collections.abc import Callable
from typing import Protocol
from uuid import UUID

from src.core.constants import RecipeStatus
from src.services.models.recipe import CulopsRecipeRef, RecipeRef


class RecipesRepoInterface(Protocol):
    def store_recipe_source(
        self,
        partner_id: str,
        recipe_id: UUID,
        culops_recipe_id: int,
        culops_product_sku: str,
        is_external: bool = False,
    ) -> None: ...

    def get_culops_recipe_ref_by_id(self, partner_id: str, recipe_id: UUID) -> CulopsRecipeRef | None: ...

    def get_recipe_sku_by_id(self, partner_id: str, recipe_id: UUID) -> tuple[str, RecipeStatus] | None: ...

    def mark_recipe_as_deleted(
        self, partner_id: str, recipe_id: UUID, pre_delete_hook: Callable[[], None] | None = None
    ) -> None: ...

    def get_recipe_id_by_culops_recipe_id(self, culops_recipe_id: int) -> UUID | None: ...

    def get_culops_recipe_ref_by_sku(self, partner_id: str, sku: str) -> RecipeRef | None: ...

    def get_culops_recipe_refs_by_skus(self, partner_id: str, skus: list[str]) -> list[RecipeRef]: ...

    def get_all_recipe_refs_by_partner(self, partner_id: str) -> list[CulopsRecipeRef]: ...
