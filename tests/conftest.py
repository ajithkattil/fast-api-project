import base64
import json
from collections.abc import Generator
from datetime import UTC, datetime
from typing import Any
from unittest.mock import MagicMock

import pytest
from fastapi.testclient import TestClient

from src.db.mocks.idempotency_data import MockIdempotencyDB
from src.db.mocks.pantry_data import MockPantryDB
from src.db.mocks.partner_data import MockPartnerDB
from src.dependancies.culops_client import get_culops_client
from src.dependancies.idempotency_db import get_idempotency_db
from src.dependancies.pantry_db import get_pantry_db
from src.dependancies.partner_db import get_partner_db
from src.dependancies.partner_service import get_partner_service
from src.dependancies.token_service import get_token_service
from src.main import app
from src.services.partner import PartnerService
from src.services.token import TokenName, TokenService
from src.token_manager.models import Param


@pytest.fixture
def test_client() -> Generator[TestClient, Any, None]:
    class MockParamStoreClient:
        def get_params(self, names: list[str]) -> list[Param]:
            now = int(datetime.now(UTC).timestamp())
            header = {"alg": "ES512"}
            payload: dict[str, int] = {}
            payload["iat"] = now
            payload["exp"] = now + 60
            header_bytes = json.dumps(header, separators=(",", ":")).encode()
            header_part = base64.urlsafe_b64encode(header_bytes).decode().rstrip("=")
            payload_bytes = json.dumps(payload, separators=(",", ":")).encode()
            payload_part = base64.urlsafe_b64encode(payload_bytes).decode().rstrip("=")
            test_token = f"{header_part}.{payload_part}."
            return [Param(name=TokenName.CUL_OPS_ACCESS_TOKEN.value, value=test_token)]

    # Create mock CulOps client
    from src.utils.generate_pantry_mocks import generate_mock_pantry_items

    # Create minimal mock data for brand test
    mock_items = generate_mock_pantry_items(items_per_pantry=3)
    mock_items[0].brand_name = "samuri pizza cat"  # Only first item has the brand

    def mock_get_partner_culops_pantry_data(available_from=None, available_until=None, partner_id="", brand_name="", page=None, page_size=None):
        if brand_name == "samuri pizza cat":
            return iter([(mock_items, False)])
        else:
            return iter([])

    mock_culops_client = MagicMock()
    mock_culops_client.get_partner_culops_pantry_data.side_effect = mock_get_partner_culops_pantry_data

    app.dependency_overrides[get_partner_db] = lambda: MockPartnerDB()
    app.dependency_overrides[get_pantry_db] = lambda: MockPantryDB()
    app.dependency_overrides[get_idempotency_db] = lambda: MockIdempotencyDB()
    app.dependency_overrides[get_partner_service] = lambda: PartnerService(
        partner_id="BA-MAIN", partner_db=MockPartnerDB()
    )
    app.dependency_overrides[get_token_service] = lambda: TokenService(param_store_client=MockParamStoreClient())
    app.dependency_overrides[get_culops_client] = lambda: mock_culops_client
    with TestClient(app) as c:
        yield c
    app.dependency_overrides = {}


def encode_jwt(payload: dict) -> str:
    header = {"alg": "RS256", "typ": "JWT"}

    def b64u(d: bytes) -> str:
        return base64.urlsafe_b64encode(d).decode().rstrip("=")

    h = b64u(json.dumps(header, separators=(",", ":")).encode())
    p = b64u(json.dumps(payload, separators=(",", ":")).encode())
    s = b64u(b"signature")
    return f"{h}.{p}.{s}"
