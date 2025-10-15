from datetime import UTC, datetime, timedelta
from uuid import UUID, uuid4

from src.services.models.pantry import (
    Pantry,
    PantryItem,
    PantryItemAvailability,
    PantryItemCost,
    PantryItemCustomField,
    PantryItemDataSource,
)
from src.utils.datetime_helper import parse_to_datetime


def make_data_source() -> PantryItemDataSource:
    return PantryItemDataSource(culops_culinary_ingredient_id=11, culops_culinary_ingredient_specification_id=22)


def make_custom_field(item_id: str) -> PantryItemCustomField:
    return PantryItemCustomField(key="field1", value="value1")


def make_availability() -> PantryItemAvailability:
    return PantryItemAvailability(
        available_from=parse_to_datetime("2024-01-01"), available_until=parse_to_datetime("2024-12-31")
    )


def make_cost() -> PantryItemCost:
    return PantryItemCost(
        production_cost_us_dollars=5.75,
        start_date=parse_to_datetime("2024-01-01"),
        end_date=parse_to_datetime("2024-12-31"),
    )


def make_pantry_item() -> PantryItem:
    item_id = str(uuid4())
    data_source = make_data_source()
    item = PantryItem(
        id=item_id,
        units="lb",
        amount=2.5,
        pantry_item_data_source=data_source,
        is_prepped_and_ready=True,
        description="Test Item",
        availability=[],
        cost=[],
        custom_fields=[make_custom_field("123")],
    )
    item.add_cost(make_cost())
    item.add_availability(make_availability())
    return item


def make_pantry() -> Pantry:
    pantry_state_id = str(uuid4())
    partner_id = str(uuid4())
    return Pantry(
        pantry_state_id=pantry_state_id,
        partner_id=partner_id,
        pantry_state_timestamp=datetime(2024, 1, 1),
        pantry_items=[make_pantry_item()],
        partner_cost_markup=[],
    )


def make_partner_cost_markup_row(
    partner_id: str, applied_from: datetime | None = None, applied_until: datetime | None = None
) -> dict:
    a_f = (applied_from or datetime.now(UTC)).isoformat(timespec="seconds")
    a_u = (applied_until or datetime.now(UTC) + timedelta(days=365)).isoformat(timespec="seconds")
    return {
        "partner_id": str(partner_id),
        "applied_from": a_f,
        "applied_until": a_u,
        "markup_percent": 5.0,
    }


def make_partner_assembly_packaging_option_row(id: int = 1, packaging_option: str | None = None) -> dict:
    return {
        "assembly_packaging_option_id": id,
        "assembly_packaging_option_name": packaging_option or "bagged",
    }


def make_idempotency_key_row(
    idempotent_action: str,
    idempotency_key: UUID | None = None,
    expires_at: datetime | None = None,
) -> dict:
    return {
        "idempotentActionKey": idempotent_action,
        "idempotencyKey": idempotency_key or uuid4(),
        "expiresAt": expires_at or datetime.now(UTC) + timedelta(minutes=1440),
    }
