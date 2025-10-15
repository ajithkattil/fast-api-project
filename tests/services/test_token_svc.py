import base64
import json
from datetime import UTC, datetime
from unittest.mock import MagicMock, patch

import pytest

from src.core.config import settings
from src.services.token import TokenName, TokenService
from src.token_manager.models import Param


@pytest.fixture(autouse=True)
def reset_token_service_singleton() -> None:
    TokenService._instance = None


def _b64url(data: bytes) -> str:
    return base64.urlsafe_b64encode(data).decode().rstrip("=")


def _unsigned_token_with_exp_in(seconds_from_now: int, include_exp: bool = True, include_iat: bool = True) -> str:
    now = int(datetime.now(UTC).timestamp())
    header = {"alg": "ES512"}
    payload: dict[str, int] = {}
    if include_iat:
        payload["iat"] = now
    if include_exp:
        payload["exp"] = now + seconds_from_now
    header_part = _b64url(json.dumps(header, separators=(",", ":")).encode())
    payload_part = _b64url(json.dumps(payload, separators=(",", ":")).encode())
    return f"{header_part}.{payload_part}."


def test_get_token_returns_cached_valid_token() -> None:
    token_name = TokenName.CUL_OPS_ACCESS_TOKEN
    mock_param_store: MagicMock = MagicMock()
    token_svc = TokenService(param_store_client=mock_param_store)
    cached_token = _unsigned_token_with_exp_in(settings.TOKEN_EXPIRY_BUFFER + 60)
    token_svc._token_cache[token_name] = cached_token

    result = token_svc.get_token(token_name)

    assert result == cached_token
    mock_param_store.get_params.assert_not_called()


def test_get_token_fetches_when_cache_missing() -> None:
    token_name = TokenName.CUL_OPS_ACCESS_TOKEN
    mock_param_store: MagicMock = MagicMock()
    token_svc = TokenService(param_store_client=mock_param_store)
    fetched_token = _unsigned_token_with_exp_in(settings.TOKEN_EXPIRY_BUFFER + 60)
    
    # Mock SSM response
    mock_param_store.get_params.return_value = [Param(name="test", value=fetched_token)]
    
    result = token_svc.get_token(token_name)

    assert result == fetched_token
    assert token_svc._token_cache[token_name] == fetched_token
    mock_param_store.get_params.assert_called_once()


def test_get_token_fetches_when_cached_token_near_expiry() -> None:
    token_name = TokenName.CUL_OPS_ACCESS_TOKEN
    mock_param_store: MagicMock = MagicMock()
    token_svc = TokenService(param_store_client=mock_param_store)
    near_exp = _unsigned_token_with_exp_in(settings.TOKEN_EXPIRY_BUFFER - 1)
    fresh = _unsigned_token_with_exp_in(settings.TOKEN_EXPIRY_BUFFER + 60)
    token_svc._token_cache[token_name] = near_exp
    
    # Mock SSM response
    mock_param_store.get_params.return_value = [Param(name="test", value=fresh)]

    result = token_svc.get_token(token_name)

    assert result == fresh
    assert token_svc._token_cache[token_name] == fresh


def test_get_token_fetches_when_cached_token_invalid() -> None:
    token_name = TokenName.CUL_OPS_ACCESS_TOKEN
    mock_param_store: MagicMock = MagicMock()
    token_svc = TokenService(param_store_client=mock_param_store)
    invalid = _unsigned_token_with_exp_in(settings.TOKEN_EXPIRY_BUFFER + 60, include_exp=False, include_iat=True)
    fresh = _unsigned_token_with_exp_in(settings.TOKEN_EXPIRY_BUFFER + 60)
    token_svc._token_cache[token_name] = invalid
    
    # Mock SSM response
    mock_param_store.get_params.return_value = [Param(name="test", value=fresh)]

    result = token_svc.get_token(token_name)

    assert result == fresh
    assert token_svc._token_cache[token_name] == fresh


def test_get_token_falls_back_to_env_var_when_ssm_fails() -> None:
    token_name = TokenName.CUL_OPS_ACCESS_TOKEN
    mock_param_store: MagicMock = MagicMock()
    token_svc = TokenService(param_store_client=mock_param_store)
    token_svc._token_cache.clear()
    fallback_token = _unsigned_token_with_exp_in(settings.TOKEN_EXPIRY_BUFFER + 60)
    from src.core.exceptions import ServerError

    # Mock SSM failure but env var exists
    mock_param_store.get_params.side_effect = ServerError("SSM failed")
    with patch("os.getenv", return_value=fallback_token):
        result = token_svc.get_token(token_name)

    assert result == fallback_token
    assert token_svc._token_cache[token_name] == fallback_token


def test_get_token_fetch_failure_raises_server_error() -> None:
    token_name = TokenName.CUL_OPS_ACCESS_TOKEN
    mock_param_store: MagicMock = MagicMock()
    token_svc = TokenService(param_store_client=mock_param_store)
    token_svc._token_cache.clear()
    from src.core.exceptions import ServerError

    # Mock SSM failure and no env var fallback
    mock_param_store.get_params.side_effect = ServerError("SSM failed")
    with patch("os.getenv", return_value=None):
        with pytest.raises(ServerError):
            token_svc.get_token(token_name)


def test_get_token_fetches_when_cached_token_expired() -> None:
    """Test that an expired token triggers a fetch from SSM."""
    token_name = TokenName.CUL_OPS_ACCESS_TOKEN
    mock_param_store: MagicMock = MagicMock()
    token_svc = TokenService(param_store_client=mock_param_store)

    # Create an expired token (expired 10 seconds ago)
    expired_token = _unsigned_token_with_exp_in(-10)
    # Create a fresh token
    fresh_token = _unsigned_token_with_exp_in(settings.TOKEN_EXPIRY_BUFFER + 60)

    # Cache the expired token
    token_svc._token_cache[token_name] = expired_token

    # Mock SSM to return fresh token
    mock_param_store.get_params.return_value = [Param(name="test", value=fresh_token)]

    # Get token should detect expiry and fetch fresh one
    result = token_svc.get_token(token_name)

    assert result == fresh_token
    assert token_svc._token_cache[token_name] == fresh_token
    mock_param_store.get_params.assert_called_once()
