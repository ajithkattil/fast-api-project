from datetime import datetime
from typing import Protocol
from uuid import UUID

from src.services.models.pantry import Pantry, PantryItem, PantryItemCulinaryIngredientSpecification
from src.services.models.recipe import RecipePantryItemData


class PantryDBInterface(Protocol):
    def get_partner_pantry_by_id(
        self, pantry_state_id: str, partner_id: str, page_size: int, page: int
    ) -> tuple[Pantry | None, int]: ...

    def save_pantry_state(
        self,
        pantry_state_id: UUID,
        partner_id: str,
        pantry_state_timestamp: datetime,
        items_available_from: datetime | None,
        items_available_until: datetime | None,
    ) -> None: ...

    def save_pantry_items(self, pantry_state_id: UUID, items: list[PantryItem]) -> None: ...

    def delete_pantry(self, pantry_state_id: UUID) -> None: ...

    def get_pantry_item_data_sources(
        self,
        pantry_item_ids: list[str],
    ) -> dict[UUID, PantryItemCulinaryIngredientSpecification]: ...

    def get_pantry_item_data_by_culops_culinary_ingredient_and_specification_id(
        self, culinary_ingredient_specification_id: int, culinary_ingredient_id: int
    ) -> RecipePantryItemData | None: ...
