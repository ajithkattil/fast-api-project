from datetime import datetime
from unittest.mock import MagicMock

import pytest

from src.services.models.recipe import Recipe
from src.services.recipe import RecipeSlotAssignmentService
from tests.services.fixtures.test_recipe_cycle_fixtures import (
    cabinet_data_items,
    culops_2_person_recipes,
    culops_add_ons_recipes,
    culops_prepped_and_ready_recipes,
    easy_mock_recipe,
    partner_recipe_plan_maps,
)

partner_id = "BA-MAIN"


@pytest.fixture()
def mock_partner_db() -> MagicMock:
    return MagicMock()


@pytest.fixture()
def mock_culops_client() -> MagicMock:
    return MagicMock()


@pytest.fixture()
def mock_cabinet_client() -> MagicMock:
    return MagicMock()


@pytest.fixture()
def service(
    mock_partner_db: MagicMock, mock_culops_client: MagicMock, mock_cabinet_client: MagicMock
) -> RecipeSlotAssignmentService:
    service = RecipeSlotAssignmentService(mock_partner_db, mock_culops_client, mock_cabinet_client)

    def mock_get_cycle_recipes_by_plan(partner_id: str, cycle_date: datetime, plan_name: str) -> list[Recipe]:
        if plan_name == "2-Person":
            return culops_2_person_recipes()
        elif plan_name == "Add-ons":
            return culops_add_ons_recipes()
        elif plan_name == "Prepped and Ready":
            return culops_prepped_and_ready_recipes()
        else:
            raise ValueError(f"Invalid plan name: {plan_name}")

    mock_culops_client.get_cycle_recipes_by_plan.side_effect = mock_get_cycle_recipes_by_plan
    mock_partner_db.get_partner_recipe_plan_maps.return_value = partner_recipe_plan_maps()
    mock_cabinet_client.get_recipe_slots.return_value = cabinet_data_items()
    return service


def test_get_partner_recipe_plan_slots(service: RecipeSlotAssignmentService) -> None:
    recipe = easy_mock_recipe("2-Person")
    code = service.assign_recipe_slot(recipe)

    assert code == "RE13"


def test_get_partner_recipe_plan_slots_addon(service: RecipeSlotAssignmentService) -> None:
    recipe = easy_mock_recipe("Add-ons", addon=True)
    code = service.assign_recipe_slot(recipe)

    assert code == "ADD07"


def test_get_partner_recipe_plan_slots_prepped_and_ready(service: RecipeSlotAssignmentService) -> None:
    recipe = easy_mock_recipe("Prepped and Ready")
    pantry_item = MagicMock()
    pantry_item.is_prepped_and_ready = True
    pantry_items = [pantry_item]
    recipe._pantry_items = pantry_items  # type: ignore[assignment]
    code = service.assign_recipe_slot(recipe)

    assert code == "PR07"

    with pytest.raises(Exception, match="Invalid recipe configuration for Blue Apron plan assignment"):
        pantry_item = MagicMock()
        pantry_item2 = MagicMock()
        pantry_item.is_prepped_and_ready = True
        pantry_items = [pantry_item, pantry_item2]
        recipe._pantry_items = pantry_items  # type: ignore[assignment]

        recipe = easy_mock_recipe("Prepped and Ready")
        recipe._pantry_items = pantry_items  # type: ignore[assignment]
        code = service.assign_recipe_slot(recipe)


def test_get_partner_recipe_plan_slots_no_slots(
    service: RecipeSlotAssignmentService, mock_culops_client: MagicMock, mock_cabinet_client: MagicMock
) -> None:
    slots = cabinet_data_items()[3:4]  # "V"
    c_recipes = [(easy_mock_recipe("2-Person"), "V")]
    mock_cabinet_client.get_recipe_slots.return_value = slots
    mock_culops_client.get_recipes.return_value = c_recipes

    with pytest.raises(Exception, match="No available slots for recipe"):
        recipe = easy_mock_recipe("2-Person")
        service.assign_recipe_slot(recipe)


def test_get_partner_recipe_plan_partner_id_does_not_match(service: RecipeSlotAssignmentService) -> None:
    with pytest.raises(Exception, match="Unsupported partner ID"):
        recipe = easy_mock_recipe(partner="NOT_BA_MAIN")
        service.assign_recipe_slot(recipe)
