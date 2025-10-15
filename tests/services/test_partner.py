from unittest.mock import MagicMock

import pytest

from src.services.models.partner import CostMarkup, Partner
from src.services.partner import PartnerService
from src.utils.datetime_helper import parse_to_datetime


@pytest.fixture
def mock_partner_db() -> MagicMock:
    return MagicMock()


@pytest.fixture
def service(mock_partner_db: MagicMock) -> PartnerService:
    return PartnerService(partner_id="partner_123", partner_db=mock_partner_db)


def test_validate_partner_id_valid(service: PartnerService, mock_partner_db: MagicMock) -> None:
    mock_partner_db.find_partner_id.return_value = {"id": "partner_123"}
    assert service.validate_partner_id() is True


def test_validate_partner_id_invalid(service: PartnerService, mock_partner_db: MagicMock) -> None:
    mock_partner_db.find_partner_id.return_value = None
    assert service.validate_partner_id() is False


def test_get_partner_by_id(service: PartnerService, mock_partner_db: MagicMock) -> None:
    expected_partner = Partner(name="partner_123", recipe_create_cutoff_days=1)
    mock_partner_db.get_partner_by_id.return_value = expected_partner
    result = service.get_partner()
    assert result == expected_partner


def test_get_partner_cost_markups(service: PartnerService, mock_partner_db: MagicMock) -> None:
    markups = [
        CostMarkup(
            applied_from=parse_to_datetime("2025-1-1"),
            applied_until=parse_to_datetime("2025-5-30"),
            markup_percent=5,
        )
    ]
    mock_partner_db.get_partner_cost_markups.return_value = markups
    result = service.get_partner_cost_markups()
    assert result == markups


def test_get_partner_assembly_packaging_options(service: PartnerService, mock_partner_db: MagicMock) -> None:
    options = ["box", "bag"]
    mock_partner_db.get_partner_assembly_packaging_options.return_value = options
    result = service.get_partner_assembly_packaging_options()
    assert result == options


def test_get_partner_cost_markups_returns_empty_list(service: PartnerService, mock_partner_db: MagicMock) -> None:
    mock_partner_db.get_partner_cost_markups.return_value = []
    assert service.get_partner_cost_markups() == []


def test_validate_partner_id_valid_calls_db(service: PartnerService, mock_partner_db: MagicMock) -> None:
    mock_partner_db.find_partner_id.return_value = {"id": "partner_123"}
    service.validate_partner_id()
    mock_partner_db.find_partner_id.assert_called_once_with(partner_id="partner_123")
