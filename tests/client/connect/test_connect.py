import json
from unittest.mock import Mock, patch

import pytest
from requests.exceptions import HTTPError, RequestException

from src.clients.connect.client import ConnectClient


def _valid_token_response_json() -> dict[str, object]:
    return {
        "access_token": "new-access",
        "token_type": "Bearer",
        "expires_in": 3600,
        "refresh_token": "new-refresh",
        "scope": "read write",
        "created_at": 1732051200,
        "id_token": "id-token",
    }


def test_refresh_token_success() -> None:
    client = ConnectClient()

    resp = Mock()
    resp.raise_for_status.return_value = None
    resp.json.return_value = _valid_token_response_json()

    with patch.object(client.session, "post", return_value=resp) as mock_post:
        result = client.refresh_token("old-refresh", "client-id", "client-secret")

    expected_headers = {
        "Content-Type": "application/x-www-form-urlencoded",
    }
    expected_form = {
        "grant_type": "refresh_token",
        "refresh_token": "old-refresh",
        "client_id": "client-id",
        "client_secret": "client-secret",
    }

    mock_post.assert_called_once_with(client.token_url, headers=expected_headers, data=expected_form)

    assert result.access_token == "new-access"
    assert result.refresh_token == "new-refresh"
    assert result.token_type == "Bearer"
    assert result.expires_in == 3600
    assert result.scope == "read write"
    assert result.created_at == 1732051200
    assert result.id_token == "id-token"


def test_refresh_token_http_error_raises_server_error() -> None:
    client = ConnectClient()

    resp = Mock()
    resp.raise_for_status.side_effect = HTTPError("boom")

    with patch.object(client.session, "post", return_value=resp):
        with pytest.raises(Exception) as exc:
            client.refresh_token("old-refresh", "client-id", "client-secret")
    assert "Failed to refresh Connect token" in str(exc.value)


def test_refresh_token_request_exception_raises_server_error() -> None:
    client = ConnectClient()

    with patch.object(client.session, "post", side_effect=RequestException("conn")):
        with pytest.raises(Exception) as exc:
            client.refresh_token("old-refresh", "client-id", "client-secret")
    assert "Failed to refresh Connect token" in str(exc.value)


def test_refresh_token_validation_error() -> None:
    client = ConnectClient()

    resp = Mock()
    resp.raise_for_status.return_value = None
    resp.text = json.dumps({"unexpected": "field"})
    resp.json.return_value = {"unexpected": "field"}

    with patch.object(client.session, "post", return_value=resp):
        with pytest.raises(ValueError) as exc:
            client.refresh_token("old-refresh", "client-id", "client-secret")
    assert "Response format not expected" in str(exc.value)
    assert "Response keys: ['unexpected']" in str(exc.value)
