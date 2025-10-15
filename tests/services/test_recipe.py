from collections.abc import Callable
from datetime import datetime, timedelta
from typing import Any
from unittest.mock import Mock, patch
from uuid import UUID, uuid4

import pytest

from src.api.routes.v1.models import (
    RecipeIngredient,
    RecipePatchRequest,
    RecipePostRequest,
    RecipeResponse,
    RecipeSku,
    RecipeTags,
)
from src.core.exceptions import (
    RecipeAlreadyDeletedError,
    RecipeNotFoundError,
    ServerError,
)
from src.services.models.pantry import (
    PantryItemAvailability,
    PantryItemCulinaryIngredientSpecification,
    PantryItemStatus,
)
from src.services.models.recipe import (
    CulopsRecipe,
    CulopsRecipePantryItemData,
    CulopsRecipeRef,
    PackagingConfigurationTag,
    RecipeConstraintTag,
    RecipeRef,
    TagListType,
)
from src.services.recipe import RecipeService
from src.utils.datetime_helper import parse_from_datetime
from tests.services.fixtures.test_recipe_cycle_fixtures import easy_mock_recipe

partner_id = "BA-MAIN"


@pytest.fixture
def mock_partner_repo() -> Mock:
    mock = Mock()
    mock.get_recipe_create_cutoff_days.return_value = 7
    mock.get_recipe_update_cutoff_days.return_value = 7
    mock.get_partner_recipe_constraint_tags.return_value = [
        RecipeConstraintTag(
            tag_id="600CaloriesOrLess", tag_type=TagListType.BADGE_TAG_LIST, tag_value="600 Calories Or Less"
        ),
        RecipeConstraintTag(tag_id="carbConscious", tag_type=TagListType.BADGE_TAG_LIST, tag_value="Carb Conscious"),
        RecipeConstraintTag(tag_id="wheatFree", tag_type=TagListType.BADGE_TAG_LIST, tag_value="Wheat Free"),
    ]
    mock.get_partner_packaging_configuration_tags.return_value = [
        PackagingConfigurationTag(tag_id="heatAndEat", tag_type=TagListType.CAMPAIGN_TAG_LIST, tag_value="Heat & Eat"),
        PackagingConfigurationTag(
            tag_id="preparedAndReady", tag_type=TagListType.CAMPAIGN_TAG_LIST, tag_value="Prepared And Ready"
        ),
        PackagingConfigurationTag(
            tag_id="familyStyle", tag_type=TagListType.CAMPAIGN_TAG_LIST, tag_value="Family Style"
        ),
    ]
    return mock


@pytest.fixture
def mock_pantry_repo() -> Mock:
    mock = Mock()
    mock.get_pantry_item_data_sources.return_value = {
        UUID("f47ac10b-58cc-4372-a567-0e02b2c3d479"): PantryItemCulinaryIngredientSpecification(
            pantry_item_id=UUID("f47ac10b-58cc-4372-a567-0e02b2c3d479"),
            culops_culinary_ingredient_specification_id=123,
            culops_culinary_ingredient_id=1234,
        ),
        UUID("b9a2f51c-24e3-4e2f-b2fc-9f37c0c73c4a"): PantryItemCulinaryIngredientSpecification(
            pantry_item_id=UUID("b9a2f51c-24e3-4e2f-b2fc-9f37c0c73c4a"),
            culops_culinary_ingredient_specification_id=456,
            culops_culinary_ingredient_id=4567,
        ),
        UUID("f47ac10b-58cc-4372-a567-0e02b2c3d477"): PantryItemCulinaryIngredientSpecification(
            pantry_item_id=UUID("f47ac10b-58cc-4372-a567-0e02b2c3d477"),
            culops_culinary_ingredient_specification_id=789,
            culops_culinary_ingredient_id=456,
        ),
        UUID("b9a2f51c-24e3-4e2f-b2fc-9f37c0c73c4b"): PantryItemCulinaryIngredientSpecification(
            pantry_item_id=UUID("b9a2f51c-24e3-4e2f-b2fc-9f37c0c73c4b"),
            culops_culinary_ingredient_specification_id=101112,
            culops_culinary_ingredient_id=456,
        ),
    }

    return mock


@pytest.fixture
def mock_cycle_date() -> datetime:
    cycle_date = datetime.now() + timedelta(days=60)
    days_until_monday = (7 - cycle_date.weekday()) % 7
    cycle_date += timedelta(days=days_until_monday)
    return cycle_date


@pytest.fixture
def mock_culops_client(mock_cycle_date: datetime) -> Mock:
    mock = Mock()
    mock.get_recipe_pantry_item_data.return_value = {
        123: PantryItemStatus(
            availabilities=[
                PantryItemAvailability(
                    available_from=datetime.now() - timedelta(days=1),
                    available_until=datetime.now() + timedelta(days=30),
                )
            ],
            is_prepped_and_ready=False,
        ),
        456: PantryItemStatus(
            availabilities=[
                PantryItemAvailability(
                    available_from=datetime.now() - timedelta(days=1),
                    available_until=datetime.now() + timedelta(days=30),
                )
            ],
            is_prepped_and_ready=False,
        ),
        789: PantryItemStatus(
            availabilities=[
                PantryItemAvailability(
                    available_from=datetime.now() - timedelta(days=1),
                    available_until=datetime.now() + timedelta(days=30),
                )
            ],
            is_prepped_and_ready=False,
        ),
        101112: PantryItemStatus(
            availabilities=[
                PantryItemAvailability(
                    available_from=datetime.now() - timedelta(days=1),
                    available_until=datetime.now() + timedelta(days=30),
                )
            ],
            is_prepped_and_ready=False,
        ),
    }
    from src.services.models.recipe import CreateCulopsRecipeResponse

    mock.create_recipe.return_value = CreateCulopsRecipeResponse(recipe_id=123456789, recipe_sku="123456789")
    mock.get_recipe.return_value = CulopsRecipe(
        partner_id=partner_id,
        recipe_id=uuid4(),
        culops_recipe_id=12345,
        title="test recipe",
        subtitle="test bsub title",
        servings=4,
        add_on=False,
        cycle_date=mock_cycle_date,
        recipe_constraint_tags=[],
        packaging_configuration_tags=[],
        recipe_slot_plan="2-Person",
        recipe_slot_short_code="RE01",
        recipe_card_assignments=[],
        pantry_items=[
            CulopsRecipePantryItemData(
                pantry_item_id="f47ac10b-58cc-4372-a567-0e02b2c3d479", ingredient_id="123", is_prepped_and_ready=False
            ),
            CulopsRecipePantryItemData(
                pantry_item_id="b9a2f51c-24e3-4e2f-b2fc-9f37c0c73c4a", ingredient_id="456", is_prepped_and_ready=False
            ),
        ],
    )
    return mock


@pytest.fixture
def mock_recipes_repo() -> Mock:
    mock = Mock()
    mock.get_culops_recipe_ref_by_id.return_value = Mock(
        culops_recipe_id=123456, recipe_id=UUID("caf542de-d27b-4002-ab9c-3a757e2debec"), deleted=False
    )

    return mock


@pytest.fixture
def mock_cabinet_client() -> Mock:
    return Mock()


@pytest.fixture
def recipe_service(
    mock_partner_repo: Mock,
    mock_pantry_repo: Mock,
    mock_culops_client: Mock,
    mock_recipes_repo: Mock,
    mock_cabinet_client: Mock,
) -> RecipeService:
    return RecipeService(
        partner_repo=mock_partner_repo,
        pantry_repo=mock_pantry_repo,
        recipes_repo=mock_recipes_repo,
        culops_client=mock_culops_client,
        cabinet_client=mock_cabinet_client,
    )


@pytest.fixture
def valid_recipe_post_request() -> RecipePostRequest:
    cycle_date_dt = datetime.now() + timedelta(days=15)  # More buffer to avoid cutoff conflicts
    # Calculate days until next Monday (0 = Monday, 1 = Tuesday, ..., 6 = Sunday)
    days_until_monday = (7 - cycle_date_dt.weekday()) % 7
    days_until_monday = 7 if days_until_monday == 0 else days_until_monday
    cycle_date_dt = cycle_date_dt + timedelta(days=days_until_monday)
    cycle_date_str = cycle_date_dt.strftime("%Y-%m-%d")
    return RecipePostRequest(
        cycleDate=cycle_date_str,
        title="Crispy Hash Brown Skillet",
        subtitle="A delicious breakfast skillet",
        servings=2,
        isAddOn=False,
        mainProtein="BEEF",
        pantryItems=[
            RecipeIngredient(pantryItemId="f47ac10b-58cc-4372-a567-0e02b2c3d479"),
            RecipeIngredient(pantryItemId="b9a2f51c-24e3-4e2f-b2fc-9f37c0c73c4a"),
        ],
        recipeTags=RecipeTags(
            recipeConstraintTags=["600CaloriesOrLess", "wheatFree"],
            packagingConfigurationTags=["heatAndEat", "familyStyle"],
        ),
    )


@pytest.fixture
def recipe_patch_request() -> RecipePatchRequest:
    return RecipePatchRequest(
        title="Updated Title",
        subtitle="Updated Subtitle",
        recipeTags=RecipeTags(
            recipeConstraintTags=["600CaloriesOrLess"],
            packagingConfigurationTags=["heatAndEat"],
        ),
        pantryItems=[RecipeIngredient(pantryItemId="f47ac10b-58cc-4372-a567-0e02b2c3d479")],
    )


@pytest.fixture
def mock_slot_assignment_service() -> Mock:
    slot_assignment_service = Mock()
    slot_assignment_service.assign_recipe_slot.return_value = "M"
    return slot_assignment_service


def test_get_recipes_success(
    recipe_service: RecipeService,
    mock_culops_client: Mock,
    mock_recipes_repo: Mock,
    mock_cabinet_client: Mock,
) -> None:
    mock_cabinet_client.find_cycle.return_value = True
    recipe_ref = CulopsRecipeRef(
        culops_recipe_id=123456, recipe_id=UUID("caf542de-d27b-4002-ab9c-3a757e2debec"), deleted=False
    )
    mock_recipes_repo.get_culops_recipe_ref_by_id.return_value = recipe_ref

    res_recipe = easy_mock_recipe()
    res_recipe._recipe_id = UUID("caf542de-d27b-4002-ab9c-3a757e2debec")
    res_recipe._title = "test recipe"
    res_recipe._subtitle = "test sub title"

    mock_culops_client.get_cycle_recipes.return_value = [res_recipe]

    response = recipe_service.get_recipes(partner_id, "2025-08-11", ["caf542de-d27b-4002-ab9c-3a757e2debec"])

    assert isinstance(response, list)
    assert len(response) == 1
    assert response[0].recipe_id == "caf542de-d27b-4002-ab9c-3a757e2debec"
    assert response[0].cycle_date == "2025-08-11"
    assert response[0].title == "test recipe"
    assert response[0].subtitle == "test sub title"


def test_get_recipes_success_no_recipe_ids(
    recipe_service: RecipeService,
    mock_culops_client: Mock,
    mock_cabinet_client: Mock,
) -> None:
    mock_cabinet_client.find_cycle.return_value = True

    r1 = easy_mock_recipe()
    r1._recipe_id = UUID("caf542de-d27b-4002-ab9c-3a757e2debec")
    r1._title = "Recipe One"
    r1._subtitle = "Sub One"

    r2 = easy_mock_recipe()
    r2._recipe_id = UUID("2a4a4c7c-4f83-4b16-8c2a-6f9a2f3c5e1a")
    r2._title = "Recipe Two"
    r2._subtitle = "Sub Two"

    mock_culops_client.get_cycle_recipes.return_value = [r1, r2]

    response = recipe_service.get_recipes(partner_id, "2025-08-11", None)

    assert isinstance(response, list)
    assert len(response) == 2
    assert response[0].title == "Recipe One"
    assert response[1].title == "Recipe Two"


def test_get_recipes_mixed_known_and_unknown_ids_raises_recipe_not_found(
    recipe_service: RecipeService,
    mock_culops_client: Mock,
    mock_recipes_repo: Mock,
    mock_cabinet_client: Mock,
) -> None:
    mock_cabinet_client.find_cycle.return_value = True

    known_id = "caf542de-d27b-4002-ab9c-3a757e2debec"
    unknown_id = str(uuid4())

    def repo_side_effect(p_id: str, r_id: UUID) -> Any:
        if r_id == UUID(known_id):
            return CulopsRecipeRef(culops_recipe_id=98765, recipe_id=r_id, deleted=False)
        return None

    mock_recipes_repo.get_culops_recipe_ref_by_id.side_effect = repo_side_effect

    r = easy_mock_recipe()
    r._recipe_id = UUID(known_id)
    r._title = "Known"
    mock_culops_client.get_cycle_recipes.return_value = [r]

    with pytest.raises(RecipeNotFoundError, match=f"Recipe {unknown_id} not found"):
        recipe_service.get_recipes(partner_id, "2025-08-11", [known_id, unknown_id])


def test_get_recipes_deleted_id_raises_already_deleted_error(
    recipe_service: RecipeService,
    mock_culops_client: Mock,
    mock_recipes_repo: Mock,
    mock_cabinet_client: Mock,
) -> None:
    mock_cabinet_client.find_cycle.return_value = True

    deleted_id = "caf542de-d27b-4002-ab9c-3a757e2debec"

    def repo_side_effect(p_id: str, r_id: UUID) -> Any:
        if r_id == UUID(deleted_id):
            return CulopsRecipeRef(culops_recipe_id=98765, recipe_id=r_id, deleted=False)
        return None

    mock_recipes_repo.get_culops_recipe_ref_by_id.side_effect = repo_side_effect

    def repo_get_recipe_uuid_side_effect(culops_recipe_id: int) -> Any:
        if culops_recipe_id == 98765:
            return UUID(deleted_id)
        return None

    mock_culops_client.get_cycle_recipes.side_effect = RecipeNotFoundError(
        f"Recipe {deleted_id} not found", recipe_id=98765
    )

    mock_recipes_repo.get_recipe_id_by_culops_recipe_id.side_effect = repo_get_recipe_uuid_side_effect

    with pytest.raises(RecipeAlreadyDeletedError, match=f"Recipe {deleted_id} has been deleted"):
        recipe_service.get_recipes(partner_id, "2025-08-11", [deleted_id])


def test_get_recipes_deleted_id_raises_already_deleted_error_with_uuid(
    recipe_service: RecipeService,
    mock_culops_client: Mock,
    mock_recipes_repo: Mock,
    mock_cabinet_client: Mock,
) -> None:
    deleted_id = "caf542de-d27b-4002-ab9c-3a757e2debec"

    mock_recipes_repo.get_culops_recipe_ref_by_id.return_value = CulopsRecipeRef(
        culops_recipe_id=11111, recipe_id=UUID(deleted_id), deleted=True
    )

    with pytest.raises(RecipeAlreadyDeletedError, match=f"Recipe {deleted_id} has been deleted"):
        recipe_service.get_recipes(partner_id, "2025-08-11", [deleted_id])

    mock_culops_client.get_cycle_recipes.assert_not_called()


def test_get_recipes_invalid_cycle_date_format(
    recipe_service: RecipeService,
) -> None:
    with pytest.raises(ValueError):
        recipe_service.get_recipes(partner_id, "invalid-date", None)


def test_get_recipes_cycle_not_found_in_cabinet(
    recipe_service: RecipeService,
    mock_cabinet_client: Mock,
) -> None:
    mock_cabinet_client.find_cycle.return_value = False

    with pytest.raises(ValueError, match=r"Cycle date 2025-08-11 is not a valid cycle date"):
        recipe_service.get_recipes(partner_id, "2025-08-11", None)


def test_get_recipes_cabinet_server_error(
    recipe_service: RecipeService,
    mock_cabinet_client: Mock,
) -> None:
    mock_cabinet_client.find_cycle.side_effect = ServerError("cabinet error")

    with pytest.raises(ServerError, match=r"Failed to validate cycle for cycle date: 2025-08-11"):
        recipe_service.get_recipes(partner_id, "2025-08-11", None)


def test_get_recipes_invalid_recipe_id_uuid(
    recipe_service: RecipeService,
    mock_cabinet_client: Mock,
) -> None:
    mock_cabinet_client.find_cycle.return_value = True

    with pytest.raises(ValueError, match=r"Recipe id not-a-uuid is not a valid UUID"):
        recipe_service.get_recipes(partner_id, "2025-08-11", ["not-a-uuid"])


def test_get_recipes_repo_server_error(
    recipe_service: RecipeService,
    mock_recipes_repo: Mock,
    mock_cabinet_client: Mock,
) -> None:
    mock_cabinet_client.find_cycle.return_value = True
    mock_recipes_repo.get_culops_recipe_ref_by_id.side_effect = ServerError("db error")

    with pytest.raises(ServerError, match=r"db error"):
        recipe_service.get_recipes(partner_id, "2025-08-11", [str(uuid4())])


def test_get_recipes_culops_server_error(
    recipe_service: RecipeService,
    mock_culops_client: Mock,
    mock_cabinet_client: Mock,
) -> None:
    mock_cabinet_client.find_cycle.return_value = True
    mock_culops_client.get_cycle_recipes.side_effect = ServerError("culops error")

    with pytest.raises(ServerError, match=r"Failed to get cycle recipes for cycle date: 2025-08-11"):
        recipe_service.get_recipes(partner_id, "2025-08-11", None)


def test_get_recipes_culops_value_error(
    recipe_service: RecipeService,
    mock_culops_client: Mock,
    mock_cabinet_client: Mock,
) -> None:
    mock_cabinet_client.find_cycle.return_value = True
    mock_culops_client.get_cycle_recipes.side_effect = ValueError("bad cycle")

    with pytest.raises(ServerError, match=r"Failed to get cycle recipes for cycle date: 2025-08-11"):
        recipe_service.get_recipes(partner_id, "2025-08-11", None)


def test_create_recipe_success(
    recipe_service: RecipeService,
    valid_recipe_post_request: RecipePostRequest,
    mock_partner_repo: Mock,
    mock_pantry_repo: Mock,
    mock_culops_client: Mock,
    mock_recipes_repo: Mock,
    mock_slot_assignment_service: Mock,
    mock_cabinet_client: Mock,
) -> None:
    with patch("src.services.recipe.RecipeSlotAssignmentService") as mock_slot_service_class:
        mock_slot_service_class.return_value = mock_slot_assignment_service
        response = recipe_service.create_recipe(partner_id, valid_recipe_post_request)

    assert isinstance(response, RecipeResponse)
    assert response.recipe_id is not None
    assert response.cycle_date == valid_recipe_post_request.cycle_date
    assert response.title == valid_recipe_post_request.title
    assert len(response.ingredients) == len(valid_recipe_post_request.pantry_items)
    assert response.is_add_on is valid_recipe_post_request.is_add_on
    assert response.recipe_tags is not None
    assert response.recipe_tags.recipe_constraint_tags is not None
    assert response.recipe_tags.packaging_configuration_tags is not None
    assert "wheatFree" in response.recipe_tags.recipe_constraint_tags
    assert "heatAndEat" in response.recipe_tags.packaging_configuration_tags
    assert response.recipe_card_ids == [valid_recipe_post_request.title]

    mock_partner_repo.get_recipe_create_cutoff_days.assert_called_once_with(partner_id)
    mock_pantry_repo.get_pantry_item_data_sources.assert_called_once()
    mock_culops_client.get_recipe_pantry_item_data.assert_called_once()
    mock_culops_client.create_recipe.assert_called_once()
    mock_culops_client.add_recipe_ingredients.assert_called_once()
    mock_recipes_repo.store_recipe_source.assert_called_once()


def test_create_recipe_all_prepped_and_ready(
    recipe_service: RecipeService,
    valid_recipe_post_request: RecipePostRequest,
    mock_culops_client: Mock,
    mock_slot_assignment_service: Mock,
) -> None:
    mock_culops_client.get_recipe_pantry_item_data.return_value = {
        123: PantryItemStatus(
            availabilities=[
                PantryItemAvailability(
                    available_from=datetime.now() - timedelta(days=1),
                    available_until=datetime.now() + timedelta(days=30),
                )
            ],
            is_prepped_and_ready=True,
        ),
    }

    valid_recipe_post_request.servings = 1
    valid_recipe_post_request.pantry_items = [
        RecipeIngredient(pantryItemId="f47ac10b-58cc-4372-a567-0e02b2c3d479"),
    ]

    with patch("src.services.recipe.RecipeSlotAssignmentService") as mock_slot_service_class:
        mock_slot_service_class.return_value = mock_slot_assignment_service
        response = recipe_service.create_recipe(partner_id, valid_recipe_post_request)

    assert response.recipe_card_ids == [""]


def test_create_recipe_cycle_date_before_cutoff_date(
    recipe_service: RecipeService,
    valid_recipe_post_request: RecipePostRequest,
) -> None:
    with pytest.raises(ValueError, match="Cycle date .* is not valid"):
        invalid_cycle_date = datetime.now() - timedelta(days=1)
        valid_recipe_post_request.cycle_date = invalid_cycle_date.strftime("%Y-%m-%d")
        recipe_service.create_recipe(partner_id, valid_recipe_post_request)


def test_create_recipe_cycle_date_not_monday(
    recipe_service: RecipeService,
    valid_recipe_post_request: RecipePostRequest,
) -> None:
    with pytest.raises(ValueError, match="Cycle date .* is not valid"):
        invalid_cycle_date = datetime.now()
        days_until_monday = (7 - invalid_cycle_date.weekday()) % 7
        invalid_cycle_date = invalid_cycle_date + timedelta(days=(days_until_monday + 1))
        valid_recipe_post_request.cycle_date = invalid_cycle_date.strftime("%Y-%m-%d")
        recipe_service.create_recipe(partner_id, valid_recipe_post_request)


def test_create_recipe_cycle_date_after_cutoff_date(
    recipe_service: RecipeService,
    valid_recipe_post_request: RecipePostRequest,
    mock_partner_repo: Mock,
) -> None:
    mock_partner_repo.get_recipe_create_cutoff_days.return_value = 60

    with pytest.raises(ValueError, match="Cycle date .* is before cutoff date"):
        recipe_service.create_recipe(partner_id, valid_recipe_post_request)

    mock_partner_repo.get_recipe_create_cutoff_days.assert_called_once_with(partner_id)


def test_create_recipe_partner_cutoff_days_query_error(
    recipe_service: RecipeService,
    valid_recipe_post_request: RecipePostRequest,
    mock_partner_repo: Mock,
) -> None:
    mock_partner_repo.get_recipe_create_cutoff_days.side_effect = ServerError("Query error")
    with pytest.raises(ServerError, match="Query error"):
        recipe_service.create_recipe(partner_id, valid_recipe_post_request)


def test_create_recipe_recipe_constraint_tags_invalid(
    recipe_service: RecipeService,
    valid_recipe_post_request: RecipePostRequest,
) -> None:
    with pytest.raises(ValueError, match="Invalid recipe constraint tags: \\['INVALID'\\]"):
        assert valid_recipe_post_request.recipe_tags is not None
        valid_recipe_post_request.recipe_tags.recipe_constraint_tags = ["INVALID"]
        recipe_service.create_recipe(partner_id, valid_recipe_post_request)


def test_create_recipe_packing_config_tags_invalid(
    recipe_service: RecipeService,
    valid_recipe_post_request: RecipePostRequest,
) -> None:
    with pytest.raises(ValueError, match="Invalid packaging configuration tags: \\['INVALID'\\]"):
        assert valid_recipe_post_request.recipe_tags is not None
        valid_recipe_post_request.recipe_tags.packaging_configuration_tags = ["INVALID"]
        recipe_service.create_recipe(partner_id, valid_recipe_post_request)


def test_create_recipe_partner_tags_query_error(
    recipe_service: RecipeService,
    valid_recipe_post_request: RecipePostRequest,
    mock_partner_repo: Mock,
) -> None:
    mock_partner_repo.get_partner_recipe_constraint_tags.side_effect = ServerError("Query error")
    with pytest.raises(ServerError, match="Query error"):
        recipe_service.create_recipe(partner_id, valid_recipe_post_request)


def test_create_recipe_pantry_item_data_sources_query_error(
    recipe_service: RecipeService,
    valid_recipe_post_request: RecipePostRequest,
    mock_pantry_repo: Mock,
) -> None:
    mock_pantry_repo.get_pantry_item_data_sources.side_effect = ServerError("Query error")
    with pytest.raises(ServerError, match="Query error"):
        recipe_service.create_recipe(partner_id, valid_recipe_post_request)


def test_create_recipe_pantry_item_data_sources_missing(
    recipe_service: RecipeService,
    valid_recipe_post_request: RecipePostRequest,
) -> None:
    invalid_pantry_item_id = str(uuid4())
    with pytest.raises(ValueError, match=f"Pantry item IDs not found in pantry: \\['{invalid_pantry_item_id}'\\]"):
        valid_recipe_post_request.pantry_items.append(RecipeIngredient(pantryItemId=invalid_pantry_item_id))
        recipe_service.create_recipe(partner_id, valid_recipe_post_request)


def test_create_recipe_pantry_item_data_request_error(
    recipe_service: RecipeService,
    valid_recipe_post_request: RecipePostRequest,
    mock_culops_client: Mock,
) -> None:
    mock_culops_client.get_recipe_pantry_item_data.side_effect = ServerError("Request error")

    with pytest.raises(ServerError, match="Failed to get pantry item data for recipe"):
        recipe_service.create_recipe(partner_id, valid_recipe_post_request)


def test_create_recipe_mix_of_prepped_and_ready_items(
    recipe_service: RecipeService,
    valid_recipe_post_request: RecipePostRequest,
    mock_culops_client: Mock,
) -> None:
    with pytest.raises(ValueError, match="Mixed prepped and ready and standard pantry items"):
        mock_culops_client.get_recipe_pantry_item_data.return_value = {
            123: PantryItemStatus(
                availabilities=[
                    PantryItemAvailability(
                        available_from=datetime.now() - timedelta(days=1),
                        available_until=datetime.now() + timedelta(days=30),
                    )
                ],
                is_prepped_and_ready=True,
            ),
            456: PantryItemStatus(
                availabilities=[
                    PantryItemAvailability(
                        available_from=datetime.now() - timedelta(days=1),
                        available_until=datetime.now() + timedelta(days=30),
                    )
                ],
                is_prepped_and_ready=False,
            ),
        }
        recipe_service.create_recipe(partner_id, valid_recipe_post_request)


def test_create_recipe_multiple_prepped_and_ready_items(
    recipe_service: RecipeService,
    valid_recipe_post_request: RecipePostRequest,
    mock_culops_client: Mock,
) -> None:
    with pytest.raises(ValueError, match="Multiple prepped and ready pantry items"):
        mock_culops_client.get_recipe_pantry_item_data.return_value = {
            123: PantryItemStatus(
                availabilities=[
                    PantryItemAvailability(
                        available_from=datetime.now() - timedelta(days=1),
                        available_until=datetime.now() + timedelta(days=30),
                    )
                ],
                is_prepped_and_ready=True,
            ),
            456: PantryItemStatus(
                availabilities=[
                    PantryItemAvailability(
                        available_from=datetime.now() - timedelta(days=1),
                        available_until=datetime.now() + timedelta(days=30),
                    )
                ],
                is_prepped_and_ready=True,
            ),
        }

        valid_recipe_post_request.servings = 1
        recipe_service.create_recipe(partner_id, valid_recipe_post_request)


def test_create_recipe_item_not_available_in_cycle(
    recipe_service: RecipeService,
    valid_recipe_post_request: RecipePostRequest,
    mock_culops_client: Mock,
    mock_partner_repo: Mock,
) -> None:
    mock_partner_repo.get_partner_recipe_plan_maps.return_value = []

    mock_culops_client.get_recipe_pantry_item_data.return_value = {
        123: PantryItemStatus(
            availabilities=[],
            is_prepped_and_ready=False,
        ),
        456: PantryItemStatus(
            availabilities=[
                PantryItemAvailability(
                    available_from=datetime.now() + timedelta(days=30),
                    available_until=datetime.now() + timedelta(days=60),
                ),
            ],
            is_prepped_and_ready=False,
        ),
    }
    with pytest.raises(ValueError, match=r".*Not available for cycle date.*"):
        recipe_service.create_recipe(partner_id, valid_recipe_post_request)


def test_create_recipe_failure_to_assign_slot(
    recipe_service: RecipeService,
    valid_recipe_post_request: RecipePostRequest,
    mock_slot_assignment_service: Mock,
) -> None:
    with patch("src.services.recipe.RecipeSlotAssignmentService") as mock_slot_service_class:
        mock_slot_service_class.return_value = mock_slot_assignment_service

        mock_slot_assignment_service.assign_recipe_slot.side_effect = ServerError("Slot assignment error")

        with pytest.raises(ServerError, match="Failed to assign recipe slot for recipe"):
            recipe_service.create_recipe(partner_id, valid_recipe_post_request)


def test_create_recipe_failure_to_create_recipe(
    recipe_service: RecipeService,
    valid_recipe_post_request: RecipePostRequest,
    mock_culops_client: Mock,
    mock_slot_assignment_service: Mock,
) -> None:
    with patch("src.services.recipe.RecipeSlotAssignmentService") as mock_slot_service_class:
        mock_slot_service_class.return_value = mock_slot_assignment_service
        mock_culops_client.create_recipe.side_effect = ServerError("Recipe creation error")

        with pytest.raises(ServerError, match="Failed to create recipe .* with items"):
            recipe_service.create_recipe(partner_id, valid_recipe_post_request)

    mock_culops_client.delete_recipe.assert_not_called()


def test_create_recipe_failure_to_store_recipe_source(
    recipe_service: RecipeService,
    valid_recipe_post_request: RecipePostRequest,
    mock_culops_client: Mock,
    mock_slot_assignment_service: Mock,
    mock_recipes_repo: Mock,
) -> None:
    with patch("src.services.recipe.RecipeSlotAssignmentService") as mock_slot_service_class:
        mock_slot_service_class.return_value = mock_slot_assignment_service

        mock_recipes_repo.store_recipe_source.side_effect = ServerError("Recipe source storage error")

        with pytest.raises(ServerError, match="Failed to create recipe"):
            recipe_service.create_recipe(partner_id, valid_recipe_post_request)

    mock_culops_client.delete_recipe.assert_called_once()


def test_create_recipe_failure_to_add_recipe_ingredients(
    recipe_service: RecipeService,
    valid_recipe_post_request: RecipePostRequest,
    mock_culops_client: Mock,
    mock_slot_assignment_service: Mock,
) -> None:
    with patch("src.services.recipe.RecipeSlotAssignmentService") as mock_slot_service_class:
        mock_slot_service_class.return_value = mock_slot_assignment_service
        mock_culops_client.add_recipe_ingredients.side_effect = ServerError("Recipe ingredient addition error")

        with pytest.raises(ServerError, match="Failed to create recipe"):
            recipe_service.create_recipe(partner_id, valid_recipe_post_request)

    mock_culops_client.delete_recipe.assert_called_once()


def test_delete_recipe_success(
    recipe_service: RecipeService,
    mock_partner_repo: Mock,
    mock_culops_client: Mock,
    mock_recipes_repo: Mock,
) -> None:
    recipe_id = str(uuid4())
    recipe_uuid = UUID(recipe_id)
    culops_recipe_id = 12345
    cycle_date = datetime.now() + timedelta(days=30)

    culops_recipe_ref = CulopsRecipeRef(culops_recipe_id=culops_recipe_id, recipe_id=recipe_uuid, deleted=False)

    mock_recipe = Mock()
    mock_recipe.cycle_date = cycle_date

    mock_recipes_repo.get_culops_recipe_ref_by_id.return_value = culops_recipe_ref
    mock_culops_client.get_recipe.return_value = mock_recipe
    mock_partner_repo.get_recipe_delete_cutoff_days.return_value = 7

    recipe_service.delete_recipe(partner_id, recipe_id)

    mock_recipes_repo.get_culops_recipe_ref_by_id.assert_called_once_with(partner_id, recipe_uuid)
    mock_culops_client.get_recipe.assert_called_once_with(culops_recipe_id, partner_id)
    mock_partner_repo.get_recipe_delete_cutoff_days.assert_called_once_with(partner_id)
    mock_recipes_repo.mark_recipe_as_deleted.assert_called_once()


def test_delete_recipe_invalid_recipe_id_format(
    recipe_service: RecipeService,
) -> None:
    with pytest.raises(ValueError, match="Invalid recipe ID format: invalid-id"):
        recipe_service.delete_recipe(partner_id, "invalid-id")


def test_delete_recipe_ref_not_found(
    recipe_service: RecipeService,
    mock_recipes_repo: Mock,
) -> None:
    recipe_id = str(uuid4())
    mock_recipes_repo.get_culops_recipe_ref_by_id.return_value = None

    with pytest.raises(RecipeNotFoundError, match=f"Recipe with ID {recipe_id} not found for partner {partner_id}"):
        recipe_service.delete_recipe(partner_id, recipe_id)

    mock_recipes_repo.get_culops_recipe_ref_by_id.assert_called_once()


def test_delete_recipe_already_deleted(
    recipe_service: RecipeService,
    mock_recipes_repo: Mock,
) -> None:
    recipe_id = str(uuid4())
    culops_recipe_ref = CulopsRecipeRef(culops_recipe_id=12345, recipe_id=UUID(recipe_id), deleted=True)

    mock_recipes_repo.get_culops_recipe_ref_by_id.return_value = culops_recipe_ref

    with pytest.raises(RecipeAlreadyDeletedError, match=f"Recipe with ID {recipe_id} is already deleted"):
        recipe_service.delete_recipe(partner_id, recipe_id)

    mock_recipes_repo.get_culops_recipe_ref_by_id.assert_called_once()


def test_delete_recipe_culops_get_recipe_error(
    recipe_service: RecipeService,
    mock_recipes_repo: Mock,
    mock_culops_client: Mock,
) -> None:
    recipe_id = str(uuid4())
    culops_recipe_id = 12345

    culops_recipe_ref = CulopsRecipeRef(culops_recipe_id=culops_recipe_id, recipe_id=UUID(recipe_id), deleted=False)

    mock_recipes_repo.get_culops_recipe_ref_by_id.return_value = culops_recipe_ref
    mock_culops_client.get_recipe.side_effect = ServerError("CulOps error")

    with pytest.raises(ServerError, match=f"Failed to get Culops recipe before deleting {recipe_id} from CulOps"):
        recipe_service.delete_recipe(partner_id, recipe_id)

    mock_culops_client.get_recipe.assert_called_once_with(culops_recipe_id, partner_id)


def test_delete_recipe_culops_recipe_not_found(
    recipe_service: RecipeService,
    mock_recipes_repo: Mock,
    mock_culops_client: Mock,
) -> None:
    recipe_id = str(uuid4())
    recipe_uuid = UUID(recipe_id)
    culops_recipe_id = 12345

    culops_recipe_ref = CulopsRecipeRef(culops_recipe_id=culops_recipe_id, recipe_id=recipe_uuid, deleted=False)

    mock_recipes_repo.get_culops_recipe_ref_by_id.return_value = culops_recipe_ref
    mock_culops_client.get_recipe.return_value = None

    with pytest.raises(RecipeAlreadyDeletedError, match=f"Recipe with ID {recipe_id} not found in CulOps"):
        recipe_service.delete_recipe(partner_id, recipe_id)

    mock_recipes_repo.mark_recipe_as_deleted.assert_called_once_with(partner_id, recipe_uuid)


def test_delete_recipe_cycle_date_too_recent(
    recipe_service: RecipeService,
    mock_partner_repo: Mock,
    mock_culops_client: Mock,
    mock_recipes_repo: Mock,
) -> None:
    recipe_id = str(uuid4())
    culops_recipe_id = 12345
    cycle_date = datetime.now() - timedelta(days=3)

    culops_recipe_ref = CulopsRecipeRef(culops_recipe_id=culops_recipe_id, recipe_id=UUID(recipe_id), deleted=False)

    mock_recipe = Mock()
    mock_recipe.cycle_date = cycle_date

    mock_recipes_repo.get_culops_recipe_ref_by_id.return_value = culops_recipe_ref
    mock_culops_client.get_recipe.return_value = mock_recipe
    mock_partner_repo.get_recipe_delete_cutoff_days.return_value = 7

    with pytest.raises(ValueError, match="Recipe cycle date .* is in delete cutoff window"):
        recipe_service.delete_recipe(partner_id, recipe_id)

    mock_partner_repo.get_recipe_delete_cutoff_days.assert_called_once_with(partner_id)
    mock_recipes_repo.mark_recipe_as_deleted.assert_not_called()


def test_delete_recipe_cycle_date_exactly_at_cutoff(
    recipe_service: RecipeService,
    mock_partner_repo: Mock,
    mock_culops_client: Mock,
    mock_recipes_repo: Mock,
) -> None:
    recipe_id = str(uuid4())
    recipe_uuid = UUID(recipe_id)
    culops_recipe_id = 12345

    cutoff_days = 7
    cycle_date = datetime.now() - timedelta(days=cutoff_days)

    culops_recipe_ref = CulopsRecipeRef(culops_recipe_id=culops_recipe_id, recipe_id=recipe_uuid, deleted=False)

    mock_recipe = Mock()
    mock_recipe.cycle_date = cycle_date

    mock_recipes_repo.get_culops_recipe_ref_by_id.return_value = culops_recipe_ref
    mock_culops_client.get_recipe.return_value = mock_recipe
    mock_partner_repo.get_recipe_delete_cutoff_days.return_value = cutoff_days

    with pytest.raises(ValueError, match="Recipe cycle date .* is in delete cutoff window"):
        recipe_service.delete_recipe(partner_id, recipe_id)

    mock_partner_repo.get_recipe_delete_cutoff_days.assert_called_once_with(partner_id)
    mock_recipes_repo.mark_recipe_as_deleted.assert_not_called()


def test_delete_recipe_culops_delete_error_in_hook(
    recipe_service: RecipeService,
    mock_partner_repo: Mock,
    mock_culops_client: Mock,
    mock_recipes_repo: Mock,
) -> None:
    recipe_id = str(uuid4())
    culops_recipe_id = 12345
    cycle_date = datetime.now() + timedelta(days=30)

    culops_recipe_ref = CulopsRecipeRef(culops_recipe_id=culops_recipe_id, recipe_id=UUID(recipe_id), deleted=False)

    mock_recipe = Mock()
    mock_recipe.cycle_date = cycle_date

    mock_recipes_repo.get_culops_recipe_ref_by_id.return_value = culops_recipe_ref
    mock_culops_client.get_recipe.return_value = mock_recipe
    mock_partner_repo.get_recipe_delete_cutoff_days.return_value = 7
    mock_culops_client.delete_recipe.side_effect = ServerError("CulOps delete error")

    def mock_mark_recipe_as_deleted(
        partner_id: str, recipe_uuid: UUID, pre_delete_hook: Callable | None = None
    ) -> None:
        if pre_delete_hook:
            pre_delete_hook()

    mock_recipes_repo.mark_recipe_as_deleted.side_effect = mock_mark_recipe_as_deleted

    with pytest.raises(ServerError, match="Failed to delete recipe .* from CulOps"):
        recipe_service.delete_recipe(partner_id, recipe_id)

    mock_culops_client.delete_recipe.assert_called_once_with(culops_recipe_id)


def test_update_recipe_success(
    recipe_service: RecipeService,
    recipe_patch_request: RecipePatchRequest,
    mock_recipes_repo: Mock,
    mock_culops_client: Mock,
    mock_pantry_repo: Mock,
    mock_partner_repo: Mock,
) -> None:
    recipe_id = UUID("caf542de-d27b-4002-ab9c-3a757e2debec")

    response = recipe_service.update_recipe(partner_id, str(recipe_id), recipe_patch_request)

    assert isinstance(response, RecipeResponse)
    assert response.title == "Updated Title"
    assert response.subtitle == "Updated Subtitle"
    assert response.recipe_tags is not None
    assert response.recipe_tags.recipe_constraint_tags == ["600CaloriesOrLess"]


@pytest.mark.parametrize(
    "field_name, invalid_value",
    [
        {"recipe_id", "123"},
        {"cycle_date", "2025-10-10"},
        ("servings_count", 66),
        ("recipe_card_assignments", "oops"),
    ],
)
def test_update_recipe_invalid_request_data(
    field_name: str,
    invalid_value: Any,
    mock_cycle_date: datetime,
    recipe_service: RecipeService,
    recipe_patch_request: RecipePatchRequest,
) -> None:
    recipe_id = UUID("caf542de-d27b-4002-ab9c-3a757e2debec")

    response = recipe_service.update_recipe(partner_id, str(recipe_id), recipe_patch_request)

    assert isinstance(response, RecipeResponse)
    assert response.recipe_id == str(recipe_id)
    assert response.cycle_date == parse_from_datetime(mock_cycle_date)
    assert response.recipe_card_ids == []


def test_update_recipe_cross_id_missing(
    recipe_service: RecipeService,
    recipe_patch_request: RecipePatchRequest,
    mock_recipes_repo: Mock,
) -> None:
    recipe_id = "caf542de-d27b-4002-ab9c-3a757e2debec"

    mock_recipes_repo.get_culops_recipe_ref_by_id.return_value = None

    with pytest.raises(Exception, match=f"Recipe {recipe_id} not found"):
        recipe_service.update_recipe(partner_id, recipe_id, recipe_patch_request)


def test_update_recipe_culops_not_found(
    recipe_service: RecipeService,
    recipe_patch_request: RecipePatchRequest,
    mock_culops_client: Mock,
) -> None:
    recipe_id = "caf542de-d27b-4002-ab9c-3a757e2debec"

    mock_culops_client.get_recipe.return_value = None

    with pytest.raises(Exception, match=f"Recipe {recipe_id} not found in culops"):
        recipe_service.update_recipe(partner_id, recipe_id, recipe_patch_request)


def test_update_recipe_deleted(
    recipe_service: RecipeService,
    recipe_patch_request: RecipePatchRequest,
    mock_recipes_repo: Mock,
) -> None:
    recipe_id = "caf542de-d27b-4002-ab9c-3a757e2debec"
    mock_recipes_repo.get_culops_recipe_ref_by_id.return_value.deleted = True

    with pytest.raises(Exception, match=f"Recipe {recipe_id} has been deleted"):
        recipe_service.update_recipe(partner_id, recipe_id, recipe_patch_request)


def test_update_recipe_invalid_cycle_date(
    recipe_service: RecipeService,
    recipe_patch_request: RecipePatchRequest,
    mock_culops_client: Mock,
) -> None:
    recipe_id = "caf542de-d27b-4002-ab9c-3a757e2debec"
    # Assign an invalid (e.g., past) cycle date
    mock_culops_client.get_recipe.return_value._cycle_date = datetime.strptime("1990-01-01", "%Y-%m-%d")

    with pytest.raises(Exception, match=r"Cycle date .* is not valid"):
        recipe_service.update_recipe(partner_id, recipe_id, recipe_patch_request)


def test_update_recipe_cycle_date_after_cutoff(
    recipe_service: RecipeService,
    recipe_patch_request: RecipePatchRequest,
    mock_culops_client: Mock,
    mock_partner_repo: Mock,
) -> None:
    recipe_id = "caf542de-d27b-4002-ab9c-3a757e2debec"
    # Start with a date 2 days from now to ensure it's in the future
    cycle_date = datetime.now() + timedelta(days=2)
    days_until_monday = (7 - cycle_date.weekday()) % 7
    if days_until_monday == 0:  # If it's already Monday, go to next Monday
        days_until_monday = 7
    cycle_date += timedelta(days=days_until_monday)

    mock_partner_repo.get_recipe_update_cutoff_days.return_value = 15
    mock_culops_client.get_recipe.return_value = Mock(
        recipe_id=123456,
        title="test recipe",
        subtitle="test bsub title",
        servings_count=4,
        is_add_on=False,
        cycle_date=cycle_date,
        recipe_card_assignments=[],
    )

    with pytest.raises(Exception, match="Cycle date .* is within cutoff date .*"):
        recipe_service.update_recipe(partner_id, recipe_id, recipe_patch_request)


def test_update_recipe_mixed_prepped_and_standard(
    recipe_service: RecipeService,
    recipe_patch_request: RecipePatchRequest,
    mock_culops_client: Mock,
) -> None:
    recipe_id = "caf542de-d27b-4002-ab9c-3a757e2debec"
    # Make one item prepped and the other not
    mock_culops_client.get_recipe_pantry_item_data.return_value[123].is_prepped_and_ready = True
    mock_culops_client.get_recipe_pantry_item_data.return_value[456].is_prepped_and_ready = False

    recipe_patch_request.pantry_items = [
        RecipeIngredient(pantryItemId="f47ac10b-58cc-4372-a567-0e02b2c3d479"),
        RecipeIngredient(pantryItemId="b9a2f51c-24e3-4e2f-b2fc-9f37c0c73c4a"),
    ]

    with pytest.raises(ValueError, match="Mixed prepped and ready and standard pantry items"):
        recipe_service.update_recipe(partner_id, recipe_id, recipe_patch_request)


def test_update_recipe_multiple_prepped_items(
    recipe_service: RecipeService,
    recipe_patch_request: RecipePatchRequest,
    mock_culops_client: Mock,
) -> None:
    recipe_id = "caf542de-d27b-4002-ab9c-3a757e2debec"
    mock_culops_client.get_recipe_pantry_item_data.return_value[123].is_prepped_and_ready = True
    mock_culops_client.get_recipe_pantry_item_data.return_value[456].is_prepped_and_ready = True

    recipe_patch_request.pantry_items = [
        RecipeIngredient(pantryItemId="f47ac10b-58cc-4372-a567-0e02b2c3d479"),
        RecipeIngredient(pantryItemId="b9a2f51c-24e3-4e2f-b2fc-9f37c0c73c4a"),
    ]

    with pytest.raises(ValueError, match="Multiple prepped and ready pantry items"):
        recipe_service.update_recipe(partner_id, recipe_id, recipe_patch_request)


def test_update_recipe_adds_and_removes_ingredients(
    recipe_service: RecipeService,
    recipe_patch_request: RecipePatchRequest,
    mock_culops_client: Mock,
) -> None:
    recipe_id = "caf542de-d27b-4002-ab9c-3a757e2debec"
    recipe_patch_request.pantry_items = [
        RecipeIngredient(pantryItemId="f47ac10b-58cc-4372-a567-0e02b2c3d479"),
        RecipeIngredient(pantryItemId="b9a2f51c-24e3-4e2f-b2fc-9f37c0c73c4a"),
        RecipeIngredient(pantryItemId="b9a2f51c-24e3-4e2f-b2fc-9f37c0c73c4b"),
    ]

    recipe_service.update_recipe(partner_id, recipe_id, recipe_patch_request)

    mock_culops_client.add_recipe_ingredients.assert_called_once_with(
        123456,
        [
            PantryItemCulinaryIngredientSpecification(
                pantry_item_id=UUID("b9a2f51c-24e3-4e2f-b2fc-9f37c0c73c4b"),
                culops_culinary_ingredient_specification_id=101112,
                culops_culinary_ingredient_id=456,
            )
        ],
    )
    mock_culops_client.remove_recipe_ingredients.assert_not_called()


def test_get_recipe_ids_by_skus_mapping_success(recipe_service: RecipeService, mock_recipes_repo: Mock) -> None:
    partner_id = "TC-MAIN"
    skus = ["SKU-111", "SKU-222"]

    recipe_refs = [
        RecipeRef(recipe_id=uuid4(), culops_recipe_id=123, culops_product_sku="SKU-111"),
        RecipeRef(recipe_id=uuid4(), culops_recipe_id=456, culops_product_sku="SKU-222"),
    ]
    mock_recipes_repo.get_culops_recipe_ref_by_sku.side_effect = recipe_refs

    result: list[Any] = recipe_service.get_recipe_ids_by_skus(partner_id=partner_id, product_skus=skus)

    assert isinstance(result, list)
    assert all(isinstance(r, RecipeSku) for r in result)
    assert [r.sku for r in result] == skus
    assert mock_recipes_repo.get_culops_recipe_ref_by_sku.call_count == len(skus)
