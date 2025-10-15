from datetime import datetime
from uuid import UUID


class PantryState:
    def __init__(
        self,
        partner_id: str,
        pantry_state_id: UUID,
        pantry_state_timestamp: datetime,
        items_available_from: datetime | None = None,
        items_available_until: datetime | None = None,
    ):
        self._partner_id: str = partner_id
        self._pantry_state_id: UUID = pantry_state_id
        self._pantry_state_timestamp: datetime = pantry_state_timestamp
        self._items_available_from: datetime | None = items_available_from
        self._items_available_until: datetime | None = items_available_until

    @property
    def pantry_state_id(self) -> UUID:
        return self._pantry_state_id

    @property
    def pantry_state_timestamp(self) -> datetime:
        return self._pantry_state_timestamp

    @property
    def items_available_from(self) -> datetime | None:
        return self._items_available_from

    @property
    def items_available_until(self) -> datetime | None:
        return self._items_available_until
