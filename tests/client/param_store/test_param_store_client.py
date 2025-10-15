from unittest.mock import patch

import boto3
import pytest
from botocore.client import BaseClient
from botocore.config import Config
from botocore.stub import Stubber

from src.clients.param_store.client import ParamStoreClient
from src.core.config import settings
from src.core.exceptions import ServerError
from src.token_manager.models import Param


@pytest.fixture(autouse=True)
def ssm_client() -> BaseClient:
    config = Config(
        region_name=settings.AWS_REGION,
    )
    return boto3.client("ssm", config=config)


def test_get_params_success(ssm_client: BaseClient) -> None:
    stubber = Stubber(ssm_client)

    expected_params = {"Names": ["/app/DB_URL", "/app/DB_USER"], "WithDecryption": True}
    response = {
        "Parameters": [
            {"Name": "/app/DB_URL", "Value": "postgres://host/db"},
            {"Name": "/app/DB_USER", "Value": "svc-user"},
        ]
    }

    stubber.add_response("get_parameters", response, expected_params)

    client = ParamStoreClient()
    with patch.object(client, "_client", ssm_client):
        with stubber:
            result = client.get_params(["/app/DB_URL", "/app/DB_USER"])

    assert isinstance(result, list)
    assert len(result) == 2
    assert result[0].name == "/app/DB_URL"
    assert result[0].value == "postgres://host/db"
    assert result[1].name == "/app/DB_USER"
    assert result[1].value == "svc-user"


def test_get_params_empty_names_returns_empty(ssm_client: BaseClient) -> None:
    client = ParamStoreClient()
    with patch.object(client, "_client", ssm_client):
        res = client.get_params([])

    assert res == []


def test_get_params_with_invalid_names_raises_value_error(ssm_client: BaseClient) -> None:
    stubber = Stubber(ssm_client)

    expected_params = {"Names": ["/app/SECRET"], "WithDecryption": True}
    response = {"Parameters": [], "InvalidParameters": ["/app/SECRET"]}

    stubber.add_response("get_parameters", response, expected_params)

    client = ParamStoreClient()
    with patch.object(client, "_client", ssm_client):
        with stubber:
            with pytest.raises(ValueError) as exc:
                client.get_params(["/app/SECRET"])

    assert "Invalid parameter names in request" in str(exc.value)
    assert "/app/SECRET" in str(exc.value)


def test_get_params_boto_client_error_raises_server_error(ssm_client: BaseClient) -> None:
    stubber = Stubber(ssm_client)

    expected_params = {"Names": ["/app/DB_URL"], "WithDecryption": True}

    stubber.add_client_error(
        method="get_parameters",
        service_error_code="AccessDeniedException",
        service_message="Access Denied",
        http_status_code=400,
        expected_params=expected_params,
    )

    client = ParamStoreClient()
    with patch.object(client, "_client", ssm_client):
        with stubber:
            with pytest.raises(ServerError) as exc:
                client.get_params(["/app/DB_URL"])

    assert "Failed to get parameters from Parameter Store" in str(exc.value)


def test_get_params_missing_requested_param_raises_value_error(ssm_client: BaseClient) -> None:
    stubber = Stubber(ssm_client)

    expected_params = {"Names": ["/app/DB_URL", "/app/DB_USER"], "WithDecryption": True}
    response = {
        "Parameters": [
            {"Name": "/app/DB_URL", "Value": "postgres://host/db"},
        ]
    }

    stubber.add_response("get_parameters", response, expected_params)

    client = ParamStoreClient()
    with patch.object(client, "_client", ssm_client):
        with stubber:
            with pytest.raises(ValueError) as exc:
                client.get_params(["/app/DB_URL", "/app/DB_USER"])

    assert "Parameter /app/DB_USER not found in response" in str(exc.value)


def test_store_param_success(ssm_client: BaseClient) -> None:
    stubber = Stubber(ssm_client)

    param = Param(name="/app/NEW_PARAM", value="secret-value")

    expected_params = {
        "Name": "/app/NEW_PARAM",
        "Value": "secret-value",
        "Overwrite": True,
    }
    response = {"Version": 1}

    stubber.add_response("put_parameter", response, expected_params)

    client = ParamStoreClient()
    with patch.object(client, "_client", ssm_client):
        with stubber:
            client.store_param(param)


def test_store_param_boto_client_error_raises_server_error(ssm_client: BaseClient) -> None:
    stubber = Stubber(ssm_client)

    param = Param(name="/app/NEW_PARAM", value="secret-value")

    expected_params = {
        "Name": "/app/NEW_PARAM",
        "Value": "secret-value",
        "Overwrite": True,
    }

    stubber.add_client_error(
        method="put_parameter",
        service_error_code="AccessDeniedException",
        service_message="Access Denied",
        http_status_code=400,
        expected_params=expected_params,
    )

    client = ParamStoreClient()
    with patch.object(client, "_client", ssm_client):
        with stubber:
            with pytest.raises(ServerError) as exc:
                client.store_param(param)

    assert f"Failed to store parameter {param.name} in Parameter Store" in str(exc.value)
