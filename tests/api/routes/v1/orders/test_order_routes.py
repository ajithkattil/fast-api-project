import uuid
from typing import Any
from unittest.mock import Mock

import pytest
from fastapi import status
from fastapi.testclient import TestClient

from src.api.routes.v1.models import (
    Address,
    ContactNumber,
    FulfillmentOptions,
    OrderRecipe,
    OrderResponse,
    PostalAddress,
    SpecialHandlings,
)
from src.core.exceptions import (
    ServerError,
    UnprocessableException,
)
from src.dependancies.fulfillment_client import get_fulfillment_client
from src.dependancies.idempotency_db import get_idempotency_db
from src.dependancies.order_service import get_order_service
from src.dependancies.partner_service import get_partner_service
from src.dependancies.recipe_db import get_recipes_db
from src.main import app
from src.services.models.partner import Brand, SalesChannel
from tests.conftest import encode_jwt


@pytest.fixture
def valid_order_post_request() -> dict:
    return {
        "arrivalDate": "2025-12-20",
        "salesChannelId": "AMAZON",
        "brandId": None,
        "fulfillmentOptions": {
            "specialHandlings": [
                SpecialHandlings.WHITE_GLOVE_BOX.name,
                SpecialHandlings.GUARANTEED_DELIVERY.name,
            ],
            "deliveryOptionToken": str(uuid.uuid4()),
        },
        "recipes": [{"recipeId": str(uuid.uuid4()), "quantity": 1}],
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


@pytest.fixture
def valid_headers() -> dict:
    auth_header = encode_jwt({"custom:partner_id": "partner-123"})
    return {"Idempotency-Key": str(uuid.uuid4()), "Authorization": f"Bearer {auth_header}"}


@pytest.fixture
def mock_partner_service(valid_partner: bool = True) -> Mock:
    mock = Mock()
    mock.validate_partner_id.return_value = valid_partner
    mock.partner_id = "partner-123"
    mock.get_branding.return_value = [Brand(name="Test Brand", partner_id=mock.partner_id, fes_name="brand1")]
    mock.get_sales_channels.return_value = [
        SalesChannel(
            partner_id="partner-123",
            name="AMAZON",
            fes_name="amazon",
        ),
        SalesChannel(
            partner_id="partner-123",
            name="WALMART",
            fes_name="walmart",
        ),
    ]
    return mock


@pytest.fixture
def mock_idempotency_repo(key_exists: bool = False) -> Mock:
    mock = Mock()
    mock.idempotency_key_exists.return_value = key_exists
    mock.add_idempotency_key.return_value = None
    return mock


@pytest.fixture
def mock_order_service() -> Mock:
    mock_order_service = Mock()

    mock_order_service.create_order.return_value = OrderResponse(
        orderId=str(uuid.uuid4()),
        arrivalDate="2025-12-20",
        recipes=[OrderRecipe(recipeId=uuid.uuid4(), quantity=1)],
        fulfillable=True,
        salesChannelId="AMAZON",
        brandId=None,
        shippingAddress=Address(
            postalAddress=PostalAddress(
                postalCode="37203",
                administrativeArea="TN",
                locality="Nashville",
                addressLines=["123 Music Row", "Unit 5C"],
                recipients=["John Doe"],
            ),
            contactNumber=ContactNumber(phoneNumber="(615) 555-0123"),
            locationType="RESIDENTIAL",
            deliveryInstructions="Please leave the package on the front porch if no one answers.",
        ),
        fulfillmentOptions=FulfillmentOptions(
            specialHandlings=["WHITE_GLOVE_BOX", "GUARANTEED_DELIVERY"], deliveryOptionToken=str(uuid.uuid4())
        ),
    )
    mock_order_service.update_order.return_value = OrderResponse(
        orderId=str(uuid.uuid4()),
        arrivalDate="2025-12-22",
        recipes=[OrderRecipe(recipeId=uuid.uuid4(), quantity=2)],
        fulfillable=False,
        salesChannelId="WALMART",
        brandId=None,
        shippingAddress=Address(
            postalAddress=PostalAddress(
                postalCode="312345",
                administrativeArea="TN",
                locality="Nashville",
                addressLines=["456 Music Row", "Unit 6C"],
                recipients=["Jane Doe"],
            ),
            contactNumber=ContactNumber(phoneNumber="(615) 555-1234"),
            locationType="RESIDENTIAL",
            deliveryInstructions="Please leave the package on the back porch if no one answers.",
        ),
        fulfillmentOptions=FulfillmentOptions(
            specialHandlings=["WHITE_GLOVE_BOX"], deliveryOptionToken=str(uuid.uuid4())
        ),
    )

    def dynamic_update_order(partner_id: str, order_id: uuid.UUID, order_data: Any) -> OrderResponse:
        return OrderResponse(
            orderId=str(order_id),
            arrivalDate=order_data.arrival_date,
            recipes=order_data.recipes or [],
            fulfillable=order_data.fulfillable,
            salesChannelId=order_data.sales_channel_id,
            brandId=order_data.brand_id,
            shippingAddress=order_data.shipping_address,
            fulfillmentOptions=order_data.fulfillment_options,
        )

    mock_order_service.update_order.side_effect = dynamic_update_order

    return mock_order_service


def override_dependencies(mock_partner_service: Mock, mock_idempotency_repo: Mock, mock_order_service: Mock) -> None:
    app.dependency_overrides[get_partner_service] = lambda: mock_partner_service
    app.dependency_overrides[get_idempotency_db] = lambda: mock_idempotency_repo
    app.dependency_overrides[get_order_service] = lambda: mock_order_service
    app.dependency_overrides[get_fulfillment_client] = lambda: Mock()
    app.dependency_overrides[get_recipes_db] = lambda: Mock()


def reset_dependencies() -> None:
    app.dependency_overrides = {}


def test_post_order_success(
    test_client: TestClient,
    valid_order_post_request: dict,
    valid_headers: dict,
    mock_partner_service: Mock,
    mock_idempotency_repo: Mock,
    mock_order_service: Mock,
) -> None:
    override_dependencies(mock_partner_service, mock_idempotency_repo, mock_order_service)

    response = test_client.post("/v1/orders", json=valid_order_post_request, headers=valid_headers)

    assert response.status_code == status.HTTP_202_ACCEPTED
    json_data = response.json()
    assert "data" in json_data
    assert isinstance(json_data["data"]["order"]["recipes"], list)
    mock_partner_service.validate_partner_id.assert_called_once()
    mock_idempotency_repo.idempotency_key_exists.assert_called_once()
    mock_idempotency_repo.add_idempotency_key.assert_called_once()
    mock_order_service.create_order.assert_called_once()
    reset_dependencies()


@pytest.mark.parametrize(
    "invalid_channel_id, expected_status, expected_detail_substring",
    [
        ("INVALID_CHANNEL", 400, "Invalid sales channel id"),
        ("99999", 400, "Invalid sales channel id"),
        (12345, 422, "String_type salesChannelId"),
    ],
)
def test_post_order_invalid_sales_channel_id(
    test_client: TestClient,
    valid_order_post_request: dict,
    valid_headers: dict,
    mock_partner_service: Mock,
    mock_idempotency_repo: Mock,
    mock_order_service: Mock,
    invalid_channel_id: str | int,
    expected_status: int,
    expected_detail_substring: str,
) -> None:
    valid_order_post_request["salesChannelId"] = invalid_channel_id
    override_dependencies(mock_partner_service, mock_idempotency_repo, mock_order_service)

    response = test_client.post("/v1/orders", json=valid_order_post_request, headers=valid_headers)

    assert response.status_code == expected_status
    assert expected_detail_substring in str(response.json()["error"])

    reset_dependencies()


def test_post_order_rejects_invalid_brand_id(
    test_client: TestClient,
    valid_order_post_request: dict,
    valid_headers: dict,
    mock_partner_service: Mock,
    mock_idempotency_repo: Mock,
    mock_order_service: Mock,
) -> None:
    valid_order_post_request["brandId"] = "invalid brand"
    override_dependencies(mock_partner_service, mock_idempotency_repo, mock_order_service)

    response = test_client.post("/v1/orders", json=valid_order_post_request, headers=valid_headers)

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert "Brand invalid brand not found" in response.json()["error"]
    reset_dependencies()


def test_post_order_success_with_valid_brand(
    test_client: TestClient,
    valid_order_post_request: dict,
    valid_headers: dict,
    mock_partner_service: Mock,
    mock_idempotency_repo: Mock,
    mock_order_service: Mock,
) -> None:
    valid_order_post_request["brandId"] = "Test Brand"
    override_dependencies(mock_partner_service, mock_idempotency_repo, mock_order_service)

    response = test_client.post("/v1/orders", json=valid_order_post_request, headers=valid_headers)

    assert response.status_code == status.HTTP_202_ACCEPTED
    reset_dependencies()


def test_post_order_invalid_special_handling(
    test_client: TestClient,
    valid_order_post_request: dict,
    valid_headers: dict,
    mock_partner_service: Mock,
    mock_idempotency_repo: Mock,
    mock_order_service: Mock,
) -> None:
    valid_order_post_request["fulfillmentOptions"]["specialHandlings"] = ["INVALID_HANDLING"]
    override_dependencies(mock_partner_service, mock_idempotency_repo, mock_order_service)

    response = test_client.post("/v1/orders", json=valid_order_post_request, headers=valid_headers)

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert "Invalid special_handling" in response.json()["error"]
    reset_dependencies()


def test_post_order_invalid_delivery_option_token(
    test_client: TestClient,
    valid_order_post_request: dict,
    valid_headers: dict,
    mock_partner_service: Mock,
    mock_idempotency_repo: Mock,
    mock_order_service: Mock,
) -> None:
    valid_order_post_request["fulfillmentOptions"]["deliveryOptionToken"] = "not-a-uuid"
    override_dependencies(mock_partner_service, mock_idempotency_repo, mock_order_service)

    response = test_client.post("/v1/orders", json=valid_order_post_request, headers=valid_headers)

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert "Delivery option token is not valid" in response.json()["error"]
    reset_dependencies()


def test_post_order_access_denied(
    test_client: TestClient,
    valid_order_post_request: dict,
    valid_headers: dict,
    mock_idempotency_repo: Mock,
    mock_order_service: Mock,
) -> None:
    mock_partner_service = Mock()
    mock_partner_service.validate_partner_id.return_value = False
    mock_partner_service.partner_id = "partner-123"
    override_dependencies(mock_partner_service, mock_idempotency_repo, mock_order_service)

    response = test_client.post("/v1/orders", json=valid_order_post_request, headers=valid_headers)

    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert "Failed to find partner" in response.json()["error"]
    reset_dependencies()


def test_post_order_conflict_on_existing_idempotency_key(
    test_client: TestClient,
    valid_order_post_request: dict,
    valid_headers: dict,
    mock_partner_service: Mock,
    mock_order_service: Mock,
) -> None:
    mock_idempotency_repo = Mock()
    mock_idempotency_repo.idempotency_key_exists.return_value = True
    mock_idempotency_repo.add_idempotency_key.return_value = None
    override_dependencies(mock_partner_service, mock_idempotency_repo, mock_order_service)

    response = test_client.post("/v1/orders", json=valid_order_post_request, headers=valid_headers)

    assert response.status_code == status.HTTP_409_CONFLICT
    assert "Idempotency key already exists" in response.json()["error"]
    reset_dependencies()


@pytest.mark.parametrize(
    "exception, expected_status, expected_detail",
    [
        (UnprocessableException("Recipe not found"), status.HTTP_422_UNPROCESSABLE_ENTITY, "Recipe not found"),
        (
            UnprocessableException("Recipe already deleted"),
            status.HTTP_422_UNPROCESSABLE_ENTITY,
            "Recipe already deleted",
        ),
        (ServerError("Server error"), status.HTTP_500_INTERNAL_SERVER_ERROR, "Server error"),
        (ValueError("Some value error"), status.HTTP_400_BAD_REQUEST, "Some value error"),
    ],
)
def test_post_order_exception_handling(
    test_client: TestClient,
    valid_order_post_request: dict,
    valid_headers: dict,
    mock_partner_service: Mock,
    mock_idempotency_repo: Mock,
    mock_order_service: Mock,
    exception: Exception,
    expected_status: int,
    expected_detail: str,
) -> None:
    def raise_exception(*args: Any, **kwargs: Any) -> None:
        raise exception

    mock_order_service.create_order.side_effect = raise_exception
    override_dependencies(mock_partner_service, mock_idempotency_repo, mock_order_service)

    response = test_client.post("/v1/orders", json=valid_order_post_request, headers=valid_headers)

    assert response.status_code == expected_status
    assert expected_detail in response.json()["error"]
    reset_dependencies()


def test_post_order_missing_idempotency_key(
    test_client: TestClient,
    valid_order_post_request: dict,
    mock_partner_service: Mock,
    mock_idempotency_repo: Mock,
    mock_order_service: Mock,
) -> None:
    override_dependencies(mock_partner_service, mock_idempotency_repo, mock_order_service)

    auth_header = encode_jwt({"custom:partner_id": "partner-123"})

    response = test_client.post(
        "/v1/orders", json=valid_order_post_request, headers={"Authorization": f"Bearer {auth_header}"}
    )

    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    assert "Missing Idempotency-Key" in response.json()["error"]
    reset_dependencies()


@pytest.fixture
def valid_order_patch_request() -> dict:
    return {
        "arrivalDate": "2025-12-22",
        "salesChannelId": "WALMART",
        "brandId": None,
        "fulfillmentOptions": {
            "specialHandlings": [
                SpecialHandlings.WHITE_GLOVE_BOX.name,
            ],
            "deliveryOptionToken": str(uuid.uuid4()),
        },
        "recipes": [{"recipeId": str(uuid.uuid4()), "quantity": 2}],
        "fulfillable": False,
        "shippingAddress": {
            "postalAddress": {
                "postalCode": "312345",
                "administrativeArea": "TN",
                "locality": "Nashville",
                "addressLines": ["456 Music Row", "Unit 6C"],
                "recipients": ["Jane Doe"],
            },
            "contactNumber": {"phoneNumber": "(615) 555-1234"},
            "locationType": "RESIDENTIAL",
            "deliveryInstructions": "Please leave the package on the back porch if no one answers.",
        },
    }


def test_patch_order_success(
    test_client: TestClient,
    valid_order_patch_request: dict,
    valid_headers: dict,
    mock_partner_service: Mock,
    mock_order_service: Mock,
) -> None:
    order_id = str(uuid.uuid4())

    override_dependencies(mock_partner_service, Mock(), mock_order_service)

    response = test_client.patch(f"/v1/orders/{order_id}", json=valid_order_patch_request, headers=valid_headers)

    assert response.status_code == status.HTTP_200_OK
    assert "data" in response.json()
    assert response.json()["data"]["order"]["orderId"] == order_id
    reset_dependencies()


def test_patch_order_empty_recipes_error(
    test_client: TestClient,
    valid_order_patch_request: dict,
    valid_headers: dict,
    mock_partner_service: Mock,
    mock_order_service: Mock,
) -> None:
    order_id = str(uuid.uuid4())
    valid_order_patch_request["recipes"] = []

    override_dependencies(mock_partner_service, Mock(), mock_order_service)

    response = test_client.patch(f"/v1/orders/{order_id}", json=valid_order_patch_request, headers=valid_headers)

    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    error_msg = response.json()["error"]
    assert "Too_short recipes" in error_msg
    reset_dependencies()


def test_patch_order_invalid_sales_channel(
    test_client: TestClient,
    valid_order_patch_request: dict,
    valid_headers: dict,
    mock_partner_service: Mock,
    mock_order_service: Mock,
) -> None:
    order_id = str(uuid.uuid4())
    valid_order_patch_request["salesChannelId"] = "INVALID"

    override_dependencies(mock_partner_service, Mock(), mock_order_service)

    response = test_client.patch(f"/v1/orders/{order_id}", json=valid_order_patch_request, headers=valid_headers)

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert "Invalid sales channel id" in response.json()["error"]
    reset_dependencies()


def test_patch_order_invalid_special_handling(
    test_client: TestClient,
    valid_order_patch_request: dict,
    valid_headers: dict,
    mock_partner_service: Mock,
    mock_order_service: Mock,
) -> None:
    order_id = str(uuid.uuid4())
    valid_order_patch_request["fulfillmentOptions"]["specialHandlings"] = ["INVALID_OPTION"]

    override_dependencies(mock_partner_service, Mock(), mock_order_service)

    response = test_client.patch(f"/v1/orders/{order_id}", json=valid_order_patch_request, headers=valid_headers)

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert "Invalid special_handling" in response.json()["error"]
    reset_dependencies()


def test_patch_order_empty_fulfillment_options(
    test_client: TestClient,
    valid_order_patch_request: dict,
    valid_headers: dict,
    mock_partner_service: Mock,
    mock_order_service: Mock,
) -> None:
    order_id = str(uuid.uuid4())
    valid_order_patch_request["fulfillmentOptions"]["specialHandlings"] = []
    override_dependencies(mock_partner_service, Mock(), mock_order_service)
    response = test_client.patch(f"/v1/orders/{order_id}", json=valid_order_patch_request, headers=valid_headers)

    assert response.status_code == status.HTTP_200_OK
    assert response.json()["data"]["order"]["fulfillmentOptions"]["specialHandlings"] == []
    reset_dependencies()


def test_patch_order_invalid_delivery_option_token(
    test_client: TestClient,
    valid_order_patch_request: dict,
    valid_headers: dict,
    mock_partner_service: Mock,
    mock_order_service: Mock,
) -> None:
    order_id = str(uuid.uuid4())
    valid_order_patch_request["fulfillmentOptions"]["deliveryOptionToken"] = "not-a-uuid"

    override_dependencies(mock_partner_service, Mock(), mock_order_service)

    response = test_client.patch(f"/v1/orders/{order_id}", json=valid_order_patch_request, headers=valid_headers)

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert "Delivery option token is not valid" in response.json()["error"]
    reset_dependencies()


def test_patch_order_access_denied(
    test_client: TestClient,
    valid_order_patch_request: dict,
    valid_headers: dict,
    mock_order_service: Mock,
) -> None:
    mock_partner_service = Mock()
    mock_partner_service.validate_partner_id.return_value = False
    mock_partner_service.partner_id = "partner-123"

    order_id = str(uuid.uuid4())
    override_dependencies(mock_partner_service, Mock(), mock_order_service)

    response = test_client.patch(f"/v1/orders/{order_id}", json=valid_order_patch_request, headers=valid_headers)

    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert "Failed to find partner" in response.json()["error"]
    reset_dependencies()


@pytest.mark.parametrize(
    "exception, expected_status, expected_detail",
    [
        (UnprocessableException("Recipe not found"), status.HTTP_422_UNPROCESSABLE_ENTITY, "Recipe not found"),
        (
            UnprocessableException("Recipe already deleted"),
            status.HTTP_422_UNPROCESSABLE_ENTITY,
            "Recipe already deleted",
        ),
        (ServerError("Something exploded"), status.HTTP_500_INTERNAL_SERVER_ERROR, "Something exploded"),
        (ValueError("Some value error"), status.HTTP_400_BAD_REQUEST, "Some value error"),
    ],
)
def test_patch_order_exceptions(
    test_client: TestClient,
    valid_order_patch_request: dict,
    valid_headers: dict,
    mock_partner_service: Mock,
    exception: Exception,
    expected_status: int,
    expected_detail: str,
) -> None:
    mock_order_service = Mock()
    mock_order_service.update_order.side_effect = exception
    order_id = str(uuid.uuid4())

    override_dependencies(mock_partner_service, Mock(), mock_order_service)

    response = test_client.patch(f"/v1/orders/{order_id}", json=valid_order_patch_request, headers=valid_headers)

    assert response.status_code == expected_status
    assert expected_detail in response.json()["error"]
    reset_dependencies()


def test_delete_order_success(
    test_client: TestClient,
    mock_partner_service: Mock,
    mock_order_service: Mock,
    valid_headers: dict,
) -> None:
    order_id = str(uuid.uuid4())
    override_dependencies(mock_partner_service, Mock(), mock_order_service)

    response = test_client.delete(f"/v1/orders/{order_id}", headers=valid_headers)

    assert response.status_code == status.HTTP_204_NO_CONTENT
    mock_partner_service.validate_partner_id.assert_called_once()
    mock_order_service.delete_order.assert_called_once_with(mock_partner_service.partner_id, uuid.UUID(order_id))

    reset_dependencies()


def test_delete_order_access_denied(
    test_client: TestClient,
    mock_order_service: Mock,
    valid_headers: dict,
) -> None:
    mock_partner = Mock()
    mock_partner.validate_partner_id.return_value = False
    mock_partner.partner_id = "partner-123"

    override_dependencies(mock_partner, Mock(), mock_order_service)

    order_id = str(uuid.uuid4())
    response = test_client.delete(f"/v1/orders/{order_id}", headers=valid_headers)

    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert "Failed to find partner" in response.json()["error"]

    reset_dependencies()


def test_delete_order_invalid_uuid_format(test_client: TestClient, valid_headers: dict) -> None:
    override_dependencies(Mock(), Mock(), Mock())

    response = test_client.delete("/v1/orders/not-a-uuid", headers=valid_headers)
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    error_msg = response.json()["error"]
    assert "Uuid_parsing orderId" in error_msg


@pytest.mark.parametrize(
    "exception, expected_status, expected_detail",
    [
        (ServerError("server exploded"), status.HTTP_500_INTERNAL_SERVER_ERROR, "server exploded"),
    ],
)
def test_delete_order_raises_expected_errors(
    test_client: TestClient,
    mock_partner_service: Mock,
    mock_order_service: Mock,
    valid_headers: dict,
    exception: Exception,
    expected_status: int,
    expected_detail: str,
) -> None:
    mock_order_service.delete_order.side_effect = exception
    override_dependencies(mock_partner_service, Mock(), mock_order_service)

    order_id = str(uuid.uuid4())
    response = test_client.delete(f"/v1/orders/{order_id}", headers=valid_headers)

    assert response.status_code == expected_status
    assert expected_detail in response.json()["error"]

    reset_dependencies()
