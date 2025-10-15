import asyncio
import uuid
from collections.abc import Generator
from typing import Any
from unittest.mock import MagicMock, patch

import pytest
from fastapi import status
from fastapi.testclient import TestClient

from src.core.config import settings
from src.dependancies.fulfillment_client import get_fulfillment_client
from src.dependancies.fulfillment_producer import get_fulfillment_producer
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
def integration_test_client(mock_fulfillment_client: MockFulfillmentClient) -> Generator[TestClient, Any, None]:
    """Integration test client for FES gRPC tests."""
    with patch("src.clients.kafka.base_producer.kafka.KafkaProducer") as mock_producer_class:
        mock_producer_class.return_value = MagicMock()

        common_mocks = setup_common_mocks()
        mock_fulfillment_producer = MagicMock()

        setup_common_dependencies(
            common_mocks,
            {
                get_fulfillment_client: lambda: mock_fulfillment_client,
                get_fulfillment_producer: lambda: mock_fulfillment_producer,
            },
        )

        with TestClient(app) as c:
            yield c
        cleanup_dependencies()


@pytest.fixture
def valid_order_id() -> str:
    """Valid order ID for testing."""
    return str(uuid.uuid4())


def test_orders_delete_integration_with_fes_grpc_success(
    integration_test_client: TestClient,
    valid_headers: dict,
    valid_order_id: str,
    mock_fulfillment_client: MockFulfillmentClient,
) -> None:
    """Tests successful order deletion and FES gRPC call."""

    response = integration_test_client.delete(f"/v1/orders/{valid_order_id}", headers=valid_headers)
    assert response.status_code == status.HTTP_204_NO_CONTENT
    assert mock_fulfillment_client.cancel_order_call_count == 1


def test_orders_delete_integration_with_fes_grpc_error_handling(
    integration_test_client: TestClient,
    valid_headers: dict,
    valid_order_id: str,
) -> None:
    """Tests error handling when gRPC fails."""

    mock_fulfillment_client = MagicMock()
    mock_fulfillment_client.cancel_order.side_effect = Exception("gRPC connection failed")

    app.dependency_overrides[get_fulfillment_client] = lambda: mock_fulfillment_client

    try:
        with pytest.raises(Exception, match="gRPC connection failed"):
            integration_test_client.delete(f"/v1/orders/{valid_order_id}", headers=valid_headers)
    finally:
        if get_fulfillment_client in app.dependency_overrides:
            del app.dependency_overrides[get_fulfillment_client]


def test_orders_delete_integration_grpc_call_validation(
    integration_test_client: TestClient,
    valid_headers: dict,
    valid_order_id: str,
    mock_fulfillment_client: MockFulfillmentClient,
) -> None:
    """Tests FES gRPC call validation."""
    response = integration_test_client.delete(f"/v1/orders/{valid_order_id}", headers=valid_headers)
    assert response.status_code == status.HTTP_204_NO_CONTENT
    assert mock_fulfillment_client.cancel_order_call_count == 1
    calls = mock_fulfillment_client.calls
    assert len(calls) == 1
    assert calls[0][0] == "cancel_order"
    assert str(calls[0][1]) == valid_order_id


def test_orders_delete_integration_grpc_execution(
    integration_test_client: TestClient,
    valid_headers: dict,
    valid_order_id: str,
    mock_fulfillment_client: MockFulfillmentClient,
) -> None:
    """Tests gRPC execution for FES integration."""

    response = integration_test_client.delete(f"/v1/orders/{valid_order_id}", headers=valid_headers)

    assert response.status_code == status.HTTP_204_NO_CONTENT
    assert mock_fulfillment_client.cancel_order_call_count == 1, "gRPC call should have executed"
