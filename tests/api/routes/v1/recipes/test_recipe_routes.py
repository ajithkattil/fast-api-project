import uuid
from collections.abc import Generator
from contextlib import contextmanager
from typing import Any
from unittest.mock import Mock

import pytest
from fastapi import status
from fastapi.testclient import TestClient

from src.api.routes.v1.models import RecipeIngredient, RecipePatchRequest, RecipeResponse, RecipeSku, RecipeTags
from src.core.exceptions import AccessDeniedException, RecipeAlreadyDeletedError, RecipeNotFoundError, ServerError
from src.dependancies.idempotency_db import get_idempotency_db
from src.dependancies.partner_service import get_partner_service
from src.dependancies.recipe_service import get_recipe_service
from src.main import app
from tests.conftest import encode_jwt


@pytest.fixture
def valid_recipe_post_request() -> dict:
    return {
        "cycleDate": "2025-05-11",
        "title": "Crispy Hash Brown Skillet",
        "pantryItems": [
            {"pantryItemId": "f47ac10b-58cc-4372-a567-0e02b2c3d479"},
            {"pantryItemId": "b9a2f51c-24e3-4e2f-b2fc-9f37c0c73c4a"},
            {"pantryItemId": "d5f39c3a-7c72-4b5f-8f1d-2c1c6b7b9e2a"},
            {"pantryItemId": "a8b7c6d5-e4f3-4a2b-9c8d-7e6f5a4b3c2d"},
            {"pantryItemId": "c1d2e3f4-5a6b-7c8d-9e0f-1a2b3c4d5e6f"},
            {"pantryItemId": "e7f8g9h0-1i2j-3k4l-5m6n-7o8p9q0r1s2t"},
            {"pantryItemId": "3b4c5d6e-7f8g-9h0i-1j2k-3l4m5n6o7p8q"},
        ],
        "servings": 4,
        "mainProtein": "PORK",
        "isAddOn": True,
        "recipeTags": {"recipeConstraintTags": ["wheatFree"]},
    }


@pytest.fixture
def valid_headers() -> dict:
    auth_header = encode_jwt({"custom:partner_id": "partner-123"})
    return {"Idempotency-Key": str(uuid.uuid4()), "Authorization": f"Bearer {auth_header}"}


@pytest.fixture
def mock_partner_repo(valid_partner_id: bool = True, cutoff_days: int = 30, validate_tags: bool = True) -> Mock:
    mock = Mock()
    mock.validate_partner_id.return_value = valid_partner_id
    mock.get_recipe_create_cutoff_days.return_value = cutoff_days
    mock.validate_tags.return_value = validate_tags
    return mock


@pytest.fixture
def mock_partner_service(valid_partner_id: bool = True, validate_tags: bool = True) -> Mock:
    mock = Mock()
    mock.validate_partner_id.return_value = valid_partner_id
    mock.validate_tags.return_value = validate_tags
    mock.partner_id = "123"
    return mock


@pytest.fixture
def mock_idempotency_repo(idemp_key_found: bool = False) -> Mock:
    mock = Mock()
    mock.idempotency_key_exists.return_value = idemp_key_found
    return mock


@pytest.fixture
def mock_recipe_service(response_recipe: dict | None = None) -> Mock:
    if response_recipe is None:
        response_recipe = RecipeResponse(
            recipeId=str(uuid.uuid4()),
            cycleDate="2025-05-11",
            title="Crispy Hash Brown Skillet",
            subtitle="with onions",
            pantryItems=[
                RecipeIngredient(pantryItemId="f47ac10b-58cc-4372-a567-0e02b2c3d479"),
                RecipeIngredient(pantryItemId="b9a2f51c-24e3-4e2f-b2fc-9f37c0c73c4a"),
            ],
            servings=4,
            isAddOn=True,
            recipeCardIds=["card1"],
            recipeTags=RecipeTags(recipeConstraintTags=["wheatFree"]),
        )

    mock = Mock()
    mock.create_recipe.return_value = response_recipe

    # For update_recipe, create a dynamic response based on the input data
    def update_recipe_side_effect(partner_id: str, recipe_id: str, recipe_data: RecipePatchRequest) -> RecipeResponse:
        # Create a response that reflects the updated data
        updated_response = RecipeResponse(
            recipeId=recipe_id,
            cycleDate="2025-05-11",
            title=recipe_data.title or "Crispy Hash Brown Skillet",
            subtitle=recipe_data.subtitle or "with onions",
            pantryItems=recipe_data.pantry_items
            or [
                RecipeIngredient(pantryItemId="f47ac10b-58cc-4372-a567-0e02b2c3d479"),
                RecipeIngredient(pantryItemId="b9a2f51c-24e3-4e2f-b2fc-9f37c0c73c4a"),
            ],
            servings=4,
            mainProtein="PORK",
            isAddOn=True,
            recipeCardIds=["card1"],
            recipeTags=recipe_data.recipe_tags or RecipeTags(recipeConstraintTags=["wheatFree"]),
        )
        return updated_response

    mock.update_recipe.side_effect = update_recipe_side_effect
    return mock


def test_get_pantry_errors_when_missing_partner_id(test_client: TestClient) -> None:
    with pytest.raises(AccessDeniedException):
        test_client.get("/v1/recipes")


def test_post_recipe_success(
    test_client: TestClient,
    valid_recipe_post_request: dict,
    valid_headers: dict,
    mock_partner_service: Mock,
    mock_idempotency_repo: Mock,
    mock_recipe_service: Mock,
) -> None:
    # Store original overrides
    original_overrides = app.dependency_overrides.copy()

    # Override dependencies at the app level
    app.dependency_overrides[get_partner_service] = lambda: mock_partner_service
    app.dependency_overrides[get_idempotency_db] = lambda: mock_idempotency_repo
    app.dependency_overrides[get_recipe_service] = lambda: mock_recipe_service

    try:
        response = test_client.post("/v1/recipes", json=valid_recipe_post_request, headers=valid_headers)
        assert response.status_code == status.HTTP_201_CREATED
        data = response.json()
        assert "data" in data
        assert "recipe" in data["data"]
        assert "pantryItems" in data["data"]["recipe"]
        assert data["data"]["recipe"]["recipeId"] is not None

        # Verify mocks were called correctly
        mock_partner_service.validate_partner_id.assert_called_once()
        mock_idempotency_repo.idempotency_key_exists.assert_called_once()
        mock_recipe_service.create_recipe.assert_called_once()
    finally:
        app.dependency_overrides = original_overrides


def test_post_recipe_conflict_on_existing_idempotency_key(
    test_client: TestClient,
    valid_recipe_post_request: dict,
) -> None:
    auth_header = encode_jwt({"custom:partner_id": "123"})
    headers = {
        "Authorization": f"Bearer {auth_header}",
        "idempotency-key": "ff22dcdb-c7b2-428a-8f2a-d63f25f48d70",
    }

    response = test_client.post("/v1/recipes", json=valid_recipe_post_request, headers=headers)
    assert response.status_code == status.HTTP_409_CONFLICT


def test_post_recipe_invalid_tags(test_client: TestClient, valid_headers: dict) -> None:
    invalid_tag_req = {
        "cycleDate": "2025-05-11",
        "title": "Crispy Hash Brown Skillet",
        "pantryItems": [
            {"pantryItemId": "f47ac10b-58cc-4372-a567-0e02b2c3d479"},
        ],
        "servings": 4,
        "mainProtein": "PORK",
        "isAddOn": True,
        "recipeTags": {"recipeConstraintTags": ["wheatFree", "invalidTag"]},
    }

    response = test_client.post("/v1/recipes", json=invalid_tag_req, headers=valid_headers)

    assert response.status_code == status.HTTP_400_BAD_REQUEST


def test_post_recipe_bad_payload(test_client: TestClient, valid_headers: dict) -> None:
    bad_payload = {"bad": "data"}
    response = test_client.post("/v1/recipes", json=bad_payload, headers=valid_headers)

    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


def test_post_recipe_missing_partner_header(
    test_client: TestClient,
    valid_recipe_post_request: dict,
) -> None:
    with pytest.raises(AccessDeniedException):
        test_client.post("/v1/recipes", json=valid_recipe_post_request)


@pytest.fixture
def valid_recipe_patch_request() -> dict:
    return {
        "title": "Updated Hash Brown Skillet",
        "recipeTags": {"recipeConstraintTags": ["wheatFree"]},
    }


@pytest.fixture
def invalid_tag_patch_request() -> dict:
    return {
        "title": "Still Crispy",
        "recipeTags": {"recipeConstraintTags": ["invalidTag"]},
    }


@pytest.mark.parametrize(
    "field, value, expected",
    [
        ("title", "Updated Title", "Updated Title"),
        ("subtitle", "New Subtitle", "New Subtitle"),
        (
            "recipeTags",
            {"recipeConstraintTags": ["wheatFree"], "packagingConfigurationTags": ["heatAndEat"]},
            {"recipeConstraintTags": ["wheatFree"], "packagingConfigurationTags": ["heatAndEat"]},
        ),
        ("pantryItems", [{"pantryItemId": "abc123"}], [{"pantryItemId": "abc123"}]),
    ],
)
def test_patch_recipe_each_allowed_field(
    field: str,
    value: Any,
    expected: Any,
    test_client: TestClient,
    valid_headers: dict,
    mock_recipe_service: Mock,
    mock_partner_service: Mock,
    valid_recipe_patch_request: dict,
) -> None:
    recipe_id = "caf542de-d27b-4002-ab9c-3a757e2debec"

    # Store original overrides
    original_overrides = app.dependency_overrides.copy()

    # Override recipe service dependency
    app.dependency_overrides[get_recipe_service] = lambda: mock_recipe_service
    app.dependency_overrides[get_partner_service] = lambda: mock_partner_service

    try:
        response = test_client.patch(f"/v1/recipes/{recipe_id}", json={field: value}, headers=valid_headers)

        assert response.status_code == 200, response.text

        recipe = response.json()["data"]["recipe"]

        assert recipe[field] == expected
    finally:
        app.dependency_overrides = original_overrides


@pytest.mark.parametrize("field", ["servings", "mainProtein", "isAddOn", "cycleDate", "invalidField"])
def test_patch_recipe_each_not_allowed_field(
    field: str, test_client: TestClient, valid_headers: dict, mock_recipe_service: Mock
) -> None:
    recipe_id = "caf542de-d27b-4002-ab9c-3a757e2debec"
    value = {
        "servings": 200,
        "mainProtein": "MEAT",
        "isAddOn": False,
        "cycleDate": "2024-05-11",
        "invalidField": "oops",
    }[field]

    # Store original overrides
    original_overrides = app.dependency_overrides.copy()

    # Override recipe service dependency
    app.dependency_overrides[get_recipe_service] = lambda: mock_recipe_service

    try:
        response = test_client.patch(f"/v1/recipes/{recipe_id}", json={field: value}, headers=valid_headers)
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.json()["error"] == "At least one updatable field must be provided."
    finally:
        app.dependency_overrides = original_overrides


def test_patch_empty_body(
    test_client: TestClient,
    valid_headers: dict,
    mock_recipe_service: Mock,
) -> None:
    recipe_id = "caf542de-d27b-4002-ab9c-3a757e2debec"

    # Store original overrides
    original_overrides = app.dependency_overrides.copy()

    # Override recipe service dependency
    app.dependency_overrides[get_recipe_service] = lambda: mock_recipe_service

    try:
        response = test_client.patch(f"/v1/recipes/{recipe_id}", json={}, headers=valid_headers)

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert "At least one updatable field must be provided." in response.json()["error"]
    finally:
        app.dependency_overrides = original_overrides


def test_patch_recipe_invalid_tags(
    test_client: TestClient,
    invalid_tag_patch_request: dict,
    valid_headers: dict,
    mock_recipe_service: Mock,
) -> None:
    recipe_id = "caf542de-d27b-4002-ab9c-3a757e2debec"

    # Store original overrides
    original_overrides = app.dependency_overrides.copy()

    # Override recipe service dependency
    app.dependency_overrides[get_recipe_service] = lambda: mock_recipe_service

    try:
        response = test_client.patch(f"/v1/recipes/{recipe_id}", json=invalid_tag_patch_request, headers=valid_headers)
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.json()["error"] == "Invalid recipe tags"
    finally:
        app.dependency_overrides = original_overrides


def test_patch_recipe_missing_partner_header(test_client: TestClient, valid_recipe_patch_request: dict) -> None:
    with pytest.raises(AccessDeniedException):
        test_client.patch("/v1/recipes", json=valid_recipe_patch_request)


@contextmanager
def delete_overrides(
    mock_partner_service: Mock, mock_recipe_service: Mock | None = None
) -> Generator[None, None, None]:
    original_overrides = app.dependency_overrides.copy()
    try:
        if mock_recipe_service:
            app.dependency_overrides[get_recipe_service] = lambda: mock_recipe_service
        app.dependency_overrides[get_partner_service] = lambda: mock_partner_service

        yield

    finally:
        app.dependency_overrides = original_overrides


def test_delete_recipe_success(
    test_client: TestClient,
    valid_headers: dict,
    mock_partner_service: Mock,
) -> None:
    recipe_id = "caf542de-d27b-4002-ab9c-3a757e2debec"

    mock_recipe_service = Mock()
    mock_recipe_service.delete_recipe.return_value = None

    with delete_overrides(mock_partner_service, mock_recipe_service):
        response = test_client.delete(f"/v1/recipes/{recipe_id}", headers=valid_headers)

        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert response.content == b""

        mock_partner_service.validate_partner_id.assert_called_once()
        mock_recipe_service.delete_recipe.assert_called_once_with("123", recipe_id)


def test_delete_recipe_not_found(
    test_client: TestClient,
    valid_headers: dict,
    mock_partner_service: Mock,
) -> None:
    recipe_id = "non-existent-recipe-id"

    mock_recipe_service = Mock()
    mock_recipe_service.delete_recipe.side_effect = RecipeNotFoundError(
        f"Recipe with ID {recipe_id} not found for partner 123"
    )

    with delete_overrides(mock_partner_service, mock_recipe_service):
        response = test_client.delete(f"/v1/recipes/{recipe_id}", headers=valid_headers)

        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert "not found" in response.json()["error"].lower()

        mock_partner_service.validate_partner_id.assert_called_once()
        mock_recipe_service.delete_recipe.assert_called_once_with("123", recipe_id)


def test_delete_recipe_already_deleted(
    test_client: TestClient,
    valid_headers: dict,
    mock_partner_service: Mock,
) -> None:
    recipe_id = "already-deleted-recipe-id"

    mock_recipe_service = Mock()
    mock_recipe_service.delete_recipe.side_effect = RecipeAlreadyDeletedError(
        f"Recipe with ID {recipe_id} is already deleted"
    )

    with delete_overrides(mock_partner_service, mock_recipe_service):
        response = test_client.delete(f"/v1/recipes/{recipe_id}", headers=valid_headers)

        assert response.status_code == status.HTTP_410_GONE
        assert "already deleted" in response.json()["error"].lower()

        mock_partner_service.validate_partner_id.assert_called_once()
        mock_recipe_service.delete_recipe.assert_called_once_with("123", recipe_id)


def test_delete_recipe_invalid_id_format(
    test_client: TestClient,
    valid_headers: dict,
    mock_partner_service: Mock,
) -> None:
    recipe_id = "invalid-uuid-format"

    mock_recipe_service = Mock()
    mock_recipe_service.delete_recipe.side_effect = ValueError(f"Invalid recipe ID format: {recipe_id}")

    with delete_overrides(mock_partner_service, mock_recipe_service):
        response = test_client.delete(f"/v1/recipes/{recipe_id}", headers=valid_headers)

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert "invalid recipe id format" in response.json()["error"].lower()

        mock_partner_service.validate_partner_id.assert_called_once()
        mock_recipe_service.delete_recipe.assert_called_once_with("123", recipe_id)


def test_delete_recipe_server_error(
    test_client: TestClient,
    valid_headers: dict,
    mock_partner_service: Mock,
) -> None:
    recipe_id = "caf542de-d27b-4002-ab9c-3a757e2debec"

    mock_recipe_service = Mock()
    mock_recipe_service.delete_recipe.side_effect = ServerError("Failed to connect to external service")

    with delete_overrides(mock_partner_service, mock_recipe_service):
        response = test_client.delete(f"/v1/recipes/{recipe_id}", headers=valid_headers)

        assert response.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR
        assert "external service" in response.json()["error"].lower()

        mock_partner_service.validate_partner_id.assert_called_once()
        mock_recipe_service.delete_recipe.assert_called_once_with("123", recipe_id)


def test_delete_recipe_missing_partner_header(test_client: TestClient) -> None:
    recipe_id = "caf542de-d27b-4002-ab9c-3a757e2debec"

    with pytest.raises(AccessDeniedException):
        test_client.delete(f"/v1/recipes/{recipe_id}")


def test_delete_recipe_invalid_partner(
    test_client: TestClient,
    valid_headers: dict,
) -> None:
    recipe_id = "caf542de-d27b-4002-ab9c-3a757e2debec"

    mock_partner_service = Mock()
    mock_partner_service.validate_partner_id.return_value = False
    mock_partner_service.partner_id = "invalid-partner"

    with delete_overrides(mock_partner_service):
        response = test_client.delete(f"/v1/recipes/{recipe_id}", headers=valid_headers)

        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        assert "failed to find partner" in response.json()["error"].lower()

        mock_partner_service.validate_partner_id.assert_called_once()


@pytest.fixture
def mock_recipe_service_for_get_recipes(recipes_response: list[RecipeResponse] | None = None) -> Mock:
    if recipes_response is None:
        recipes_response = [
            RecipeResponse(
                recipeId="recipe-1",
                cycleDate="2025-01-20",
                title="Test Recipe 1",
                subtitle="A delicious test recipe",
                pantryItems=[
                    RecipeIngredient(pantryItemId="pantry-1"),
                    RecipeIngredient(pantryItemId="pantry-2"),
                ],
                servings=2,
                isAddOn=False,
                recipeCardIds=["card-1"],
                recipeTags=RecipeTags(recipeConstraintTags=["wheatFree"]),
            ),
            RecipeResponse(
                recipeId="recipe-2",
                cycleDate="2025-01-20",
                title="Test Recipe 2",
                subtitle="Another delicious test recipe",
                pantryItems=[
                    RecipeIngredient(pantryItemId="pantry-3"),
                ],
                servings=2,
                isAddOn=True,
                recipeCardIds=["card-2"],
                recipeTags=RecipeTags(packagingConfigurationTags=["eco-friendly"]),
            ),
        ]

    mock = Mock()
    mock.get_recipes.return_value = recipes_response
    return mock


@contextmanager
def get_recipes_overrides(mock_partner_service: Mock, mock_recipe_service: Mock) -> Generator[None, Any, None]:
    original_overrides = app.dependency_overrides.copy()

    app.dependency_overrides[get_partner_service] = lambda: mock_partner_service
    app.dependency_overrides[get_recipe_service] = lambda: mock_recipe_service

    try:
        yield
    finally:
        app.dependency_overrides = original_overrides


def test_get_recipes_success(
    test_client: TestClient,
    valid_headers: dict,
    mock_partner_service: Mock,
    mock_recipe_service_for_get_recipes: Mock,
) -> None:
    cycle_date = "2025-01-20"

    with get_recipes_overrides(mock_partner_service, mock_recipe_service_for_get_recipes):
        response = test_client.get(f"/v1/recipes/{cycle_date}", headers=valid_headers)

        assert response.status_code == status.HTTP_200_OK
        data = response.json()

        assert "data" in data
        assert "recipes" in data["data"]
        assert len(data["data"]["recipes"]) == 2

        recipe1 = data["data"]["recipes"][0]
        assert recipe1["recipeId"] == "recipe-1"
        assert recipe1["title"] == "Test Recipe 1"
        assert recipe1["cycleDate"] == "2025-01-20"
        assert recipe1["isAddOn"] is False
        assert "pantryItems" in recipe1
        assert len(recipe1["pantryItems"]) == 2

        recipe2 = data["data"]["recipes"][1]
        assert recipe2["recipeId"] == "recipe-2"
        assert recipe2["title"] == "Test Recipe 2"
        assert recipe2["isAddOn"] is True
        assert "pantryItems" in recipe2
        assert len(recipe2["pantryItems"]) == 1

        mock_partner_service.validate_partner_id.assert_called_once()
        mock_recipe_service_for_get_recipes.get_recipes.assert_called_once_with(
            partner_id="123", cycle_date=cycle_date, recipe_ids=None
        )


def test_get_recipes_with_pagination(
    test_client: TestClient,
    valid_headers: dict,
    mock_partner_service: Mock,
    mock_recipe_service_for_get_recipes: Mock,
) -> None:
    cycle_date = "2025-01-20"

    with get_recipes_overrides(mock_partner_service, mock_recipe_service_for_get_recipes):
        response = test_client.get(f"/v1/recipes/{cycle_date}?page=1&pageSize=1", headers=valid_headers)

        assert response.status_code == status.HTTP_200_OK
        data = response.json()

        assert "meta" in data
        assert data["meta"]["pagination"]["current_page"] == 1
        assert data["meta"]["pagination"]["per_page"] == 1
        assert data["meta"]["pagination"]["total"] == 2
        assert data["meta"]["pagination"]["total_pages"] == 2

        assert "links" in data
        assert data["links"]["self"] is not None
        assert data["links"]["first"] is not None
        assert data["links"]["last"] is not None
        assert data["links"]["next"] is not None
        assert data["links"]["prev"] is None

        assert len(data["data"]["recipes"]) == 1


def test_get_recipes_with_recipe_ids_filter(
    test_client: TestClient,
    valid_headers: dict,
    mock_partner_service: Mock,
    mock_recipe_service_for_get_recipes: Mock,
) -> None:
    cycle_date = "2025-01-20"
    recipe_ids = "recipe-1,recipe-3"

    with get_recipes_overrides(mock_partner_service, mock_recipe_service_for_get_recipes):
        response = test_client.get(f"/v1/recipes/{cycle_date}?recipeIds={recipe_ids}", headers=valid_headers)

        assert response.status_code == status.HTTP_200_OK

        mock_recipe_service_for_get_recipes.get_recipes.assert_called_once_with(
            partner_id="123", cycle_date=cycle_date, recipe_ids=["recipe-1", "recipe-3"]
        )


def test_get_recipes_with_all_query_parameters(
    test_client: TestClient,
    valid_headers: dict,
    mock_partner_service: Mock,
    mock_recipe_service_for_get_recipes: Mock,
) -> None:
    cycle_date = "2025-01-20"
    recipe_ids = "recipe-1"

    with get_recipes_overrides(mock_partner_service, mock_recipe_service_for_get_recipes):
        response = test_client.get(
            f"/v1/recipes/{cycle_date}?page=2&pageSize=10&recipeIds={recipe_ids}", headers=valid_headers
        )

        assert response.status_code == status.HTTP_200_OK
        data = response.json()

        assert data["meta"]["pagination"]["current_page"] == 2
        assert data["meta"]["pagination"]["per_page"] == 10

        mock_recipe_service_for_get_recipes.get_recipes.assert_called_once_with(
            partner_id="123", cycle_date=cycle_date, recipe_ids=["recipe-1"]
        )


def test_get_recipes_empty_result(
    test_client: TestClient,
    valid_headers: dict,
    mock_partner_service: Mock,
) -> None:
    cycle_date = "2025-01-20"

    mock_recipe_service = Mock()
    mock_recipe_service.get_recipes.return_value = []

    with get_recipes_overrides(mock_partner_service, mock_recipe_service):
        response = test_client.get(f"/v1/recipes/{cycle_date}", headers=valid_headers)

        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert "Failed to find recipes" in response.json()["error"]


def test_get_recipes_invalid_partner(
    test_client: TestClient,
    valid_headers: dict,
) -> None:
    cycle_date = "2025-01-20"

    mock_partner_service = Mock()
    mock_partner_service.validate_partner_id.return_value = False
    mock_partner_service.partner_id = "invalid-partner"

    mock_recipe_service = Mock()

    with get_recipes_overrides(mock_partner_service, mock_recipe_service):
        response = test_client.get(f"/v1/recipes/{cycle_date}", headers=valid_headers)

        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        assert "failed to find partner" in response.json()["error"].lower()

        mock_partner_service.validate_partner_id.assert_called_once()
        mock_recipe_service.get_recipes.assert_not_called()


def test_get_recipes_missing_partner_header(test_client: TestClient) -> None:
    cycle_date = "2025-01-20"

    with pytest.raises(AccessDeniedException):
        test_client.get(f"/v1/recipes/{cycle_date}")


def test_get_recipes_invalid_page_parameter(
    test_client: TestClient,
    valid_headers: dict,
    mock_partner_service: Mock,
    mock_recipe_service_for_get_recipes: Mock,
) -> None:
    cycle_date = "2025-01-20"

    with get_recipes_overrides(mock_partner_service, mock_recipe_service_for_get_recipes):
        response = test_client.get(f"/v1/recipes/{cycle_date}?page=0", headers=valid_headers)

        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


def test_get_recipes_invalid_page_size_parameter(
    test_client: TestClient,
    valid_headers: dict,
    mock_partner_service: Mock,
    mock_recipe_service_for_get_recipes: Mock,
) -> None:
    cycle_date = "2025-01-20"

    with get_recipes_overrides(mock_partner_service, mock_recipe_service_for_get_recipes):
        response = test_client.get(f"/v1/recipes/{cycle_date}?pageSize=0", headers=valid_headers)

        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


def test_get_recipes_page_size_exceeds_maximum(
    test_client: TestClient,
    valid_headers: dict,
    mock_partner_service: Mock,
    mock_recipe_service_for_get_recipes: Mock,
) -> None:
    cycle_date = "2025-01-20"

    with get_recipes_overrides(mock_partner_service, mock_recipe_service_for_get_recipes):
        response = test_client.get(f"/v1/recipes/{cycle_date}?pageSize=1001", headers=valid_headers)

        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


def test_get_recipes_service_raises_value_error(
    test_client: TestClient,
    valid_headers: dict,
    mock_partner_service: Mock,
) -> None:
    cycle_date = "2025-01-20"

    mock_recipe_service = Mock()
    mock_recipe_service.get_recipes.side_effect = ValueError("Invalid cycle date format")

    with get_recipes_overrides(mock_partner_service, mock_recipe_service):
        response = test_client.get(f"/v1/recipes/{cycle_date}", headers=valid_headers)
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert "Invalid cycle date format" in response.json()["error"]

        mock_partner_service.validate_partner_id.assert_called_once()
        mock_recipe_service.get_recipes.assert_called_once()


def test_get_recipes_with_special_characters_in_cycle_date(
    test_client: TestClient,
    valid_headers: dict,
    mock_partner_service: Mock,
    mock_recipe_service_for_get_recipes: Mock,
) -> None:
    cycle_date = "2025-01-20%20"

    with get_recipes_overrides(mock_partner_service, mock_recipe_service_for_get_recipes):
        response = test_client.get(f"/v1/recipes/{cycle_date}", headers=valid_headers)

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert "Invalid cycle date format" in response.json()["error"]

        mock_recipe_service_for_get_recipes.get_recipes.assert_not_called()


def test_get_recipes_pagination_edge_cases(
    test_client: TestClient,
    valid_headers: dict,
    mock_partner_service: Mock,
) -> None:
    cycle_date = "2025-01-20"

    many_recipes = [
        RecipeResponse(
            recipeId=f"recipe-{i}",
            cycleDate=cycle_date,
            title=f"Test Recipe {i}",
            subtitle=f"Recipe number {i}",
            pantryItems=[RecipeIngredient(pantryItemId=f"pantry-{i}")],
            servings=2,
            isAddOn=False,
            recipeCardIds=[f"card-{i}"],
            recipeTags=RecipeTags(),
        )
        for i in range(1, 26)
    ]

    mock_recipe_service = Mock()
    mock_recipe_service.get_recipes.return_value = many_recipes

    with get_recipes_overrides(mock_partner_service, mock_recipe_service):
        response = test_client.get(f"/v1/recipes/{cycle_date}?page=3&pageSize=10", headers=valid_headers)

        assert response.status_code == status.HTTP_200_OK
        data = response.json()

        assert data["meta"]["pagination"]["current_page"] == 3
        assert data["meta"]["pagination"]["total_pages"] == 3
        assert data["meta"]["pagination"]["total"] == 25

        assert data["links"]["prev"] is not None
        assert data["links"]["next"] is None
        assert data["links"]["last"] is not None


def test_get_recipes_url_encoding_preserved(
    test_client: TestClient,
    valid_headers: dict,
    mock_partner_service: Mock,
    mock_recipe_service_for_get_recipes: Mock,
) -> None:
    cycle_date = "2025-01-20"
    recipe_ids = "recipe-1,recipe-2"

    with get_recipes_overrides(mock_partner_service, mock_recipe_service_for_get_recipes):
        response = test_client.get(
            f"/v1/recipes/{cycle_date}?recipeIds={recipe_ids}&page=1&pageSize=1", headers=valid_headers
        )

        assert response.status_code == status.HTTP_200_OK
        data = response.json()

        assert "recipeIds=recipe-1,recipe-2" in data["links"]["self"]
        assert "recipeIds=recipe-1,recipe-2" in data["links"]["next"]


def test_get_recipes_invalid_cycle_date_format(
    test_client: TestClient,
    valid_headers: dict,
    mock_partner_service: Mock,
    mock_recipe_service_for_get_recipes: Mock,
) -> None:
    cycle_date = "invalid-date-format"

    with get_recipes_overrides(mock_partner_service, mock_recipe_service_for_get_recipes):
        response = test_client.get(f"/v1/recipes/{cycle_date}", headers=valid_headers)

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert "Invalid cycle date format" in response.json()["error"]
        assert "Expected format: YYYY-MM-DD" in response.json()["error"]

        mock_recipe_service_for_get_recipes.get_recipes.assert_not_called()


def test_get_recipes_cycle_date_not_monday(
    test_client: TestClient,
    valid_headers: dict,
    mock_partner_service: Mock,
    mock_recipe_service_for_get_recipes: Mock,
) -> None:
    cycle_date = "2025-01-21"

    with get_recipes_overrides(mock_partner_service, mock_recipe_service_for_get_recipes):
        response = test_client.get(f"/v1/recipes/{cycle_date}", headers=valid_headers)

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert "must be a Monday" in response.json()["error"]

        mock_recipe_service_for_get_recipes.get_recipes.assert_not_called()


def test_get_recipes_valid_monday_cycle_date(
    test_client: TestClient,
    valid_headers: dict,
    mock_partner_service: Mock,
    mock_recipe_service_for_get_recipes: Mock,
) -> None:
    cycle_date = "2025-01-20"

    with get_recipes_overrides(mock_partner_service, mock_recipe_service_for_get_recipes):
        response = test_client.get(f"/v1/recipes/{cycle_date}", headers=valid_headers)

        assert response.status_code == status.HTTP_200_OK

        mock_recipe_service_for_get_recipes.get_recipes.assert_called_once_with(
            partner_id="123", cycle_date=cycle_date, recipe_ids=None
        )


@pytest.fixture
def mock_recipe_service_for_sku_mapping() -> Mock:
    mock = Mock()
    res: list[RecipeSku] = [
        RecipeSku(id="1c0ac0b5-39b3-4b9a-8f7f-5f8b9c1a4e2f", sku="604400001"),
        RecipeSku(id="2d1bd1c6-4a4c-5c8b-9g8g-6g9c0d2b5f3g", sku="604400002"),
    ]
    mock.get_recipe_ids_by_skus.return_value = res
    return mock


def test_get_recipes_by_skus_success(
    test_client: TestClient,
    valid_headers: dict,
    mock_partner_service: Mock,
    mock_recipe_service_for_sku_mapping: Mock,
) -> None:
    product_skus = "604400001,604400002"
    return_options = "recipe-id-sku-mapping"

    with get_recipes_overrides(mock_partner_service, mock_recipe_service_for_sku_mapping):
        response = test_client.get(
            f"/v1/recipes?product-skus={product_skus}&return-options={return_options}", headers=valid_headers
        )

        assert response.status_code == status.HTTP_200_OK
        data = response.json()

        assert len(data) == 2
        assert data[0]["id"] == "1c0ac0b5-39b3-4b9a-8f7f-5f8b9c1a4e2f"
        assert data[0]["sku"] == "604400001"
        assert data[1]["id"] == "2d1bd1c6-4a4c-5c8b-9g8g-6g9c0d2b5f3g"
        assert data[1]["sku"] == "604400002"

        mock_recipe_service_for_sku_mapping.get_recipe_ids_by_skus.assert_called_once_with(
            partner_id="123",
            product_skus=["604400001", "604400002"],
        )


def test_get_recipes_by_skus_missing_product_skus(
    test_client: TestClient,
    valid_headers: dict,
    mock_partner_service: Mock,
    mock_recipe_service_for_sku_mapping: Mock,
) -> None:
    return_options = "recipe-id-sku-mapping"

    with get_recipes_overrides(mock_partner_service, mock_recipe_service_for_sku_mapping):
        response = test_client.get(f"/v1/recipes?return-options={return_options}", headers=valid_headers)

        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


def test_get_recipes_by_skus_missing_return_options(
    test_client: TestClient,
    valid_headers: dict,
    mock_partner_service: Mock,
    mock_recipe_service_for_sku_mapping: Mock,
) -> None:
    product_skus = "604400001,604400002"

    with get_recipes_overrides(mock_partner_service, mock_recipe_service_for_sku_mapping):
        response = test_client.get(f"/v1/recipes?product-skus={product_skus}", headers=valid_headers)

        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


def test_get_recipes_by_skus_no_results(
    test_client: TestClient,
    valid_headers: dict,
    mock_partner_service: Mock,
) -> None:
    product_skus = "604400001,604400002"
    return_options = "recipe-id-sku-mapping"

    mock_recipe_service = Mock()
    mock_recipe_service.get_recipe_ids_by_skus.return_value = []

    with get_recipes_overrides(mock_partner_service, mock_recipe_service):
        response = test_client.get(
            f"/v1/recipes?product-skus={product_skus}&return-options={return_options}", headers=valid_headers
        )

        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert "Failed to find recipes for SKUs" in response.json()["error"]


def test_get_recipe_ids_by_skus_unknown_option_raises(
    test_client: TestClient,
    valid_headers: dict,
    mock_partner_service: Mock,
    mock_recipe_service_for_sku_mapping: Mock,
) -> None:
    product_skus = "604400001,604400002"

    with get_recipes_overrides(mock_partner_service, mock_recipe_service_for_sku_mapping):
        response = test_client.get(
            f"/v1/recipes?product-skus={product_skus}&return-options=invalid-option", headers=valid_headers
        )

        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
