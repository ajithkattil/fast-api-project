from unittest.mock import Mock

import pytest

from src.clients.connect.client import ConnectClient
from src.clients.param_store.client import ParamStoreClient
from src.core.config import settings
from src.core.exceptions import ServerError
from src.token_manager.models import Param, TokenResponse
from src.token_manager.service import TokenManagerService


def _token_response() -> TokenResponse:
    return TokenResponse(
        access_token="new-access",
        token_type="Bearer",
        expires_in=3600,
        refresh_token="new-refresh",
        scope="read write",
        created_at=1732051200,
        id_token="id-token",
    )


def _params_with_tokens(access: str = "old-access", refresh: str = "old-refresh") -> list[Param]:
    return [
        Param(name=f"/{settings.DEPLOY_ENV}/{settings.SERVICE_PARAMS_BASE_PATH}/{settings.CUL_OPS_ACCESS_TOKEN_PARAM_NAME}", value=access),
        Param(name=f"/{settings.DEPLOY_ENV}/{settings.SERVICE_PARAMS_BASE_PATH}/{settings.CUL_OPS_REFRESH_TOKEN_PARAM_NAME}", value=refresh),
    ]


def test_refresh_token_success() -> None:
    param_store = Mock(spec=ParamStoreClient)
    connect = Mock(spec=ConnectClient)

    param_store.get_params.return_value = _params_with_tokens()
    connect.refresh_token.return_value = _token_response()

    svc = TokenManagerService(param_store, connect)
    svc.refresh_token()

    connect.refresh_token.assert_called_once_with(
        "old-refresh",
        settings.CONNECT_CLIENT_ID,
        settings.CONNECT_CLIENT_SECRET,
    )

    calls = param_store.store_param.call_args_list
    assert len(calls) == 2
    first_param = calls[0].args[0]
    second_param = calls[1].args[0]
    assert first_param.name == f"/{settings.DEPLOY_ENV}/{settings.SERVICE_PARAMS_BASE_PATH}/{settings.CUL_OPS_ACCESS_TOKEN_PARAM_NAME}"
    assert first_param.value == "new-access"
    assert second_param.name == f"/{settings.DEPLOY_ENV}/{settings.SERVICE_PARAMS_BASE_PATH}/{settings.CUL_OPS_REFRESH_TOKEN_PARAM_NAME}"
    assert second_param.value == "new-refresh"


def test_refresh_token_get_params_server_error() -> None:
    param_store = Mock(spec=ParamStoreClient)
    connect = Mock(spec=ConnectClient)
    param_store.get_params.side_effect = ServerError("down")

    svc = TokenManagerService(param_store, connect)
    with pytest.raises(ServerError) as exc:
        svc.refresh_token()
    msg = str(exc.value)
    assert "Failed to get CulOps token parameters" in msg
    assert settings.CUL_OPS_ACCESS_TOKEN_PARAM_NAME in msg
    assert settings.CUL_OPS_REFRESH_TOKEN_PARAM_NAME in msg


def test_refresh_token_get_params_value_error_wrapped() -> None:
    param_store = Mock(spec=ParamStoreClient)
    connect = Mock(spec=ConnectClient)
    param_store.get_params.side_effect = ValueError("bad")

    svc = TokenManagerService(param_store, connect)
    with pytest.raises(ServerError) as exc:
        svc.refresh_token()
    assert "Missing or invalid CulOps token parameters" in str(exc.value)


def test_refresh_token_missing_tokens_in_params() -> None:
    param_store = Mock(spec=ParamStoreClient)
    connect = Mock(spec=ConnectClient)
    param_store.get_params.return_value = [
        Param(name=settings.CUL_OPS_ACCESS_TOKEN_PARAM_NAME, value="only-access"),
    ]

    svc = TokenManagerService(param_store, connect)
    with pytest.raises(ServerError) as exc:
        svc.refresh_token()
    assert "Missing or invalid CulOps tokens" in str(exc.value)


@pytest.mark.parametrize("exc_cls", [ServerError, ValueError])
def test_refresh_token_connect_client_errors_wrapped(exc_cls: type[Exception]) -> None:
    param_store = Mock(spec=ParamStoreClient)
    connect = Mock(spec=ConnectClient)
    param_store.get_params.return_value = _params_with_tokens()
    connect.refresh_token.side_effect = exc_cls("boom")

    svc = TokenManagerService(param_store, connect)
    with pytest.raises(ServerError) as exc:
        svc.refresh_token()
    assert "Failed to refresh CulOps token" in str(exc.value)


def test_refresh_token_store_param_server_error_wrapped() -> None:
    param_store = Mock(spec=ParamStoreClient)
    connect = Mock(spec=ConnectClient)
    param_store.get_params.return_value = _params_with_tokens()
    connect.refresh_token.return_value = _token_response()
    param_store.store_param.side_effect = ServerError("ssm")

    svc = TokenManagerService(param_store, connect)
    with pytest.raises(ServerError) as exc:
        svc.refresh_token()
    msg = str(exc.value)
    assert "Failed to store CulOps token parameters" in msg
    assert settings.CUL_OPS_ACCESS_TOKEN_PARAM_NAME in msg
    assert settings.CUL_OPS_REFRESH_TOKEN_PARAM_NAME in msg
