from datetime import datetime
from unittest.mock import Mock, patch

import pytest
from requests import HTTPError, RequestException

from src.clients.cabinet.cabinet import CabinetService
from src.core.exceptions import ServerError
from src.services.models.recipe import RecipeSlotCode
from src.utils.datetime_helper import parse_to_datetime


@pytest.fixture
def cabinet_service() -> CabinetService:
    return CabinetService()


@pytest.mark.parametrize("filter_date", ["2025-06-01", None])
def test_get_recipe_slots_data_valid(cabinet_service: CabinetService, filter_date: str | None) -> None:
    mock_response = Mock()
    mock_response.status_code = 200
    mock_response.json.return_value = {
        "data": [
            {
                "id": "WC09",
                "type": "recipe-slots",
                "attributes": {
                    "culinary-code": "WC09",
                    "meal-type": "WildCard09",
                    "activates-at": "2025-06-01T00:00:00Z",
                    "deactivates-at": None,
                    "plan-id": 10,
                    "plan-name": "Wild Card plan",
                    "plan-description": "Wild Card",
                    "short-code": "WC09",
                    "color-code": "f2be20",
                    "sort-order": 5106,
                    "presentation-sort-order": 5106,
                },
                "links": {"self": "https://cabinet.staging.f--r.co/recipe-slots/WC09"},
            }
        ]
    }

    with patch.object(cabinet_service.session, "get", return_value=mock_response):
        results = cabinet_service.get_recipe_slots(
            filter_date=parse_to_datetime(filter_date) if filter_date else None,
        )

    assert len(results) == 1
    assert isinstance(results[0], RecipeSlotCode)
    assert results[0].slot_code == "WC09"
    assert results[0].plan_id == 10
    assert results[0]._plan_description == "Wild Card"


@pytest.mark.parametrize("filter_date", ["2020-06-01", "2030-06-01"])
def test_get_recipe_slots_invalid_date(cabinet_service: CabinetService, filter_date: str) -> None:
    mock_response = Mock()
    mock_response.status_code = 500
    mock_response.text = "Internal Server Error"

    with patch.object(cabinet_service.session, "get", return_value=mock_response):
        with pytest.raises(ServerError):
            cabinet_service.get_recipe_slots(
                filter_date=parse_to_datetime(filter_date),
            )


def test_missing_bearer_token(cabinet_service: CabinetService) -> None:
    with patch.object(cabinet_service.session, "get", side_effect=Exception("Missing bearer token")):
        with pytest.raises(RuntimeError, match="Missing bearer token"):
            cabinet_service.get_recipe_slots(
                filter_date=parse_to_datetime("2025-06-01"),
            )


def test_find_cycle_success(cabinet_service: CabinetService) -> None:
    cycle_date = datetime.strptime("2025-07-07", "%Y-%m-%d")
    mock_response = Mock()
    mock_response.status_code = 200
    mock_response.json.return_value = {
        "data": [
            {
                "id": "1",
                "type": "cycles",
                "attributes": {
                    "date": "2025-07-07",
                    "is-active": True,
                },
            }
        ]
    }

    with patch.object(cabinet_service.session, "get", return_value=mock_response):
        result = cabinet_service.find_cycle(cycle_date)
        assert result is True


def test_find_cycle_request_exception(cabinet_service: CabinetService) -> None:
    cycle_date = datetime.strptime("2025-07-07", "%Y-%m-%d")
    with patch.object(cabinet_service.session, "get", side_effect=RequestException("network error")):
        with pytest.raises(ServerError):
            cabinet_service.find_cycle(cycle_date)


def test_find_cycle_http_error(cabinet_service: CabinetService) -> None:
    cycle_date = datetime.strptime("2025-07-07", "%Y-%m-%d")
    mock_response = Mock()
    mock_response.raise_for_status.side_effect = HTTPError("bad request")
    with patch.object(cabinet_service.session, "get", return_value=mock_response):
        with pytest.raises(ServerError):
            cabinet_service.find_cycle(cycle_date)


def test_find_cycle_validation_error(cabinet_service: CabinetService) -> None:
    cycle_date = datetime.strptime("2025-07-07", "%Y-%m-%d")
    mock_response = Mock()
    mock_response.status_code = 200
    mock_response.raise_for_status.return_value = None
    mock_response.json.return_value = {"invalid": "shape"}
    with patch.object(cabinet_service.session, "get", return_value=mock_response):
        with pytest.raises(ServerError):
            cabinet_service.find_cycle(cycle_date)
