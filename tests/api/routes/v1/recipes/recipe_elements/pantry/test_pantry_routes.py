from math import ceil
from typing import Any

import pytest
from fastapi import status
from fastapi.testclient import TestClient

from src.api.routes.v1.models import GetPantry
from src.core.exceptions import AccessDeniedException
from src.utils.paginator import PaginatedResponse
from tests.conftest import encode_jwt


@pytest.mark.parametrize(
    "params",
    [
        ({}),
        ({"page": 1}),
        ({"pageSize": 100}),
        ({"availableFrom": "2025-05-01"}),
        ({"availableUntil": "2025-05-10"}),
        (
            {
                "page": 1,
                "pageSize": 100,
                "pantryItems": 12345,
            }
        ),
        ({"brand": "samuri pizza cat"}),
        ({"brand": "samuri pizza cat", "availableFrom": "2025-06-05", "availableUntil": "2025-07-10"}),
    ],
)
def test_get_pantry_param_success_cases(params: Any, test_client: TestClient) -> None:
    headers = {"Authorization": f"Bearer {encode_jwt({'custom:partner_id': 'BA-MAIN'})}"}
    response = test_client.get("/v1/recipes/recipeelements/pantry", params=params, headers=headers)
    assert response.status_code == status.HTTP_200_OK
    json_data = response.json()
    assert "data" in json_data
    assert "meta" in json_data
    assert "links" in json_data
    assert "pantry" in json_data["data"]
    assert isinstance(json_data["data"]["pantry"]["pantryItems"], list)


@pytest.mark.parametrize(
    "params,expected_status",
    [
        ({"page": -1}, status.HTTP_422_UNPROCESSABLE_ENTITY),
        ({"pageSize": 0}, status.HTTP_422_UNPROCESSABLE_ENTITY),
        ({"availableFrom": "not-a-date"}, status.HTTP_400_BAD_REQUEST),
        ({"availableUntil": "not-a-date"}, status.HTTP_400_BAD_REQUEST),
        ({"pantryItems": 12345}, status.HTTP_200_OK),
        ({}, status.HTTP_200_OK),
    ],
)
def test_get_pantry_param_edge_cases(params: Any, expected_status: int, test_client: TestClient) -> None:
    headers = {"Authorization": f"Bearer {encode_jwt({'custom:partner_id': 'BA-MAIN'})}"}
    response = test_client.get("/v1/recipes/recipeelements/pantry", params=params, headers=headers)
    assert response.status_code == expected_status


def test_get_pantry_errors_when_missing_partner_id(test_client: TestClient) -> None:
    with pytest.raises(AccessDeniedException):
        test_client.get("/v1/recipes/recipeelements/pantry")


def validate_links(
    response_data: PaginatedResponse[GetPantry],
    base_url: str,
    page_size: int,
    pantry_state_id: str,
    current_page: int,
) -> None:
    """Helper function to validate the links section in the response."""
    assert "links" in response_data
    assert "self" in response_data["links"]
    assert "first" in response_data["links"]
    assert "last" in response_data["links"]
    assert "prev" in response_data["links"]
    assert "next" in response_data["links"]

    total_pages = response_data["meta"]["pagination"]["total_pages"]
    url_base = f"{base_url}?availableFrom=&availableUntil=&pageSize={page_size}&pantryStateId={pantry_state_id}&"

    expected_self = f"{url_base}page={current_page}"
    expected_first = f"{url_base}page=1"
    expected_last = f"{url_base}page={total_pages}"
    expected_next = None
    expected_prev = None

    if current_page == 1 and current_page < total_pages:
        expected_next = f"{url_base}page={current_page + 1}"
    if current_page > 1:
        expected_prev = f"{url_base}page={current_page - 1}"

    assert response_data["links"]["self"] == expected_self
    assert response_data["links"]["first"] == expected_first
    assert response_data["links"]["last"] == expected_last
    assert response_data["links"]["next"] == expected_next
    assert response_data["links"]["prev"] == expected_prev


def validate_meta(response_data: PaginatedResponse[GetPantry], page_size: int, expected_page: int = 1) -> None:
    """Helper function to validate the meta section in the response."""
    assert "meta" in response_data
    assert "pagination" in response_data["meta"]
    assert "total" in response_data["meta"]["pagination"]
    assert "per_page" in response_data["meta"]["pagination"]
    assert "current_page" in response_data["meta"]["pagination"]
    assert "total_pages" in response_data["meta"]["pagination"]

    total_items = response_data["meta"]["pagination"]["total"]
    total_pages = ceil(total_items / page_size)

    assert response_data["meta"]["pagination"]["per_page"] == page_size
    assert response_data["meta"]["pagination"]["current_page"] == expected_page
    assert response_data["meta"]["pagination"]["total_pages"] == total_pages


def test_get_paginated_pantry_all_pages(test_client: TestClient) -> None:
    base_url = "http://localhost:8000/v1/recipes/recipeelements/pantry"
    page_size = 100
    pantry_state_id = "12345"
    page = 1

    next_url = (
        f"{base_url}?availableFrom=&availableUntil=&pageSize={page_size}&pantryStateId={pantry_state_id}&page={page}"
    )
    while next_url:
        headers = {"Authorization": f"Bearer {encode_jwt({'custom:partner_id': 'BA-MAIN'})}"}
        response = test_client.get(next_url, headers=headers)
        assert response.status_code == status.HTTP_200_OK

        data = response.json()

        validate_links(data, base_url, page_size, pantry_state_id, page)
        validate_meta(data, page_size, page)

        next_url = data["links"]["next"]
        page += 1


def test_get_pantry_with_existing_brand(test_client: TestClient) -> None:
    headers = {"Authorization": f"Bearer {encode_jwt({'custom:partner_id': 'BA-MAIN'})}"}
    params = {"brand": "samuri pizza cat"}
    response = test_client.get("/v1/recipes/recipeelements/pantry", params=params, headers=headers)
    assert response.status_code == status.HTTP_200_OK
    json_data = response.json()
    pantry_items = json_data["data"]["pantry"]["pantryItems"]
    assert isinstance(pantry_items, list)
    assert any(item.get("brand") == "samuri pizza cat" for item in pantry_items)


def test_get_pantry_with_non_existing_brand_filters_out_matching_items(test_client: TestClient) -> None:
    headers = {"Authorization": f"Bearer {encode_jwt({'custom:partner_id': 'BA-MAIN'})}"}
    params = {"brand": "NonExistentBrandXYZ"}
    response = test_client.get("/v1/recipes/recipeelements/pantry", params=params, headers=headers)

    assert response.status_code == status.HTTP_200_OK

    pantry_items = response.json()["data"]["pantry"]["pantryItems"]
    assert isinstance(pantry_items, list)

    for item in pantry_items:
        assert "brand" not in item or item["brand"] in (None, "")
