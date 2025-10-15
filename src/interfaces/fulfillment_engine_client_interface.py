from typing import Protocol
from uuid import UUID

from src.services.models.orders import Order


class FulfillmentEngineClientInterface(Protocol):
    def get_order(self, order_id: UUID) -> Order: ...

    def mark_fulfillable(self, order_id: UUID) -> Order: ...

    def update_order(self, order: Order) -> Order: ...

    def cancel_order(self, order_id: UUID) -> None: ...
