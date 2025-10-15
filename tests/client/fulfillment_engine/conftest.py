# Fixtures defined here are automatically available to ALL test files in this directory
# No imports needed - pytest magic discovers and injects them as test parameters
from uuid import UUID, uuid4

import pytest
from blueapron.proto.FulfillmentManagementService.Brand_pb2 import Brand
from blueapron.proto.FulfillmentManagementService.FulfillmentManagementService_pb2 import (
    GetFulfillmentResponse,
    MarkFulfillableResponse,
)
from blueapron.proto.FulfillmentManagementService.MessageFlow_pb2 import (
    CancelFulfillmentResponse,
    Fulfillment,
    FulfillmentOptions,
    FulfillmentReferenceId,
    SalesChannelId,
    TargetArrival,
)
from blueapron.proto.shared.contacts.AssignedAddress_pb2 import (
    AssignedAddress,
    LocationType,
)
from blueapron.proto.shared.contacts.PhoneNumber_pb2 import DialablePhone
from blueapron.proto.shared.LineItem_pb2 import LineItem as LineItem
from blueapron.proto.shared.Shipment_pb2 import Shipment
from blueapron.proto.shared.ShippingMethodId_pb2 import ShippingMethodId
from blueapron.proto.vendor.google.rpc.code_pb2 import Code
from blueapron.proto.vendor.google.rpc.status_pb2 import Status
from blueapron.proto.vendor.google.type.date_pb2 import Date
from blueapron.proto.vendor.google.type.postal_address_pb2 import PostalAddress


@pytest.fixture
def order_id() -> UUID:
    return uuid4()


def _create_shipping_address(
    location_type: LocationType | int = LocationType.RESIDENTIAL,
    delivery_instructions: str | None = "Leave at front door",
) -> AssignedAddress:
    return AssignedAddress(
        postal_address=PostalAddress(
            postal_code="12345",
            administrative_area="CA",
            locality="Test City",
            address_lines=["123 Test Street"],
            recipients=["Test Recipient"],
        ),
        contact_number=DialablePhone(phone_number="555-555-5555"),
        location_type=location_type,
        delivery_instructions=delivery_instructions,
    )


def _create_line_items(include_items: bool = True) -> list[LineItem]:
    if not include_items:
        return []
    return [
        LineItem(quantity=1, sku="TEST_SKU_123"),
        LineItem(quantity=2, sku="TEST_SKU_456"),
    ]


def _create_fulfillment(
    order_id: UUID,
    status: Fulfillment.Status = Fulfillment.Status.STATUS_ACTIVE,
    location_type: LocationType | int = LocationType.RESIDENTIAL,
    delivery_instructions: str | None = "Leave at front door",
    include_brand: bool = True,
    include_sales_channel: bool = True,
    include_line_items: bool = True,
    special_handlings: list | None = None,
) -> Fulfillment:
    fulfillment_kwargs = {
        "fulfillment_reference_id": FulfillmentReferenceId(id=str(order_id)),
        "status": status,
        "target_arrival": TargetArrival(arrival_date=Date(year=2025, month=7, day=15)),
        "shipping_address": _create_shipping_address(location_type, delivery_instructions),
        "line_items": _create_line_items(include_line_items),
        "shipments": [
            Shipment(
                shipping_method_id=ShippingMethodId(id=str(uuid4())),
            )
        ],
    }

    if include_brand:
        fulfillment_kwargs["brand"] = Brand(name="test-brand")

    if include_sales_channel:
        fulfillment_kwargs["sales_channel_id"] = SalesChannelId(id="test-sales-channel-id")

    if special_handlings is None:
        special_handlings = [FulfillmentOptions.SpecialHandling.WHITE_GLOVE_BOX]

    if special_handlings:
        fulfillment_kwargs["special_handlings"] = special_handlings

    return Fulfillment(**fulfillment_kwargs)


@pytest.fixture
def valid_fulfillment_response(order_id: UUID) -> GetFulfillmentResponse:
    fulfillment = _create_fulfillment(order_id)
    return GetFulfillmentResponse(fulfillment=fulfillment, status=Status(code=Code.OK))


@pytest.fixture
def not_found_response() -> GetFulfillmentResponse:
    return GetFulfillmentResponse(status=Status(code=Code.NOT_FOUND))


@pytest.fixture
def fulfillment_without_brand(order_id: UUID) -> GetFulfillmentResponse:
    fulfillment = _create_fulfillment(order_id, include_brand=False, include_sales_channel=False)
    return GetFulfillmentResponse(fulfillment=fulfillment, status=Status(code=Code.OK))


@pytest.fixture
def fulfillment_without_delivery_instructions(order_id: UUID) -> GetFulfillmentResponse:
    fulfillment = _create_fulfillment(order_id, delivery_instructions=None)
    return GetFulfillmentResponse(fulfillment=fulfillment, status=Status(code=Code.OK))


@pytest.fixture
def fulfillment_unfulfillable_status(order_id: UUID) -> GetFulfillmentResponse:
    fulfillment = _create_fulfillment(order_id, status=Fulfillment.Status.STATUS_UNFULFILLABLE)
    return GetFulfillmentResponse(fulfillment=fulfillment, status=Status(code=Code.OK))


@pytest.fixture
def fulfillment_commercial_location(order_id: UUID) -> GetFulfillmentResponse:
    fulfillment = _create_fulfillment(order_id, location_type=LocationType.COMMERCIAL)
    return GetFulfillmentResponse(fulfillment=fulfillment, status=Status(code=Code.OK))


@pytest.fixture
def fulfillment_invalid_location_type(order_id: UUID) -> GetFulfillmentResponse:
    fulfillment = _create_fulfillment(order_id, location_type=LocationType.UNKNOWN_LOCATION_TYPE)
    return GetFulfillmentResponse(fulfillment=fulfillment, status=Status(code=Code.OK))


@pytest.fixture
def fulfillment_guaranteed_delivery(order_id: UUID) -> GetFulfillmentResponse:
    fulfillment = _create_fulfillment(
        order_id, special_handlings=[FulfillmentOptions.SpecialHandling.GUARANTEED_DELIVERY]
    )
    return GetFulfillmentResponse(fulfillment=fulfillment, status=Status(code=Code.OK))


@pytest.fixture
def fulfillment_invalid_special_handling(order_id: UUID) -> GetFulfillmentResponse:
    fulfillment = _create_fulfillment(
        order_id,
        special_handlings=[
            FulfillmentOptions.SpecialHandling.UNKNOWN_SPECIAL_HANDLING,
            FulfillmentOptions.SpecialHandling.WHITE_GLOVE_BOX,
        ],
    )
    return GetFulfillmentResponse(fulfillment=fulfillment, status=Status(code=Code.OK))


@pytest.fixture
def invalid_argument_response() -> GetFulfillmentResponse:
    return GetFulfillmentResponse(status=Status(code=Code.INVALID_ARGUMENT))


@pytest.fixture
def invalid_argument_response_with_message() -> GetFulfillmentResponse:
    return GetFulfillmentResponse(status=Status(code=Code.INVALID_ARGUMENT, message="Order ID format is invalid"))


@pytest.fixture
def internal_error_response() -> GetFulfillmentResponse:
    return GetFulfillmentResponse(status=Status(code=Code.INTERNAL))


@pytest.fixture
def internal_error_response_with_message() -> GetFulfillmentResponse:
    return GetFulfillmentResponse(status=Status(code=Code.INTERNAL, message="Database connection failed"))


@pytest.fixture
def mark_fulfillable_success_response() -> MarkFulfillableResponse:
    return MarkFulfillableResponse(status=Status(code=Code.OK))


@pytest.fixture
def mark_fulfillable_not_found_response() -> MarkFulfillableResponse:
    return MarkFulfillableResponse(status=Status(code=Code.NOT_FOUND))


@pytest.fixture
def mark_fulfillable_invalid_argument_response() -> MarkFulfillableResponse:
    return MarkFulfillableResponse(status=Status(code=Code.INVALID_ARGUMENT))


@pytest.fixture
def mark_fulfillable_invalid_argument_response_with_message() -> MarkFulfillableResponse:
    return MarkFulfillableResponse(status=Status(code=Code.INVALID_ARGUMENT, message="Order is already fulfillable"))


@pytest.fixture
def mark_fulfillable_internal_error_response() -> MarkFulfillableResponse:
    return MarkFulfillableResponse(status=Status(code=Code.INTERNAL))


@pytest.fixture
def mark_fulfillable_internal_error_response_with_message() -> MarkFulfillableResponse:
    return MarkFulfillableResponse(status=Status(code=Code.INTERNAL, message="Failed to update fulfillment status"))


@pytest.fixture
def cancel_fulfillment_success_response() -> CancelFulfillmentResponse:
    return CancelFulfillmentResponse(status=Status(code=Code.OK))


@pytest.fixture
def cancel_fulfillment_not_found_response() -> CancelFulfillmentResponse:
    return CancelFulfillmentResponse(status=Status(code=Code.FAILED_PRECONDITION))


@pytest.fixture
def cancel_fulfillment_invalid_argument_response() -> CancelFulfillmentResponse:
    return CancelFulfillmentResponse(status=Status(code=Code.FAILED_PRECONDITION))


@pytest.fixture
def cancel_fulfillment_invalid_argument_response_with_message() -> CancelFulfillmentResponse:
    return CancelFulfillmentResponse(status=Status(code=Code.INVALID_ARGUMENT, message="Order cannot be canceled"))


@pytest.fixture
def cancel_fulfillment_internal_error_response() -> CancelFulfillmentResponse:
    return CancelFulfillmentResponse(status=Status(code=Code.INTERNAL))


@pytest.fixture
def cancel_fulfillment_internal_error_response_with_message() -> CancelFulfillmentResponse:
    return CancelFulfillmentResponse(status=Status(code=Code.INTERNAL, message="Database connection failed"))
