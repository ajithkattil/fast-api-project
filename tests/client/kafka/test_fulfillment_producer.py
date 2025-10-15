from collections.abc import Generator
from datetime import datetime
from unittest.mock import MagicMock, patch
from uuid import uuid4

import pytest
from blueapron.proto.FulfillmentManagementService.MessageFlow_pb2 import (
    ConsumerToFulfillmentMessage,
    FulfillmentOptions as ProtoFulfillmentOptions,
    FulfillmentRequest,
)
from blueapron.proto.shared.contacts.AssignedAddress_pb2 import LocationType as ProtoLocationType

from src.clients.kafka.fulfillment_producer import FulfillmentProducer
from src.core.exceptions import ServerError
from src.services.models.orders import (
    ContactNumber,
    FulfillmentOptions,
    LocationType,
    Order,
    OrderRecipe,
    PostalAddress,
    ShippingAddress,
    SpecialHandlings,
)


@pytest.fixture
def mock_base_producer_produce() -> Generator[MagicMock, None, None]:
    with patch.object(FulfillmentProducer, "produce") as mock_produce:
        yield mock_produce


@pytest.fixture
def fulfillment_producer() -> Generator[FulfillmentProducer, None, None]:
    with patch("src.clients.kafka.base_producer.kafka.KafkaProducer") as mock_producer:
        mock_producer_instance = MagicMock()
        mock_producer.return_value = mock_producer_instance
        yield FulfillmentProducer()


@pytest.fixture
def valid_order() -> Order:
    order_id = str(uuid4())
    return Order(
        id=order_id,
        sales_channel_id="business-channel",
        brand="test-brand",
        arrival_date=datetime(2025, 7, 15),
        fulfillable=True,
        shipping_address=ShippingAddress(
            postal_address=PostalAddress(
                postal_code="12345",
                administrative_area="CA",
                locality="City",
                address_lines=["123 First St"],
                recipients=["Frank James"],
            ),
            contact_number=ContactNumber(phone_number="555-555-5555"),
            location_type=LocationType.RESIDENTIAL,
            delivery_instructions="Leave at front door",
        ),
        recipes=[OrderRecipe(quantity=1, recipe_sku="SKU123")],
        fulfillment_options=FulfillmentOptions(
            delivery_option_token="token-abc",
            special_handlings=[SpecialHandlings.WHITE_GLOVE_BOX],
        ),
    )


def test_send_fulfillment_message_success(
    fulfillment_producer: FulfillmentProducer, mock_base_producer_produce: MagicMock, valid_order: Order
) -> None:
    fulfillment_producer.send_fulfillment_message(valid_order)

    mock_base_producer_produce.assert_called_once()
    args, _ = mock_base_producer_produce.call_args
    message = args[0]
    assert isinstance(message, ConsumerToFulfillmentMessage)

    req = message.fulfillment_request
    order_addr = valid_order.shipping_address
    req_addr = req.shipping_address

    assert req.fulfillment_reference_id.id == valid_order.id
    assert req.status == FulfillmentRequest.Status.FULFILLABLE
    assert req_addr.postal_address.postal_code == order_addr.postal_address.postal_code
    assert req_addr.postal_address.administrative_area == order_addr.postal_address.administrative_area
    assert req_addr.postal_address.locality == order_addr.postal_address.locality
    assert req_addr.postal_address.address_lines == order_addr.postal_address.address_lines
    assert req_addr.postal_address.recipients == order_addr.postal_address.recipients
    assert req_addr.contact_number.phone_number == order_addr.contact_number.phone_number
    assert req_addr.delivery_instructions == order_addr.delivery_instructions


def test_send_fulfillment_message_without_brand(
    fulfillment_producer: FulfillmentProducer, mock_base_producer_produce: MagicMock, valid_order: Order
) -> None:
    valid_order.brand = None
    fulfillment_producer.send_fulfillment_message(valid_order)

    mock_base_producer_produce.assert_called_once()


def test_send_fulfillment_message_without_sales_channel_id(
    fulfillment_producer: FulfillmentProducer, mock_base_producer_produce: MagicMock, valid_order: Order
) -> None:
    valid_order.sales_channel_id = None
    fulfillment_producer.send_fulfillment_message(valid_order)

    mock_base_producer_produce.assert_called_once()
    args, _ = mock_base_producer_produce.call_args
    message = args[0]
    assert isinstance(message, ConsumerToFulfillmentMessage)

    req = message.fulfillment_request
    assert req.sales_channel_id.id == ""


def test_send_fulfillment_message_without_delivery_instructions(
    fulfillment_producer: FulfillmentProducer, mock_base_producer_produce: MagicMock, valid_order: Order
) -> None:
    valid_order.shipping_address.delivery_instructions = None
    fulfillment_producer.send_fulfillment_message(valid_order)

    mock_base_producer_produce.assert_called_once()
    args, _ = mock_base_producer_produce.call_args
    message = args[0]
    assert isinstance(message, ConsumerToFulfillmentMessage)

    req = message.fulfillment_request
    req_addr = req.shipping_address
    assert not req_addr.delivery_instructions


def test_send_fulfillment_message_without_fulfillment_options(
    fulfillment_producer: FulfillmentProducer, mock_base_producer_produce: MagicMock, valid_order: Order
) -> None:
    valid_order.fulfillment_options = None
    fulfillment_producer.send_fulfillment_message(valid_order)

    mock_base_producer_produce.assert_called_once()
    args, _ = mock_base_producer_produce.call_args
    message = args[0]
    assert isinstance(message, ConsumerToFulfillmentMessage)

    req = message.fulfillment_request
    assert not req.HasField("fulfillment_options")


def test_send_fulfillment_message_without_delivery_option_token(
    fulfillment_producer: FulfillmentProducer, mock_base_producer_produce: MagicMock, valid_order: Order
) -> None:
    assert valid_order.fulfillment_options is not None
    valid_order.fulfillment_options.delivery_option_token = None
    fulfillment_producer.send_fulfillment_message(valid_order)

    mock_base_producer_produce.assert_called_once()
    args, _ = mock_base_producer_produce.call_args
    message = args[0]
    assert isinstance(message, ConsumerToFulfillmentMessage)

    req = message.fulfillment_request
    assert req.delivery_option_token == ""


def test_send_fulfillment_message_with_empty_special_handlings(
    fulfillment_producer: FulfillmentProducer, mock_base_producer_produce: MagicMock, valid_order: Order
) -> None:
    assert valid_order.fulfillment_options is not None
    valid_order.fulfillment_options.special_handlings = []

    fulfillment_producer.send_fulfillment_message(valid_order)

    mock_base_producer_produce.assert_called_once()
    args, _ = mock_base_producer_produce.call_args
    message = args[0]
    assert isinstance(message, ConsumerToFulfillmentMessage)

    req = message.fulfillment_request
    assert not req.HasField("fulfillment_options")


def test_send_fulfillment_message_producer_error(
    fulfillment_producer: FulfillmentProducer, mock_base_producer_produce: MagicMock, valid_order: Order
) -> None:
    mock_base_producer_produce.side_effect = ServerError("Kafka Error")

    with pytest.raises(ServerError):
        fulfillment_producer.send_fulfillment_message(valid_order)


def test_map_order_status() -> None:
    assert FulfillmentProducer._map_order_status(True) == FulfillmentRequest.Status.FULFILLABLE
    assert FulfillmentProducer._map_order_status(False) == FulfillmentRequest.Status.COMMITTED


def test_map_special_handlings() -> None:
    assert FulfillmentProducer._map_special_handlings([SpecialHandlings.WHITE_GLOVE_BOX]) == [
        ProtoFulfillmentOptions.SpecialHandling.WHITE_GLOVE_BOX
    ]
    assert FulfillmentProducer._map_special_handlings([SpecialHandlings.GUARANTEED_DELIVERY]) == [
        ProtoFulfillmentOptions.SpecialHandling.GUARANTEED_DELIVERY
    ]


def test_map_order_location_type() -> None:
    assert FulfillmentProducer._map_order_location_type(LocationType.RESIDENTIAL) == ProtoLocationType.RESIDENTIAL
    assert FulfillmentProducer._map_order_location_type(LocationType.COMMERCIAL) == ProtoLocationType.COMMERCIAL
