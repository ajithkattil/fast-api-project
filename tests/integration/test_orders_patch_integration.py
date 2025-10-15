import uuid
from collections.abc import Generator
from typing import Any
from unittest.mock import MagicMock

import pytest
from fastapi import status
from fastapi.testclient import TestClient

from src.dependancies.fulfillment_client import get_fulfillment_client
from src.dependancies.fulfillment_producer import get_fulfillment_producer
from src.dependancies.fulfillment_response_producer import get_fulfillment_response_producer
from src.main import app

from .shared_test_helpers import (
    MockFulfillmentClient,
    cleanup_dependencies,
    mock_fulfillment_client,
    setup_common_dependencies,
    setup_common_mocks,
    valid_headers,
)


@pytest.fixture
def patch_integration_test_client(mock_fulfillment_client: MockFulfillmentClient) -> Generator[TestClient, Any, None]:
    """Integration test client for PATCH order tests."""
    common_mocks = setup_common_mocks()
    mock_fulfillment_producer = MagicMock()
    mock_fulfillment_response_producer = MagicMock()

    setup_common_dependencies(
        common_mocks,
        {
            get_fulfillment_client: lambda: mock_fulfillment_client,
            get_fulfillment_producer: lambda: mock_fulfillment_producer,
            get_fulfillment_response_producer: lambda: mock_fulfillment_response_producer,
        },
    )

    with TestClient(app) as c:
        yield c
    cleanup_dependencies()


def test_orders_patch_integration_success(
    patch_integration_test_client: TestClient,
    valid_headers: dict,
    mock_fulfillment_client: MockFulfillmentClient,
) -> None:
    """Tests successful order update via FES."""
    order_id = str(uuid.uuid4())
    patch_request = {"arrivalDate": "2025-12-25"}

    response = patch_integration_test_client.patch(f"/v1/orders/{order_id}", json=patch_request, headers=valid_headers)

    assert response.status_code == status.HTTP_200_OK
    assert mock_fulfillment_client.get_order_call_count == 1
    assert mock_fulfillment_client.update_order_call_count == 1
    assert mock_fulfillment_client.mark_fulfillable_call_count == 0


def test_orders_patch_mark_fulfillable_only(
    patch_integration_test_client: TestClient,
    valid_headers: dict,
    mock_fulfillment_client: MockFulfillmentClient,
) -> None:
    """Tests PATCH with only fulfillable flag (uses mark_fulfillable FES call)."""
    order_id = str(uuid.uuid4())
    patch_request = {"fulfillable": True}

    response = patch_integration_test_client.patch(f"/v1/orders/{order_id}", json=patch_request, headers=valid_headers)

    assert response.status_code == status.HTTP_200_OK
    assert mock_fulfillment_client.mark_fulfillable_call_count == 1
    assert mock_fulfillment_client.update_order_call_count == 0
    assert mock_fulfillment_client.get_order_call_count == 0


def test_orders_patch_different_updates(
    patch_integration_test_client: TestClient,
    valid_headers: dict,
    mock_fulfillment_client: MockFulfillmentClient,
) -> None:
    """Tests PATCH with different update types via FES."""
    order_id = str(uuid.uuid4())

    response = patch_integration_test_client.patch(
        f"/v1/orders/{order_id}", json={"arrivalDate": "2025-12-25"}, headers=valid_headers
    )
    assert response.status_code == status.HTTP_200_OK

    response = patch_integration_test_client.patch(
        f"/v1/orders/{order_id}", json={"fulfillable": False}, headers=valid_headers
    )
    assert response.status_code == status.HTTP_200_OK

    response = patch_integration_test_client.patch(
        f"/v1/orders/{order_id}",
        json={"arrivalDate": "2025-12-30", "fulfillable": True},
        headers=valid_headers,
    )
    assert response.status_code == status.HTTP_200_OK

    assert mock_fulfillment_client.get_order_call_count == 3
    assert mock_fulfillment_client.update_order_call_count == 3


def test_orders_patch_error_handling(
    patch_integration_test_client: TestClient,
    valid_headers: dict,
) -> None:
    """Tests error handling when FES fails."""
    order_id = str(uuid.uuid4())
    patch_request = {"arrivalDate": "2025-12-25"}

    mock_fulfillment_client = MagicMock()
    mock_fulfillment_client.get_order.side_effect = Exception("FES connection failed")

    app.dependency_overrides[get_fulfillment_client] = lambda: mock_fulfillment_client

    try:
        with pytest.raises(Exception) as exc_info:
            patch_integration_test_client.patch(f"/v1/orders/{order_id}", json=patch_request, headers=valid_headers)

        assert "FES connection failed" in str(exc_info.value)
    finally:
        if get_fulfillment_client in app.dependency_overrides:
            del app.dependency_overrides[get_fulfillment_client]
