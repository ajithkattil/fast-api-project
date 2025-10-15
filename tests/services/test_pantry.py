import base64
import json
from datetime import UTC, datetime
from typing import Any
from unittest.mock import MagicMock, patch
from uuid import UUID

import pytest

from src.api.routes.v1.models import (
    PantryItemAvailability as ResponsePantryItemAvailability,
)
from src.clients.culops.culops import CulOpsService
from src.core.exceptions import ServerError
from src.db.mocks.pantry_data import MockPantryDB
from src.db.mocks.partner_data import MockPartnerDB
from src.interfaces.pantry_db_interface import PantryDBInterface
from src.interfaces.partner_repo_interface import PartnerRepoInterface
from src.services.models.pantry import (
    Pantry,
    PantryItem,
    PantryItemAvailability,
    PantryItemCost,
    PartnerCostMarkup,
)
from src.services.pantry import PantryService
from src.services.partner import PartnerService
from src.utils.datetime_helper import parse_to_datetime
from src.utils.generate_pantry_mocks import generate_mock_pantry_items


@pytest.fixture
def pantry_data() -> Pantry:
    available_from = parse_to_datetime("2025-01-01")
    available_until = parse_to_datetime("2025-04-11")
    return Pantry(
        pantry_items=generate_mock_pantry_items(
            items_per_pantry=500,
            seed=5,
            available_from=available_from,
            available_until=available_until,
        ),
        pantry_state_id="12345",
        partner_id="123",
        pantry_state_timestamp=datetime.now(),
        ingredients_available_from=available_from,
        ingredients_available_until=available_until,
        partner_cost_markup=[],
    )


@pytest.fixture
def pantry_db_mock() -> PantryDBInterface:
    return MockPantryDB()


@pytest.fixture
def culops_service() -> CulOpsService:
    mock_partner_repo = MagicMock()
    mock_recipe_repo = MagicMock()
    mock_pantry_repo = MagicMock()
    mock_token_svc = MagicMock()

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

    mock_token_svc.get_token.return_value = test_token

    return CulOpsService(
        partner_repo=mock_partner_repo,
        recipe_repo=mock_recipe_repo,
        pantry_repo=mock_pantry_repo,
        token_svc=mock_token_svc,
    )


@pytest.fixture
def partner_db() -> PartnerRepoInterface:
    return MockPartnerDB()


@pytest.fixture
def partner_service(partner_db: PartnerRepoInterface) -> PartnerService:
    return PartnerService("123", partner_db)


@pytest.fixture
def pantry_service(
    pantry_db_mock: MockPantryDB,
    culops_service: CulOpsService,
    partner_service: PartnerService,
) -> PantryService:
    pantry_service = PantryService(
        pantry_db=pantry_db_mock, culops_service=culops_service, partner_service=partner_service
    )
    return pantry_service


def test_get_pantry_valid_input(pantry_service: PantryService, pantry_data: Pantry) -> None:
    page_size = 2

    res = pantry_service.get_pantry(
        available_from=None, available_until=None, pantry_state_id="12345", partner_id="123", page_size=page_size
    )

    assert res is not None, "Pantry should not be None"
    pantry, _ = res

    returned_ids = [item.id for item in (pantry.pantry_items[:page_size])]
    expected_ids = [item.id for item in pantry_data.pantry_items[:page_size]]

    assert returned_ids == expected_ids


def test_get_pantry_availability_from(
    pantry_service: PantryService,
) -> None:
    available_from = "2025-03-05"

    with patch("src.services.pantry.uuid4", return_value="12345"):
        pantry, _ = pantry_service.get_pantry(available_from=available_from, partner_id="123")

    pantry_items = pantry.pantry_items
    for item in pantry_items:
        assert all(isinstance(item, ResponsePantryItemAvailability) for item in item.availability)
        if not item.availability:
            continue
        assert any(
            period.start_date and parse_to_datetime(period.start_date) <= parse_to_datetime(available_from)
            for period in item.availability
        )


def test_get_pantry_availability_until(
    pantry_service: PantryService,
) -> None:
    available_until = "2025-02-01"

    with patch("src.services.pantry.uuid4", return_value="103050"):
        pantry, _ = pantry_service.get_pantry(available_from=None, available_until=available_until, partner_id="123")

    pantry_items = pantry.pantry_items

    for item in pantry_items:
        assert all(isinstance(avail, ResponsePantryItemAvailability) for avail in item.availability)
        if not item.availability:
            continue
        assert any(
            period.end_date and period.end_date <= available_until if period.end_date else True
            for period in item.availability
        )


def test_get_pantry_returns_same_items_for_pantry_state_id_query(
    pantry_service: PantryService,
) -> None:
    res: tuple[Pantry, int] = pantry_service.get_pantry(
        available_from=None, available_until=None, pantry_state_id="12345", partner_id="123"
    )

    assert res is not None, "Pantry should not be None"
    pantry, _ = res

    returned_ids = [item.id for item in pantry.pantry_items]

    pantry_2, _ = pantry_service.get_pantry(
        available_from=None, available_until=None, pantry_state_id="12345", partner_id="123"
    )
    expected_ids = [item.id for item in pantry_2.pantry_items]

    assert pantry.pantry_state_id == pantry_2.pantry_state_id
    assert returned_ids == expected_ids


def test_get_pantry_missing_partner_id_raises() -> None:
    mock_pantry_db = MagicMock()
    mock_culops = MagicMock()
    mock_partner_svc = MagicMock()
    svc = PantryService(mock_pantry_db, mock_culops, mock_partner_svc)

    with pytest.raises(ValueError, match="Missing partner id"):
        svc.get_pantry(partner_id="")


def test_get_pantry_save_state_failure_raises_no_delete() -> None:
    from uuid import UUID

    mock_pantry_db = MagicMock()
    mock_culops = MagicMock()
    mock_partner_svc = MagicMock()

    mock_pantry_db.save_pantry_state.side_effect = ServerError("save state failed")

    svc = PantryService(mock_pantry_db, mock_culops, mock_partner_svc)

    with patch("src.services.pantry.uuid4", return_value=UUID("00000000-0000-0000-0000-000000000001")):
        with pytest.raises(ServerError, match="Failed to get pantry for partner"):
            svc.get_pantry(partner_id="123")

    mock_pantry_db.delete_pantry.assert_not_called()


def test_get_pantry_save_items_failure_deletes_and_raises() -> None:
    mock_pantry_db = MagicMock()
    mock_culops = MagicMock()
    mock_partner_svc = MagicMock()

    mock_partner_svc.get_partner_cost_markups.return_value = []

    items_page = generate_mock_pantry_items(items_per_pantry=2)

    def gen() -> Any:
        yield items_page

    mock_culops.get_partner_culops_pantry_data.side_effect = lambda **_: gen()
    mock_pantry_db.save_pantry_items.side_effect = ServerError("save items failed")

    svc = PantryService(mock_pantry_db, mock_culops, mock_partner_svc)

    mock_uuid = UUID("00000000-0000-0000-0000-000000000002")
    with patch("src.services.pantry.uuid4", return_value=mock_uuid):
        with pytest.raises(ServerError, match="Failed to get pantry for partner 123"):
            svc.get_pantry(partner_id="123")

    mock_pantry_db.delete_pantry.assert_called_once_with(mock_uuid)


def test_get_pantry_generator_failure_deletes_and_raises() -> None:
    mock_pantry_db = MagicMock()
    mock_culops = MagicMock()
    mock_partner_svc = MagicMock()

    mock_partner_svc.get_partner_cost_markups.return_value = []

    def failing_gen() -> Any:
        if False:
            yield []
        raise ServerError("fetch failed")

    mock_culops.get_partner_culops_pantry_data.side_effect = lambda **_: failing_gen()

    svc = PantryService(mock_pantry_db, mock_culops, mock_partner_svc)

    fixed_id = UUID("00000000-0000-0000-0000-000000000003")
    with patch("src.services.pantry.uuid4", return_value=fixed_id):
        with pytest.raises(ServerError, match="Failed to get pantry for partner 123"):
            svc.get_pantry(partner_id="123")

    mock_pantry_db.delete_pantry.assert_called_once_with(fixed_id)


def test_get_pantry_no_pantry_found_raises() -> None:
    mock_pantry_db = MagicMock()
    mock_culops = MagicMock()
    mock_partner_svc = MagicMock()

    mock_partner_svc.get_partner_cost_markups.return_value = []
    mock_pantry_db.get_partner_pantry_by_id.return_value = (None, 0)

    items_page = generate_mock_pantry_items(items_per_pantry=1)

    def gen() -> Any:
        yield items_page

    mock_culops.get_partner_culops_pantry_data.side_effect = lambda **_: gen()

    svc = PantryService(mock_pantry_db, mock_culops, mock_partner_svc)

    fixed_id = UUID("00000000-0000-0000-0000-000000000004")
    with patch("src.services.pantry.uuid4", return_value=fixed_id):
        with pytest.raises(ValueError, match="No pantry data found"):
            svc.get_pantry(partner_id="123")


def test_calculate_cost_ranges(
    pantry_service: PantryService,
) -> None:
    # Setup Pantry
    availabilities = [
        PantryItemAvailability(
            available_from=parse_to_datetime("2025-01-01"), available_until=parse_to_datetime("2025-05-30")
        ),
        PantryItemAvailability(
            available_from=parse_to_datetime("2025-08-01"), available_until=parse_to_datetime("2025-12-30")
        ),
    ]

    costs = [
        PantryItemCost(
            start_date=parse_to_datetime("2025-01-01"),
            end_date=parse_to_datetime("2025-03-30"),
            production_cost_us_dollars=10.00,
        ),
        PantryItemCost(
            start_date=parse_to_datetime("2025-04-01"),
            end_date=parse_to_datetime("2025-06-30"),
            production_cost_us_dollars=10.25,
        ),
        PantryItemCost(
            start_date=parse_to_datetime("2025-07-01"),
            end_date=parse_to_datetime("2025-09-30"),
            production_cost_us_dollars=10.50,
        ),
        PantryItemCost(
            start_date=parse_to_datetime("2025-10-01"),
            end_date=parse_to_datetime("2025-12-30"),
            production_cost_us_dollars=10.30,
        ),
    ]

    pantry_item = PantryItem(
        availability=availabilities,
        id="1234567890",
        description="test cost calculation",
        cost=costs,
        units="any",
        amount=1,
        is_prepped_and_ready=False,
        custom_fields=[],
    )

    partner_markup = [
        PartnerCostMarkup(
            applied_from=parse_to_datetime("2025-01-01"),
            applied_until=parse_to_datetime("2025-02-28"),
            markup_percent=5,
        ),
        PartnerCostMarkup(
            applied_from=parse_to_datetime("2025-03-01"),
            applied_until=parse_to_datetime("2025-10-30"),
            markup_percent=5.5,
        ),
        PartnerCostMarkup(
            applied_from=parse_to_datetime("2025-11-01"),
            applied_until=parse_to_datetime("2025-12-30"),
            markup_percent=7,
        ),
    ]

    # retrieve results and test against manually calculated dates and numbers
    result = pantry_service.get_partner_cost(pantry_item, partner_markup)

    expected = [
        PantryItemCost(
            start_date=parse_to_datetime("2025-01-01"),
            end_date=parse_to_datetime("2025-02-28"),
            production_cost_us_dollars=10.5,
        ),
        PantryItemCost(
            start_date=parse_to_datetime("2025-03-01"),
            end_date=parse_to_datetime("2025-03-30"),
            production_cost_us_dollars=10.55,
        ),
        PantryItemCost(
            start_date=parse_to_datetime("2025-04-01"),
            end_date=parse_to_datetime("2025-05-30"),
            production_cost_us_dollars=10.81,
        ),
        PantryItemCost(
            start_date=parse_to_datetime("2025-08-01"),
            end_date=parse_to_datetime("2025-09-30"),
            production_cost_us_dollars=11.08,
        ),
        PantryItemCost(
            start_date=parse_to_datetime("2025-10-01"),
            end_date=parse_to_datetime("2025-10-30"),
            production_cost_us_dollars=10.87,
        ),
        PantryItemCost(
            start_date=parse_to_datetime("2025-11-01"),
            end_date=parse_to_datetime("2025-12-30"),
            production_cost_us_dollars=11.02,
        ),
    ]

    assert result == expected


def test_availability_missing_end_date(pantry_service: PantryService) -> None:
    availabilities = [PantryItemAvailability(available_from=parse_to_datetime("2025-01-01"), available_until=None)]

    costs = [
        PantryItemCost(
            start_date=parse_to_datetime("2025-01-01"),
            end_date=parse_to_datetime("2025-02-28"),
            production_cost_us_dollars=12.00,
        )
    ]

    pantry_item = PantryItem(
        availability=availabilities,
        id="1111111111",
        description="test availability open-ended ranges",
        cost=costs,
        units="box",
        amount=1,
        is_prepped_and_ready=False,
        custom_fields=[],
    )

    partner_markup = [
        PartnerCostMarkup(
            applied_from=parse_to_datetime("2025-01-01"),
            applied_until=None,
            markup_percent=1,
        )
    ]

    result = pantry_service.get_partner_cost(pantry_item, partner_markup)

    expected = [
        PantryItemCost(
            start_date=parse_to_datetime("2025-01-01"),
            end_date=parse_to_datetime("2025-02-28"),
            production_cost_us_dollars=12.12,
        ),
    ]

    assert result == expected


def test_cost_missing_end_date(pantry_service: PantryService) -> None:
    availabilities = [
        PantryItemAvailability(
            available_from=parse_to_datetime("2025-01-01"), available_until=parse_to_datetime("2025-05-30")
        )
    ]

    costs = [
        PantryItemCost(start_date=parse_to_datetime("2025-01-01"), end_date=None, production_cost_us_dollars=12.00)
    ]

    pantry_item = PantryItem(
        availability=availabilities,
        id="2222222222",
        description="test cost open-ended range",
        cost=costs,
        units="box",
        amount=1,
        is_prepped_and_ready=False,
        custom_fields=[],
    )

    partner_markup = [
        PartnerCostMarkup(
            applied_from=parse_to_datetime("2025-01-01"),
            applied_until=parse_to_datetime("2025-02-28"),
            markup_percent=10,
        )
    ]

    result = pantry_service.get_partner_cost(pantry_item, partner_markup)

    expected = [
        PantryItemCost(
            start_date=parse_to_datetime("2025-01-01"),
            end_date=parse_to_datetime("2025-02-28"),
            production_cost_us_dollars=13.20,
        ),
    ]

    assert result == expected


def test_markup_missing_end_date(pantry_service: PantryService) -> None:
    availabilities = [
        PantryItemAvailability(
            available_from=parse_to_datetime("2025-01-01"), available_until=parse_to_datetime("2025-05-30")
        )
    ]

    costs = [
        PantryItemCost(
            start_date=parse_to_datetime("2025-01-01"),
            end_date=parse_to_datetime("2025-03-31"),
            production_cost_us_dollars=12.00,
        ),
        PantryItemCost(
            start_date=parse_to_datetime("2025-04-01"),
            end_date=parse_to_datetime("2025-06-30"),
            production_cost_us_dollars=12.50,
        ),
    ]

    pantry_item = PantryItem(
        availability=availabilities,
        id="3333333333",
        description="test markup open-ended range",
        cost=costs,
        units="box",
        amount=1,
        is_prepped_and_ready=False,
        custom_fields=[],
    )

    partner_markup = [
        PartnerCostMarkup(applied_from=parse_to_datetime("2025-01-01"), applied_until=None, markup_percent=10)
    ]

    result = pantry_service.get_partner_cost(pantry_item, partner_markup)

    expected = [
        PantryItemCost(
            start_date=parse_to_datetime("2025-01-01"),
            end_date=parse_to_datetime("2025-03-31"),
            production_cost_us_dollars=13.20,
        ),
        PantryItemCost(
            start_date=parse_to_datetime("2025-04-01"),
            end_date=parse_to_datetime("2025-05-30"),
            production_cost_us_dollars=13.75,
        ),
    ]

    assert result == expected


def test_missing_start_dates(pantry_service: PantryService) -> None:
    availabilities = [PantryItemAvailability(available_from=None, available_until=parse_to_datetime("2025-05-30"))]

    costs = [
        PantryItemCost(start_date=None, end_date=parse_to_datetime("2025-03-31"), production_cost_us_dollars=8.00),
        PantryItemCost(
            start_date=parse_to_datetime("2025-04-01"),
            end_date=parse_to_datetime("2025-06-30"),
            production_cost_us_dollars=9.50,
        ),
    ]

    pantry_item = PantryItem(
        availability=availabilities,
        id="4444444444",
        description="test markup open-start range",
        cost=costs,
        units="barrel",
        amount=1,
        is_prepped_and_ready=False,
        custom_fields=[],
    )

    partner_markups = [PartnerCostMarkup(applied_from=None, applied_until=None, markup_percent=7)]

    result = pantry_service.get_partner_cost(pantry_item, partner_markups)

    expected = [
        PantryItemCost(start_date=None, end_date=parse_to_datetime("2025-03-31"), production_cost_us_dollars=8.56),
        PantryItemCost(
            start_date=parse_to_datetime("2025-04-01"),
            end_date=parse_to_datetime("2025-05-30"),
            production_cost_us_dollars=10.17,
        ),
    ]

    assert result == expected
