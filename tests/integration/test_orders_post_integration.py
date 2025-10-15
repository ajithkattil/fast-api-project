import asyncio
import time
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
    MockKafkaProducer,
    cleanup_dependencies,
    mock_kafka_producer,
    setup_common_dependencies,
    setup_common_mocks,
    valid_headers,
    valid_order_post_request,
)


@pytest.fixture
def integration_test_client(mock_kafka_producer: MockKafkaProducer) -> Generator[TestClient, Any, None]:
    """Integration test client for FES Kafka tests."""
    with (
        patch("src.clients.kafka.base_producer.kafka.KafkaProducer") as mock_producer_class,
        patch("src.services.order.TaskScheduler") as mock_task_scheduler_class,
    ):
        mock_producer_class.return_value = mock_kafka_producer

        mock_task_scheduler_instance = MagicMock()

        def mock_schedule_async_task(task: Any) -> None:
            """Execute async task immediately for testing."""
            asyncio.run(task)

        mock_task_scheduler_instance.schedule_async_task = mock_schedule_async_task
        mock_task_scheduler_class.return_value = mock_task_scheduler_instance

        common_mocks = setup_common_mocks()
        mock_fulfillment_client = MagicMock()

        mock_fulfillment_producer = MagicMock()

        def mock_send_fulfillment_message(order: Any) -> None:
            mock_kafka_producer.send(settings.FULFILLMENT_TOPIC, "mock-message", order.id)

        mock_fulfillment_producer.send_fulfillment_message = mock_send_fulfillment_message
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


def test_orders_post_integration_with_fes_kafka_success(
    integration_test_client: TestClient,
    valid_order_post_request: dict,
    valid_headers: dict,
    mock_kafka_producer: MockKafkaProducer,
) -> None:
    """Tests successful order creation and FES Kafka message generation."""

    response = integration_test_client.post("/v1/orders", json=valid_order_post_request, headers=valid_headers)
    assert response.status_code == status.HTTP_202_ACCEPTED
    response_data = response.json()
    assert "data" in response_data
    assert "orderId" in response_data["data"]["order"]
    assert mock_kafka_producer.send_call_count == 1
    sent_message = mock_kafka_producer.sent_messages[0]
    topic, message, key = sent_message
    assert topic == settings.FULFILLMENT_TOPIC, f"Expected topic {settings.FULFILLMENT_TOPIC}, got {topic}"
    assert message == "mock-message", "Message should be our mock message"


@pytest.mark.skip(reason="temporarily disabled")
def test_orders_post_integration_with_fes_kafka_error_handling(
    integration_test_client: TestClient,
    valid_order_post_request: dict,
    valid_headers: dict,
) -> None:
    """Tests error handling when Kafka fails."""

    mock_fulfillment_producer = MagicMock()
    mock_fulfillment_producer.send_fulfillment_message.side_effect = Exception("Kafka connection failed")

    app.dependency_overrides[get_fulfillment_producer] = lambda: mock_fulfillment_producer

    with patch("src.services.order.TaskScheduler") as mock_task_scheduler_class:
        mock_task_scheduler_instance = MagicMock()
        mock_task_scheduler_instance.schedule_async_task = MagicMock()
        mock_task_scheduler_class.return_value = mock_task_scheduler_instance

        try:
            response = integration_test_client.post("/v1/orders", json=valid_order_post_request, headers=valid_headers)

            assert response.status_code == status.HTTP_202_ACCEPTED
            assert mock_task_scheduler_instance.schedule_async_task.called
        finally:
            if get_fulfillment_producer in app.dependency_overrides:
                del app.dependency_overrides[get_fulfillment_producer]


def test_orders_post_integration_async_task_execution(
    integration_test_client: TestClient,
    valid_order_post_request: dict,
    valid_headers: dict,
    mock_kafka_producer: MockKafkaProducer,
) -> None:
    """Tests async task execution for FES Kafka integration."""

    response = integration_test_client.post("/v1/orders", json=valid_order_post_request, headers=valid_headers)

    assert response.status_code == status.HTTP_202_ACCEPTED
    assert mock_kafka_producer.send_call_count == 1, "Async task should have executed and sent Kafka message"


def test_orders_post_integration_message_validation(
    integration_test_client: TestClient,
    valid_order_post_request: dict,
    valid_headers: dict,
    mock_kafka_producer: MockKafkaProducer,
) -> None:
    """Tests FES Kafka message format validation."""
    response = integration_test_client.post("/v1/orders", json=valid_order_post_request, headers=valid_headers)
    assert response.status_code == status.HTTP_202_ACCEPTED
    sent_message = mock_kafka_producer.sent_messages[0]
    topic, message, key = sent_message

    assert topic == settings.FULFILLMENT_TOPIC, "Topic should be correct"
    assert message == "mock-message", "Message should be our mock message"
    assert key is not None, "Key should be present"
