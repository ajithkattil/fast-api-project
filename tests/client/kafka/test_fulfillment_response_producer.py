from collections.abc import Generator
from unittest.mock import MagicMock, patch
from uuid import uuid4

import pytest
from blueapron.proto.FulfillmentManagementService.MessageFlow_pb2 import (
    FulfillmentReferenceId,
    FulfillmentResponse,
    FulfillmentToConsumerMessage,
    SalesChannelId,
)
from blueapron.proto.vendor.google.rpc.status_pb2 import Status
from google.protobuf.message import EncodeError

from src.clients.kafka.fulfillment_response_producer import FulfillmentResponseProducer
from src.core.exceptions import ServerError


@pytest.fixture
def mock_base_producer_produce() -> Generator[MagicMock, None, None]:
    with patch.object(FulfillmentResponseProducer, "produce") as mock_produce:
        yield mock_produce


@pytest.fixture
def mock_base_producer_value_serializer() -> Generator[MagicMock, None, None]:
    with patch.object(FulfillmentResponseProducer, "_value_serializer") as mock_value_serializer:
        yield mock_value_serializer


@pytest.fixture
def fulfillment_response_producer() -> Generator[FulfillmentResponseProducer, None, None]:
    with patch("src.clients.kafka.base_producer.kafka.KafkaProducer"):
        yield FulfillmentResponseProducer()


def test_send_fulfillment_response_failed_success(
    fulfillment_response_producer: FulfillmentResponseProducer, mock_base_producer_produce: MagicMock
) -> None:
    order_id = uuid4()
    sales_channel_id = "test_sales_channel_id"
    reason = "test_reason"

    fulfillment_response_producer.send_fulfillment_response_failed(order_id, reason, sales_channel_id)

    expected_message = FulfillmentToConsumerMessage(
        fulfillment_response=FulfillmentResponse(
            fulfillment_reference_id=FulfillmentReferenceId(id=str(order_id)),
            status=Status(code=FulfillmentResponse.Status.UNKNOWN, message=reason),
            sales_channel_id=SalesChannelId(id=sales_channel_id),
        )
    )
    mock_base_producer_produce.assert_called_once_with(expected_message)


def test_send_fulfillment_response_failed_no_sales_channel_id(
    fulfillment_response_producer: FulfillmentResponseProducer, mock_base_producer_produce: MagicMock
) -> None:
    order_id = uuid4()
    reason = "test_reason"

    fulfillment_response_producer.send_fulfillment_response_failed(order_id, reason)

    expected_message = FulfillmentToConsumerMessage(
        fulfillment_response=FulfillmentResponse(
            fulfillment_reference_id=FulfillmentReferenceId(id=str(order_id)),
            status=Status(code=FulfillmentResponse.Status.UNKNOWN, message=reason),
        )
    )
    mock_base_producer_produce.assert_called_once_with(expected_message)


def test_send_fulifillment_response_failed_missing_required_args(
    fulfillment_response_producer: FulfillmentResponseProducer,
) -> None:
    with pytest.raises(ValueError) as excinfo:
        fulfillment_response_producer.send_fulfillment_response_failed(uuid4(), "")

    assert "Reason and order_id are required for failed fulfillment response" in str(excinfo.value)


def test_send_fulfillment_response_failed_raises_server_error(
    fulfillment_response_producer: FulfillmentResponseProducer, mock_base_producer_produce: MagicMock
) -> None:
    order_id = uuid4()
    sales_channel_id = "test_sales_channel_id"
    reason = "test_reason"
    mock_base_producer_produce.side_effect = ServerError("Kafka error")

    with pytest.raises(ServerError) as excinfo:
        fulfillment_response_producer.send_fulfillment_response_failed(order_id, reason, sales_channel_id)

    assert "Failed to produce fulfillment response failed message" in str(excinfo.value)
    assert str(order_id) in str(excinfo.value)


def test_send_fulfillment_response_failed_protobuf_message_value_serializer_error() -> None:
    with patch("src.clients.kafka.base_producer.kafka.KafkaProducer") as mock_kafka_producer:
        mock_producer_instance = MagicMock()
        mock_kafka_producer.return_value = mock_producer_instance
        mock_producer_instance.send.side_effect = EncodeError("Failed to serialize protobuf message")

        producer = FulfillmentResponseProducer()

        with pytest.raises(ServerError) as excinfo:
            producer.send_fulfillment_response_failed(uuid4(), "reason")

        assert "Failed to produce fulfillment response failed message" in str(excinfo.value)
