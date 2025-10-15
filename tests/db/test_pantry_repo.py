from collections.abc import Iterator
from datetime import datetime, timedelta
from unittest.mock import MagicMock, patch
from uuid import uuid4

import pytest
from sqlalchemy.exc import SQLAlchemyError

from src.core.exceptions import ServerError
from src.db.pantry_repo import PantryRepo
from src.services.models.pantry import Pantry
from tests.db.test_data import make_pantry


@pytest.fixture
def mock_connection() -> MagicMock:
    return MagicMock()


@pytest.fixture
def pantry_repo(mock_connection: MagicMock) -> Iterator[PantryRepo]:
    repo = PantryRepo()
    with patch.object(repo, "_connection", return_value=mock_connection):
        yield repo


def test_get_partner_pantry_by_id_success(pantry_repo: PantryRepo, mock_connection: MagicMock) -> None:
    # UUIDs
    pantry_state_id = uuid4()
    partner_id = "TC-MAIN"
    now = datetime.now()
    yesterday = now.replace(hour=0, minute=0, second=0, microsecond=0) - timedelta(days=1)
    next_month = now.replace(hour=0, minute=0, second=0, microsecond=0) + timedelta(days=30)
    yesterday_dt_str = yesterday.strftime("%Y-%m-%d %H:%M:%S")
    next_month_dt_str = next_month.strftime("%Y-%m-%d %H:%M:%S")

    # Pantry state DB row mock
    pantry_state_row = {
        "partner_id": partner_id,
        "pantry_state_id": pantry_state_id,
        "pantry_state_timestamp": now,
        "items_available_from": yesterday_dt_str,
        "items_available_until": next_month_dt_str,
    }

    # Pantry items DB row mock
    pantry_item_id = uuid4()
    pantry_items_rows = [
        {
            "pantry_item_id": pantry_item_id,
            "description": "Test item",
            "amount": 2.5,
            "units": "kg",
            "is_prepped_and_ready": True,
        }
    ]

    # Costs, availabilities, custom fields
    pantry_item_costs_rows = [
        {
            "pantry_item_id": pantry_item_id,
            "production_cost_us_dollars": 12.34,
            "applied_from": "2024-01-01 00:00:00",
            "applied_until": "2024-12-31 00:00:00",
        }
    ]
    pantry_item_availabilities_rows = [
        {
            "pantry_item_id": pantry_item_id,
            "applied_from": "2024-01-01 00:00:00",
            "applied_until": "2024-12-31 00:00:00",
        }
    ]
    pantry_item_custom_fields_rows = [{"pantry_item_id": pantry_item_id, "key": "field1", "value": "value1"}]
    partner_cost_markups_rows = [
        {
            "applied_from": "2024-01-01 00:00:00",
            "applied_until": "2024-12-31 00:00:00",
            "markup_percent": 15.0,
        }
    ]

    # Set up the execute/mappings/return pattern per query in sequence
    mock_connection.__enter__.return_value = mock_connection
    mock_connection.execute.side_effect = [
        # 1. pantry_states
        MagicMock(mappings=MagicMock(return_value=MagicMock(fetchone=MagicMock(return_value=pantry_state_row)))),
        # 2. total_count
        MagicMock(scalar=MagicMock(return_value=len(pantry_items_rows))),
        # 3. pantry_items
        MagicMock(mappings=MagicMock(return_value=MagicMock(fetchall=MagicMock(return_value=pantry_items_rows)))),
        # 4. costs
        MagicMock(mappings=MagicMock(return_value=pantry_item_costs_rows)),
        # 5. availabilities
        MagicMock(mappings=MagicMock(return_value=pantry_item_availabilities_rows)),
        # 6. custom_fields
        MagicMock(mappings=MagicMock(return_value=pantry_item_custom_fields_rows)),
        # 7. cost_markups
        MagicMock(mappings=MagicMock(return_value=partner_cost_markups_rows)),
    ]

    pantry, total_count = pantry_repo.get_partner_pantry_by_id(str(pantry_state_id), str(partner_id), 100)

    assert pantry is not None
    assert isinstance(pantry, Pantry)
    assert total_count == 1
    assert pantry.pantry_state_id == str(pantry_state_id)
    assert pantry.partner_id == str(partner_id)
    assert len(pantry.pantry_items) == 1
    item = pantry.pantry_items[0]
    assert item.description == "Test item"
    assert item.amount == 2.5
    assert item.is_prepped_and_ready is True
    assert len(item.cost) == 1
    assert item.cost[0].production_cost_us_dollars == 12.34
    assert len(item.availability) == 1
    assert item.availability[0].available_from is not None
    assert isinstance(item.availability[0].available_from, datetime)
    assert item.availability[0].available_from.year == 2024
    assert len(item.custom_fields) == 1
    assert item.custom_fields[0].key == "field1"
    assert len(pantry.partner_cost_markup) == 1
    assert pantry.partner_cost_markup[0].markup_percent == 15.0


def test_get_partner_pantry_by_id_db_error(pantry_repo: PantryRepo, mock_connection: MagicMock) -> None:
    conn = MagicMock()
    conn.execute.side_effect = SQLAlchemyError("DB Error")

    mock_connection.__enter__.return_value = conn

    with pytest.raises(ServerError):
        pantry_repo.get_partner_pantry_by_id(pantry_state_id=str(uuid4()), partner_id="TC-MAIN", page_size=100)


def test_save_pantry_state_success(pantry_repo: PantryRepo, mock_connection: MagicMock) -> None:
    mock_connection.__enter__.return_value = mock_connection

    pantry_state_id = uuid4()
    pantry_repo.save_pantry_state(
        pantry_state_id=pantry_state_id,
        partner_id="TC-MAIN",
        pantry_state_timestamp=datetime.now(),
        items_available_from=datetime.now(),
        items_available_until=datetime.now() + timedelta(days=7),
    )

    assert mock_connection.execute.call_count == 1


def test_save_pantry_state_db_error_raises(pantry_repo: PantryRepo, mock_connection: MagicMock) -> None:
    mock_connection.__enter__.side_effect = SQLAlchemyError("DB broke")
    with pytest.raises(ServerError):
        pantry_repo.save_pantry_state(
            pantry_state_id=uuid4(),
            partner_id="TC-MAIN",
            pantry_state_timestamp=datetime.now(),
            items_available_from=None,
            items_available_until=None,
        )


def test_save_pantry_items_success(pantry_repo: PantryRepo, mock_connection: MagicMock) -> None:
    mock_connection.__enter__.return_value = mock_connection

    pantry = make_pantry()
    pantry_repo.save_pantry_items(pantry_state_id=uuid4(), items=pantry.pantry_items)
    assert mock_connection.execute.call_count == 5


def test_save_pantry_items_missing_data_source_raises(pantry_repo: PantryRepo) -> None:
    pantry = make_pantry()
    for item in pantry.pantry_items:
        item.pantry_item_data_source = None
    with pytest.raises(ValueError, match="Pantry item data source is required"):
        pantry_repo.save_pantry_items(pantry_state_id=uuid4(), items=pantry.pantry_items)


def test_save_pantry_items_db_error_raises(pantry_repo: PantryRepo, mock_connection: MagicMock) -> None:
    mock_connection.__enter__.side_effect = SQLAlchemyError("DB broke")
    pantry = make_pantry()
    with pytest.raises(ServerError):
        pantry_repo.save_pantry_items(pantry_state_id=uuid4(), items=pantry.pantry_items)


def test_delete_pantry_success(pantry_repo: PantryRepo, mock_connection: MagicMock) -> None:
    mock_connection.__enter__.return_value = mock_connection
    pantry_repo.delete_pantry(uuid4())

    assert mock_connection.execute.call_count == 6


def test_delete_pantry_db_error_raises(pantry_repo: PantryRepo, mock_connection: MagicMock) -> None:
    mock_connection.__enter__.side_effect = SQLAlchemyError("DB broke")
    with pytest.raises(ServerError):
        pantry_repo.delete_pantry(uuid4())
