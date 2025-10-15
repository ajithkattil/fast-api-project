from datetime import datetime
from uuid import UUID

from src.core.exceptions import NotFoundException
from src.interfaces.pantry_db_interface import PantryDBInterface
from src.services.models.pantry import Pantry, PantryItem, PantryItemCulinaryIngredientSpecification
from src.services.models.recipe import RecipePantryItemData
from src.utils.generate_pantry_mocks import generate_mock_pantry_items


class MockPantryDB(PantryDBInterface):
    def __init__(self) -> None:
        self.mock_data: list[Pantry] = [
            Pantry(
                pantry_state_id="12345",
                pantry_items=generate_mock_pantry_items(),
                partner_id="123",
                pantry_state_timestamp=datetime.now(),
                ingredients_available_from=None,
                ingredients_available_until=None,
                partner_cost_markup=[],
            ),
            Pantry(
                pantry_state_id="67890",
                pantry_items=generate_mock_pantry_items(),
                partner_id="456",
                pantry_state_timestamp=datetime.now(),
                ingredients_available_from=None,
                ingredients_available_until=None,
                partner_cost_markup=[],
            ),
            Pantry(
                pantry_state_id="12345",
                pantry_items=generate_mock_pantry_items(),
                partner_id="BA-MAIN",
                pantry_state_timestamp=datetime.now(),
                ingredients_available_from=None,
                ingredients_available_until=None,
                partner_cost_markup=[],
            ),
        ]

    def get_partner_pantry_by_id(
        self,
        pantry_state_id: str | UUID,
        partner_id: str,
        page_size: int,
        page: int = 1,
    ) -> tuple[Pantry | None, int]:
        if not isinstance(pantry_state_id, str):
            pantry_state_id = str(pantry_state_id)

        pantry = next(
            (p for p in self.mock_data if p.pantry_state_id == pantry_state_id and p.partner_id == partner_id),
            None,
        )
        if not pantry:
            raise NotFoundException(f"No pantry found with id: {pantry_state_id}")

        total_count = len(pantry.pantry_items)
        offset = (page - 1) * page_size
        paginated_items = pantry.pantry_items[offset : offset + page_size]

        paginated_pantry = Pantry(
            pantry_state_id=pantry.pantry_state_id,
            pantry_items=paginated_items,
            partner_id=pantry.partner_id,
            pantry_state_timestamp=pantry.pantry_state_timestamp,
            ingredients_available_from=pantry.ingredients_available_from,
            ingredients_available_until=pantry.ingredients_available_until,
            partner_cost_markup=pantry.partner_cost_markup,
        )

        return paginated_pantry, total_count

    def get_pantry_item_data_sources(
        self,
        pantry_item_ids: list[str],
    ) -> dict[str, PantryItemCulinaryIngredientSpecification]:
        return {}

    def get_pantry_item_data_by_culops_culinary_ingredient_and_specification_id(
        self, culinary_ingredient_specification_id: int, culinary_ingredient_id: int
    ) -> RecipePantryItemData | None:
        return None

    def save_pantry_state(
        self,
        pantry_state_id: UUID,
        partner_id: str,
        pantry_state_timestamp: datetime,
        items_available_from: datetime | None,
        items_available_until: datetime | None,
    ) -> None:
        string_pantry_state_id = str(pantry_state_id)
        pantry = Pantry(
            pantry_state_id=string_pantry_state_id,
            pantry_items=[],
            partner_id=partner_id,
            pantry_state_timestamp=pantry_state_timestamp,
            ingredients_available_from=items_available_from,
            ingredients_available_until=items_available_until,
            partner_cost_markup=[],
        )
        self.mock_data.append(pantry)

    def save_pantry_items(self, pantry_state_id: UUID, items: list[PantryItem]) -> None:
        string_pantry_state_id = str(pantry_state_id)
        pantry = next(
            (p for p in self.mock_data if p.pantry_state_id == string_pantry_state_id),
            None,
        )
        if not pantry:
            raise NotFoundException(f"No pantry found with id: {pantry_state_id}")
        pantry.pantry_items.extend(items)

    def delete_pantry(self, pantry_state_id: UUID) -> None:
        pass
