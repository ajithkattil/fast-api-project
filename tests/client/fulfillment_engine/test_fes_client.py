from datetime import datetime
from unittest.mock import MagicMock, patch
from uuid import UUID

import grpc
import pytest
from blueapron.proto.FulfillmentManagementService.FulfillmentManagementService_pb2 import (
    GetFulfillmentResponse,
    MarkFulfillableResponse,
)
from blueapron.proto.FulfillmentManagementService.MessageFlow_pb2 import CancelFulfillmentResponse
from blueapron.proto.vendor.google.rpc.code_pb2 import Code

from src.clients.fulfillment_engine.client import FulfillmentEngineClient
from src.core.exceptions import OrderNotFoundError, ServerError
from src.services.models.orders import LocationType, SpecialHandlings

# Test fixtures (order_id, valid_fulfillment_response) are auto-injected from conftest.py


@pytest.fixture
def fulfillment_engine_client() -> FulfillmentEngineClient:
    with patch("src.clients.fulfillment_engine.client.FulfillmentEngineClient._get_channel") as mock_get_channel:
        mock_get_channel.return_value = MagicMock(spec=grpc.Channel)
    return FulfillmentEngineClient()


def test_get_fulfillment_success(
    fulfillment_engine_client: FulfillmentEngineClient,
    valid_fulfillment_response: GetFulfillmentResponse,
    order_id: UUID,
) -> None:
    with patch.object(
        fulfillment_engine_client.client,
        "GetFulfillment",
        return_value=valid_fulfillment_response,
    ):
        order = fulfillment_engine_client.get_order(order_id)

        assert order.id == str(order_id)
        assert order.fulfillable is True
        assert order.arrival_date == datetime(2025, 7, 15)
        assert order.brand == "test-brand"
        assert order.sales_channel_id == "test-sales-channel-id"

        assert order.shipping_address.postal_address.postal_code == "12345"
        assert order.shipping_address.postal_address.administrative_area == "CA"
        assert order.shipping_address.postal_address.locality == "Test City"
        assert order.shipping_address.postal_address.address_lines == ["123 Test Street"]
        assert order.shipping_address.postal_address.recipients == ["Test Recipient"]
        assert order.shipping_address.contact_number.phone_number == "555-555-5555"
        assert order.shipping_address.location_type == LocationType.RESIDENTIAL
        assert order.shipping_address.delivery_instructions == "Leave at front door"

        assert len(order.recipes) == 2
        assert order.recipes[0].quantity == 1
        assert order.recipes[0].recipe_sku == "TEST_SKU_123"
        assert order.recipes[1].quantity == 2
        assert order.recipes[1].recipe_sku == "TEST_SKU_456"

        assert order.fulfillment_options is not None
        assert order.fulfillment_options.special_handlings == [SpecialHandlings.WHITE_GLOVE_BOX]


def test_get_fulfillment_not_found(
    fulfillment_engine_client: FulfillmentEngineClient,
    not_found_response: GetFulfillmentResponse,
    order_id: UUID,
) -> None:
    with patch.object(
        fulfillment_engine_client.client,
        "GetFulfillment",
        return_value=not_found_response,
    ):
        with pytest.raises(
            OrderNotFoundError, match=f"Failed to get order, fulfillment not found for order {order_id}"
        ):
            fulfillment_engine_client.get_order(order_id)


def test_get_fulfillment_without_brand_or_sales_channel_id(
    fulfillment_engine_client: FulfillmentEngineClient,
    fulfillment_without_brand: GetFulfillmentResponse,
    order_id: UUID,
) -> None:
    with patch.object(
        fulfillment_engine_client.client,
        "GetFulfillment",
        return_value=fulfillment_without_brand,
    ):
        order = fulfillment_engine_client.get_order(order_id)

        assert order.brand is None
        assert order.sales_channel_id is None


def test_get_fulfillment_without_delivery_instructions(
    fulfillment_engine_client: FulfillmentEngineClient,
    fulfillment_without_delivery_instructions: GetFulfillmentResponse,
    order_id: UUID,
) -> None:
    with patch.object(
        fulfillment_engine_client.client,
        "GetFulfillment",
        return_value=fulfillment_without_delivery_instructions,
    ):
        order = fulfillment_engine_client.get_order(order_id)

        assert order.shipping_address.delivery_instructions is None


def test_get_fulfillment_unfulfillable_status(
    fulfillment_engine_client: FulfillmentEngineClient,
    fulfillment_unfulfillable_status: GetFulfillmentResponse,
    order_id: UUID,
) -> None:
    with patch.object(
        fulfillment_engine_client.client,
        "GetFulfillment",
        return_value=fulfillment_unfulfillable_status,
    ):
        order = fulfillment_engine_client.get_order(order_id)

        assert order.fulfillable is False


def test_get_fulfillment_commercial_location_type(
    fulfillment_engine_client: FulfillmentEngineClient,
    fulfillment_commercial_location: GetFulfillmentResponse,
    order_id: UUID,
) -> None:
    with patch.object(
        fulfillment_engine_client.client,
        "GetFulfillment",
        return_value=fulfillment_commercial_location,
    ):
        order = fulfillment_engine_client.get_order(order_id)

        assert order.shipping_address.location_type == LocationType.COMMERCIAL


def test_get_fulfillment_invalid_location_type_raises_server_error(
    fulfillment_engine_client: FulfillmentEngineClient,
    fulfillment_invalid_location_type: GetFulfillmentResponse,
    order_id: UUID,
) -> None:
    with patch.object(
        fulfillment_engine_client.client,
        "GetFulfillment",
        return_value=fulfillment_invalid_location_type,
    ):
        with pytest.raises(ServerError, match=f"Invalid location type.*{order_id}"):
            fulfillment_engine_client.get_order(order_id)


def test_get_fulfillment_guaranteed_delivery_special_handling(
    fulfillment_engine_client: FulfillmentEngineClient,
    fulfillment_guaranteed_delivery: GetFulfillmentResponse,
    order_id: UUID,
) -> None:
    with patch.object(
        fulfillment_engine_client.client,
        "GetFulfillment",
        return_value=fulfillment_guaranteed_delivery,
    ):
        order = fulfillment_engine_client.get_order(order_id)

        assert order.fulfillment_options is not None
        assert order.fulfillment_options.special_handlings == [SpecialHandlings.GUARANTEED_DELIVERY]


def test_get_fulfillment_invalid_special_handling_raises_server_error(
    fulfillment_engine_client: FulfillmentEngineClient,
    fulfillment_invalid_special_handling: GetFulfillmentResponse,
    order_id: UUID,
) -> None:
    with patch.object(
        fulfillment_engine_client.client,
        "GetFulfillment",
        return_value=fulfillment_invalid_special_handling,
    ):
        with pytest.raises(ServerError, match=f"Invalid special handling.*{order_id}"):
            fulfillment_engine_client.get_order(order_id)


def test_get_fulfillment_invalid_argument(
    fulfillment_engine_client: FulfillmentEngineClient,
    invalid_argument_response: GetFulfillmentResponse,
    order_id: UUID,
) -> None:
    with patch.object(
        fulfillment_engine_client.client,
        "GetFulfillment",
        return_value=invalid_argument_response,
    ):
        with pytest.raises(
            ValueError, match=f"Failed to get order, invalid argument getting fulfillment order {order_id}"
        ):
            fulfillment_engine_client.get_order(order_id)


def test_get_fulfillment_invalid_argument_with_message(
    fulfillment_engine_client: FulfillmentEngineClient,
    invalid_argument_response_with_message: GetFulfillmentResponse,
    order_id: UUID,
) -> None:
    with patch.object(
        fulfillment_engine_client.client,
        "GetFulfillment",
        return_value=invalid_argument_response_with_message,
    ):
        with pytest.raises(
            ValueError,
            match=(
                f"Failed to get order, invalid argument getting fulfillment order {order_id}: "
                "Order ID format is invalid"
            ),
        ):
            fulfillment_engine_client.get_order(order_id)


def test_get_fulfillment_internal_error(
    fulfillment_engine_client: FulfillmentEngineClient,
    internal_error_response: GetFulfillmentResponse,
    order_id: UUID,
) -> None:
    with patch.object(
        fulfillment_engine_client.client,
        "GetFulfillment",
        return_value=internal_error_response,
    ):
        with pytest.raises(
            ServerError, match=f"Failed to get order, internal error getting fulfillment order {order_id}"
        ):
            fulfillment_engine_client.get_order(order_id)


def test_get_fulfillment_internal_error_with_message(
    fulfillment_engine_client: FulfillmentEngineClient,
    internal_error_response_with_message: GetFulfillmentResponse,
    order_id: UUID,
) -> None:
    with patch.object(
        fulfillment_engine_client.client,
        "GetFulfillment",
        return_value=internal_error_response_with_message,
    ):
        with pytest.raises(
            ServerError,
            match=(
                f"Failed to get order, internal error getting fulfillment order {order_id}: Database connection failed"
            ),
        ):
            fulfillment_engine_client.get_order(order_id)


def test_get_fulfillment_grpc_error(
    fulfillment_engine_client: FulfillmentEngineClient,
    order_id: UUID,
) -> None:
    with patch.object(
        fulfillment_engine_client.client,
        "GetFulfillment",
        side_effect=grpc.RpcError("gRPC communication failed"),
    ):
        with pytest.raises(
            ServerError, match=f"Failed to get order, internal error getting fulfillment order {order_id}"
        ):
            fulfillment_engine_client.get_order(order_id)


def test_mark_fulfillable_success(
    fulfillment_engine_client: FulfillmentEngineClient,
    mark_fulfillable_success_response: MarkFulfillableResponse,
    valid_fulfillment_response: GetFulfillmentResponse,
    order_id: UUID,
) -> None:
    with (
        patch.object(
            fulfillment_engine_client.client,
            "MarkFulfillable",
            return_value=mark_fulfillable_success_response,
        ),
        patch.object(
            fulfillment_engine_client.client,
            "GetFulfillment",
            return_value=valid_fulfillment_response,
        ),
    ):
        order = fulfillment_engine_client.mark_fulfillable(order_id)

        assert order.id == str(order_id)
        assert order.fulfillable is True


def test_mark_fulfillable_not_found(
    fulfillment_engine_client: FulfillmentEngineClient,
    mark_fulfillable_not_found_response: MarkFulfillableResponse,
    order_id: UUID,
) -> None:
    with patch.object(
        fulfillment_engine_client.client,
        "MarkFulfillable",
        return_value=mark_fulfillable_not_found_response,
    ):
        with pytest.raises(
            OrderNotFoundError, match=f"Failed to mark fulfillable, fulfillment not found for order {order_id}"
        ):
            fulfillment_engine_client.mark_fulfillable(order_id)


def test_mark_fulfillable_invalid_argument(
    fulfillment_engine_client: FulfillmentEngineClient,
    mark_fulfillable_invalid_argument_response: MarkFulfillableResponse,
    order_id: UUID,
) -> None:
    with patch.object(
        fulfillment_engine_client.client,
        "MarkFulfillable",
        return_value=mark_fulfillable_invalid_argument_response,
    ):
        with pytest.raises(
            ValueError,
            match=f"Failed to mark fulfillable, invalid argument marking fulfillment order {order_id} as fulfillable",
        ):
            fulfillment_engine_client.mark_fulfillable(order_id)


def test_mark_fulfillable_invalid_argument_with_message(
    fulfillment_engine_client: FulfillmentEngineClient,
    mark_fulfillable_invalid_argument_response_with_message: MarkFulfillableResponse,
    order_id: UUID,
) -> None:
    with patch.object(
        fulfillment_engine_client.client,
        "MarkFulfillable",
        return_value=mark_fulfillable_invalid_argument_response_with_message,
    ):
        with pytest.raises(
            ValueError,
            match=(
                f"Failed to mark fulfillable, invalid argument marking fulfillment order {order_id} "
                "as fulfillable: Order is already fulfillable"
            ),
        ):
            fulfillment_engine_client.mark_fulfillable(order_id)


def test_mark_fulfillable_internal_error(
    fulfillment_engine_client: FulfillmentEngineClient,
    mark_fulfillable_internal_error_response: MarkFulfillableResponse,
    order_id: UUID,
) -> None:
    with patch.object(
        fulfillment_engine_client.client,
        "MarkFulfillable",
        return_value=mark_fulfillable_internal_error_response,
    ):
        with pytest.raises(
            ServerError,
            match=f"Failed to mark fulfillable, internal error marking fulfillment order {order_id} as fulfillable",
        ):
            fulfillment_engine_client.mark_fulfillable(order_id)


def test_mark_fulfillable_grpc_error(
    fulfillment_engine_client: FulfillmentEngineClient,
    order_id: UUID,
) -> None:
    with patch.object(
        fulfillment_engine_client.client,
        "MarkFulfillable",
        side_effect=grpc.RpcError("gRPC communication failed"),
    ):
        with pytest.raises(
            ServerError,
            match=(f"Failed to mark fulfillable, internal error marking fulfillment order {order_id} as fulfillable"),
        ):
            fulfillment_engine_client.mark_fulfillable(order_id)


def test_cancel_order_success(
    fulfillment_engine_client: FulfillmentEngineClient,
    cancel_fulfillment_success_response: CancelFulfillmentResponse,
    order_id: UUID,
) -> None:
    with patch.object(
        fulfillment_engine_client.client,
        "CancelFulfillment",
        return_value=cancel_fulfillment_success_response,
    ):
        fulfillment_engine_client.cancel_order(order_id)
        assert cancel_fulfillment_success_response.status.code == Code.OK


def test_cancel_order_not_found(
    fulfillment_engine_client: FulfillmentEngineClient,
    cancel_fulfillment_not_found_response: CancelFulfillmentResponse,
    order_id: UUID,
) -> None:
    with patch.object(
        fulfillment_engine_client.client,
        "CancelFulfillment",
        return_value=cancel_fulfillment_not_found_response,
    ):
        with pytest.raises(
            OrderNotFoundError, match=f"Failed to cancel order, fulfillment not found for order {order_id}"
        ):
            fulfillment_engine_client.cancel_order(order_id)


def test_cancel_order_internal_error(
    fulfillment_engine_client: FulfillmentEngineClient,
    cancel_fulfillment_internal_error_response: CancelFulfillmentResponse,
    order_id: UUID,
) -> None:
    with patch.object(
        fulfillment_engine_client.client,
        "CancelFulfillment",
        return_value=cancel_fulfillment_internal_error_response,
    ):
        with pytest.raises(
            ServerError,
            match=f"Failed to cancel order, internal error canceling fulfillment order {order_id}",
        ):
            fulfillment_engine_client.cancel_order(order_id)


def test_cancel_order_internal_error_with_message(
    fulfillment_engine_client: FulfillmentEngineClient,
    cancel_fulfillment_internal_error_response_with_message: CancelFulfillmentResponse,
    order_id: UUID,
) -> None:
    with patch.object(
        fulfillment_engine_client.client,
        "CancelFulfillment",
        return_value=cancel_fulfillment_internal_error_response_with_message,
    ):
        with pytest.raises(
            ServerError,
            match=(
                f"Failed to cancel order, internal error canceling fulfillment order {order_id}: "
                "Database connection failed"
            ),
        ):
            fulfillment_engine_client.cancel_order(order_id)


def test_cancel_order_grpc_error(
    fulfillment_engine_client: FulfillmentEngineClient,
    order_id: UUID,
) -> None:
    with patch.object(
        fulfillment_engine_client.client,
        "CancelFulfillment",
        side_effect=grpc.RpcError("gRPC communication failed"),
    ):
        with pytest.raises(
            ServerError,
            match=f"Failed to cancel order, internal error canceling fulfillment order {order_id}",
        ):
            fulfillment_engine_client.cancel_order(order_id)
