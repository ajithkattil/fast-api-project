from datetime import datetime
from unittest.mock import MagicMock
from uuid import uuid4

import pytest
from pydantic import ValidationError

from src.api.routes.v1.models import (
    Address,
    ContactNumber,
    FulfillmentOptions,
    OrderPatchRequest,
    OrderRecipe,
    OrderResponse,
    PostalAddress,
)
from src.core.exceptions import RecipeAlreadyDeletedError, ServerError
from src.services.models.orders import LocationType, Order, ShippingAddress
from src.services.models.recipe import CulopsRecipeRef
from src.services.order import OrderService
from src.utils.task_scheduler import TaskScheduler
from tests.services.fixtures.test_order_fixtures import order_post_request


class MockRecipeStatus:
    def __init__(self, deleted: bool) -> None:
        self.DELETED = deleted


@pytest.fixture
def mocked_dependencies() -> tuple[MagicMock, MagicMock, MagicMock, MagicMock, MagicMock, MagicMock, MagicMock]:
    partner_repo = MagicMock()
    pantry_repo = MagicMock()
    culops_client = MagicMock()
    fulfillment_client = MagicMock()
    fulfillment_producer = MagicMock()
    fulfillment_response_producer = MagicMock()
    recipes_repo = MagicMock()
    return (
        partner_repo,
        pantry_repo,
        culops_client,
        fulfillment_client,
        fulfillment_producer,
        fulfillment_response_producer,
        recipes_repo,
    )


@pytest.fixture
def order_service(
    mocked_dependencies: tuple[MagicMock, MagicMock, MagicMock, MagicMock, MagicMock, MagicMock, MagicMock],
) -> OrderService:
    (
        partner_repo,
        pantry_repo,
        culops_client,
        fulfillment_client,
        fulfillment_producer,
        fulfillment_response_producer,
        recipes_repo,
    ) = mocked_dependencies
    t = TaskScheduler()
    t.start()
    return OrderService(
        partner_repo=partner_repo,
        pantry_repo=pantry_repo,
        culops_client=culops_client,
        fulfillment_client=fulfillment_client,
        fulfillment_producer=fulfillment_producer,
        fulfillment_response_producer=fulfillment_response_producer,
        recipes_repo=recipes_repo,
    )


def test_create_order_success(
    order_service: OrderService,
    mocked_dependencies: tuple[MagicMock, MagicMock, MagicMock, MagicMock, MagicMock, MagicMock, MagicMock],
) -> None:
    _, _, _, _, fulfillment_producer, _, recipe_repo = mocked_dependencies

    # Mocking order input and dependencies
    partner_id = "test_partner"
    order_data = order_post_request()

    recipe_repo.get_recipe_sku_by_id.return_value = ("123456", MockRecipeStatus(deleted=False))

    fulfillment_producer.send_fulfillment_message = MagicMock()

    # Call function
    result = order_service.create_order(partner_id, order_data)

    # Assertions
    assert isinstance(result, OrderResponse)


def test_create_order_recipe_not_found(
    order_service: OrderService,
    mocked_dependencies: tuple[MagicMock, MagicMock, MagicMock, MagicMock, MagicMock, MagicMock, MagicMock],
) -> None:
    _, _, _, _, _, _, recipe_repo = mocked_dependencies

    # Mocking order input and dependencies
    partner_id = "test_partner"
    order_data = order_post_request()

    recipe_repo.get_recipe_sku_by_id.return_value = None

    # Assertions
    with pytest.raises(ValueError, match="not found"):
        order_service.create_order(partner_id, order_data)


def test_create_order_recipe_deleted(
    order_service: OrderService,
    mocked_dependencies: tuple[MagicMock, MagicMock, MagicMock, MagicMock, MagicMock, MagicMock, MagicMock],
) -> None:
    _, _, _, _, _, _, recipe_repo = mocked_dependencies

    partner_id = "test_partner"
    recipe_id = order_post_request().recipes[0].recipe_id
    order_data = order_post_request()

    recipe_repo.get_recipe_sku_by_id.return_value = ("123456", MockRecipeStatus(deleted=True))

    recipe_ref = CulopsRecipeRef(culops_recipe_id=1, recipe_id=recipe_id, deleted=True)
    recipe_repo.get_culops_recipe_ref_by_id.return_value = recipe_ref

    # Assertions
    with pytest.raises(ValueError, match="is deleted"):
        order_service.create_order(partner_id, order_data)


def get_mock_order() -> Order:
    return Order(
        id="ORD-123",
        arrival_date=datetime.fromisoformat("2025-07-15T00:00:00"),
        fulfillable=True,
        shipping_address=ShippingAddress(
            postal_address=PostalAddress(
                postalCode="12345",
                administrativeArea="CA",
                locality="LA",
                addressLines=["123 Street"],
                recipients=["Alice"],
            ),
            contact_number=ContactNumber(phoneNumber="+15551234567"),
            location_type=LocationType.RESIDENTIAL,
            delivery_instructions="Leave at door",
        ),
        recipes=[],
        brand="BRAND-01",
        fulfillment_options=FulfillmentOptions(specialHandlings=["fragile"], deliveryOptionToken="TOKEN-123"),
        sales_channel_id="SC-123",
    )


def test_update_order_fulfillable_only(
    order_service: OrderService,
    mocked_dependencies: tuple[MagicMock, MagicMock, MagicMock, MagicMock, MagicMock, MagicMock, MagicMock],
) -> None:
    _, _, _, fulfillment_client, _, _, _ = mocked_dependencies

    order_id = uuid4()
    patch_data = OrderPatchRequest(fulfillable=True)

    mock_updated_order = get_mock_order()
    fulfillment_client.mark_fulfillable.return_value = mock_updated_order

    result = order_service.update_order("partner-1", order_id, patch_data)

    assert result.order_id == "ORD-123"
    fulfillment_client.mark_fulfillable.assert_called_once_with(order_id=order_id)


def test_update_order_full_success(
    order_service: OrderService,
    mocked_dependencies: tuple[MagicMock, MagicMock, MagicMock, MagicMock, MagicMock, MagicMock, MagicMock],
) -> None:
    _, _, _, fulfillment_client, _, _, recipes_repo = mocked_dependencies

    recipe_id = uuid4()

    order_id = uuid4()
    patch_data = OrderPatchRequest(
        arrival_date="2025-07-20",
        fulfillable=False,
        recipes=[OrderRecipe(recipeId=recipe_id, quantity=2)],
        brand="BRAND-42",
        sales_channel_id="SC-999",
        shipping_address=Address(
            postalAddress=PostalAddress(
                postalCode="98765",
                administrativeArea="TX",
                locality="Austin",
                addressLines=["Apt 101"],
                recipients=["Bob"],
            ),
            contactNumber=ContactNumber(phoneNumber="+18885554444"),
            locationType="business",
            deliveryInstructions="Back door",
        ),
        fulfillment_options=FulfillmentOptions(specialHandlings=["frozen"], deliveryOptionToken="NEW-TOKEN-999"),
    )

    mock_current_order = get_mock_order()
    fulfillment_client.get_order.return_value = mock_current_order

    recipes_repo.get_recipe_sku_by_id.return_value = ("123456", MockRecipeStatus(deleted=False))

    fulfillment_client.update_order.return_value = get_mock_order()

    result = order_service.update_order("partner-1", order_id, patch_data)

    assert result.order_id == "ORD-123"
    fulfillment_client.update_order.assert_called_once()


def test_update_order_with_deleted_recipe(
    order_service: OrderService,
    mocked_dependencies: tuple[MagicMock, MagicMock, MagicMock, MagicMock, MagicMock, MagicMock, MagicMock],
) -> None:
    _, _, _, fulfillment_client, _, _, recipes_repo = mocked_dependencies

    recipe_id = uuid4()
    order_id = uuid4()
    patch_data = OrderPatchRequest(
        recipes=[OrderRecipe(recipeId=recipe_id, quantity=1)],
    )

    fulfillment_client.get_order.return_value = get_mock_order()

    recipes_repo.get_recipe_sku_by_id.return_value = ("123456", MockRecipeStatus(deleted=True))

    with pytest.raises(RecipeAlreadyDeletedError):
        order_service.update_order("partner-1", order_id, patch_data)


def test_update_order_missing_fulfillment(
    order_service: OrderService,
    mocked_dependencies: tuple[MagicMock, MagicMock, MagicMock, MagicMock, MagicMock, MagicMock, MagicMock],
) -> None:
    _, _, _, fulfillment_client, _, _, _ = mocked_dependencies

    order_id = uuid4()
    patch_data = OrderPatchRequest(fulfillment_options=FulfillmentOptions(specialHandlings=[], deliveryOptionToken=""))

    fulfillment_client.get_order.return_value = None

    with pytest.raises(ValueError, match=f"No fulfillment found for order ID: {order_id}"):
        order_service.update_order("partner-1", order_id, patch_data)


def test_update_order_empty_request(
    order_service: OrderService,
    mocked_dependencies: tuple[MagicMock, MagicMock, MagicMock, MagicMock, MagicMock, MagicMock, MagicMock],
) -> None:
    _, _, _, fulfillment_client, _, _, _ = mocked_dependencies

    order_id = uuid4()

    with pytest.raises(ValidationError):
        order_service.update_order("partner-1", order_id, OrderPatchRequest())


def test_delete_order_success_logs_and_calls_client(
    order_service: OrderService,
    mocked_dependencies: tuple[MagicMock, MagicMock, MagicMock, MagicMock, MagicMock, MagicMock, MagicMock],
) -> None:
    _, _, _, fulfillment_client, _, _, _ = mocked_dependencies

    order_id = uuid4()

    order_service.delete_order(partner_id="partner1", order_id=order_id)

    fulfillment_client.cancel_order.assert_called_once_with(order_id=order_id)


def test_delete_order_client_raises_logs_and_raises(
    order_service: OrderService,
    mocked_dependencies: tuple[MagicMock, MagicMock, MagicMock, MagicMock, MagicMock, MagicMock, MagicMock],
) -> None:
    _, _, _, fulfillment_client, _, _, _ = mocked_dependencies

    fulfillment_client.cancel_order.side_effect = ServerError("grpc error")

    order_id = uuid4()

    with pytest.raises(ServerError):
        order_service.delete_order(partner_id="partner1", order_id=order_id)
