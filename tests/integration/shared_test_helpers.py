"""
Shared test helpers for integration tests.

This module contains common fixtures, mock classes, and utility functions
used across multiple integration test files.
"""

import uuid
from typing import Any
from unittest.mock import MagicMock

import jwt
import pytest

from src.api.routes.v1.models import SpecialHandlings
from src.db.mocks.idempotency_data import MockIdempotencyDB
from src.db.mocks.pantry_data import MockPantryDB
from src.db.mocks.partner_data import MockPartnerDB
from src.dependancies.culops_client import get_culops_client
from src.dependancies.idempotency_db import get_idempotency_db
from src.dependancies.pantry_db import get_pantry_db
from src.dependancies.partner_db import get_partner_db
from src.dependancies.partner_service import get_partner_service
from src.dependancies.recipe_db import get_recipes_db
from src.dependancies.token_service import get_token_service
from src.main import app
from src.services.partner import PartnerService
from src.services.token import TokenService
from src.utils.generate_pantry_mocks import generate_mock_pantry_items


def encode_jwt(payload: dict) -> str:
    """Encode JWT token for testing."""
    return jwt.encode(payload, "secret", algorithm="HS256")


class MockKafkaProducer:
    """Mock Kafka producer that captures messages without sending them to real Kafka."""

    def __init__(self) -> None:
        self.sent_messages: list[tuple[str, Any, str | None]] = []
        self.send_call_count = 0

    def send(self, topic: str, value: Any, key: str | None = None) -> MagicMock:
        self.sent_messages.append((topic, value, key))
        self.send_call_count += 1

        mock_future = MagicMock()
        mock_future.get.return_value = MagicMock()
        return mock_future


class MockFulfillmentClient:
    """Mock fulfillment client that captures calls without making real requests."""

    def __init__(self) -> None:
        self.update_order_call_count = 0
        self.mark_fulfillable_call_count = 0
        self.get_order_call_count = 0
        self.cancel_order_call_count = 0
        self.calls: list[tuple[str, Any]] = []

    def update_order(self, order: Any) -> Any:
        self.update_order_call_count += 1
        self.calls.append(("update_order", order))
        return self._create_mock_order()

    def mark_fulfillable(self, order_id: str, fulfillable: bool = True) -> Any:
        self.mark_fulfillable_call_count += 1
        self.calls.append(("mark_fulfillable", order_id))
        return self._create_mock_order()

    def get_order(self, order_id: str) -> Any:
        self.get_order_call_count += 1
        self.calls.append(("get_order", order_id))
        return self._create_mock_order()

    def cancel_order(self, order_id: str) -> None:
        self.cancel_order_call_count += 1
        self.calls.append(("cancel_order", order_id))

    def _create_mock_order(self) -> MagicMock:
        mock_order = MagicMock()
        from datetime import date

        mock_order.arrival_date = date(2025, 12, 20)
        mock_order.sales_channel_id = "AMAZON"
        mock_order.brand = "test-brand"
        mock_order.fulfillable = True
        mock_order.shipping_address = MagicMock()
        mock_order.shipping_address.postal_address = MagicMock()
        mock_order.shipping_address.postal_address.postal_code = "37203"
        mock_order.shipping_address.postal_address.administrative_area = "TN"
        mock_order.shipping_address.postal_address.locality = "Nashville"
        mock_order.shipping_address.contact_number = MagicMock()
        mock_order.shipping_address.contact_number.phone_number = "(615) 555-0123"
        mock_order.shipping_address.location_type = "RESIDENTIAL"
        mock_order.shipping_address.delivery_instructions = "Test instructions"
        from src.api.routes.v1.models import FulfillmentOptions

        mock_order.fulfillment_options = FulfillmentOptions(
            specialHandlings=[],
            deliveryOptionToken=str(uuid.uuid4()),
        )
        mock_order.line_items = []
        mock_order.fulfillment_reference_id = MagicMock()
        mock_order.fulfillment_reference_id.id = str(uuid.uuid4())
        mock_order.status = "PENDING"
        mock_order.target_arrival = MagicMock()
        mock_order.target_arrival.seconds = 1735689600
        mock_order.recipes = []

        return mock_order


@pytest.fixture
def mock_kafka_producer() -> MockKafkaProducer:
    """Fixture for mock Kafka producer."""
    return MockKafkaProducer()


@pytest.fixture
def mock_fulfillment_client() -> MockFulfillmentClient:
    """Fixture for mock fulfillment client."""
    return MockFulfillmentClient()


@pytest.fixture
def valid_headers() -> dict:
    """Valid headers for integration testing."""
    token = jwt.encode({"custom:partner_id": "BA-MAIN"}, "secret", algorithm="HS256")
    return {"Idempotency-Key": str(uuid.uuid4()), "Authorization": f"Bearer {token}"}


@pytest.fixture
def valid_order_post_request() -> dict:
    """Valid order post request for integration testing."""
    return {
        "arrivalDate": "2025-12-20",
        "salesChannelId": "AMAZON",
        "brandId": "test-brand",
        "fulfillmentOptions": {
            "specialHandlings": [
                SpecialHandlings.WHITE_GLOVE_BOX.name,
                SpecialHandlings.GUARANTEED_DELIVERY.name,
            ],
            "deliveryOptionToken": str(uuid.uuid4()),
        },
        "recipes": [{"recipeId": str(uuid.uuid4()), "quantity": 2}],
        "fulfillable": True,
        "shippingAddress": {
            "postalAddress": {
                "postalCode": "37203",
                "administrativeArea": "TN",
                "locality": "Nashville",
                "addressLines": ["123 Music Row", "Unit 5C"],
                "recipients": ["John Doe"],
            },
            "contactNumber": {"phoneNumber": "(615) 555-0123"},
            "locationType": "RESIDENTIAL",
            "deliveryInstructions": "Please leave the package on the front porch if no one answers.",
        },
    }


def setup_common_mocks() -> dict:
    """Setup common mock objects used in integration tests."""
    mock_items = generate_mock_pantry_items(items_per_pantry=3)
    mock_items[0].brand_name = "test-brand"

    def mock_get_partner_culops_pantry_data(
        available_from: Any = None,
        available_until: Any = None,
        partner_id: str = "",
        brand_name: str = "",
        page: int | None = None,
        page_size: int | None = None,
    ) -> Any:
        if brand_name == "test-brand":
            return iter([(mock_items, False)])
        else:
            return iter([])

    mock_culops_client = MagicMock()
    mock_culops_client.get_partner_culops_pantry_data.side_effect = mock_get_partner_culops_pantry_data

    mock_recipes_repo = MagicMock()
    mock_recipes_repo.get_recipe_sku_by_id.return_value = ("SKU-123", MagicMock(DELETED=False))

    from src.services.models.partner import Brand, SalesChannel

    class CustomMockPartnerDB(MockPartnerDB):
        def get_sales_channels(self, partner_id: str) -> list[SalesChannel]:
            return [
                SalesChannel(partner_id=partner_id, name="AMAZON", fes_name="amazon"),
                SalesChannel(partner_id=partner_id, name="WALMART", fes_name="walmart"),
            ]

        def get_branding(self, partner_id: str) -> list[Brand]:
            return [
                Brand(name="test-brand", partner_id=partner_id, fes_name="test-brand"),
            ]

    partner_db = CustomMockPartnerDB()
    partner_service = PartnerService(partner_id="BA-MAIN", partner_db=partner_db)

    return {
        "partner_db": partner_db,
        "pantry_db": MockPantryDB(),
        "idempotency_db": MockIdempotencyDB(),
        "partner_service": partner_service,
        "token_service": TokenService(param_store_client=MagicMock()),
        "culops_client": mock_culops_client,
        "recipes_db": mock_recipes_repo,
    }


def setup_common_dependencies(common_mocks: dict, additional_overrides: dict | None = None) -> None:
    """Setup common dependency overrides for integration tests."""
    app.dependency_overrides[get_partner_db] = lambda: common_mocks["partner_db"]
    app.dependency_overrides[get_pantry_db] = lambda: common_mocks["pantry_db"]
    app.dependency_overrides[get_idempotency_db] = lambda: common_mocks["idempotency_db"]
    app.dependency_overrides[get_partner_service] = lambda: common_mocks["partner_service"]
    app.dependency_overrides[get_token_service] = lambda: common_mocks["token_service"]
    app.dependency_overrides[get_culops_client] = lambda: common_mocks["culops_client"]
    app.dependency_overrides[get_recipes_db] = lambda: common_mocks["recipes_db"]

    if additional_overrides:
        app.dependency_overrides.update(additional_overrides)


def cleanup_dependencies() -> None:
    """Clean up dependency overrides after tests."""
    app.dependency_overrides = {}
