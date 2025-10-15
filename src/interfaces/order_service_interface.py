from typing import Protocol
from uuid import UUID

from src.api.routes.v1.models import OrderPatchRequest, OrderPostRequest, OrderResponse


class OrderServiceInterface(Protocol):
    def create_order(self, partner_id: str, order_data: OrderPostRequest) -> OrderResponse: ...

    def update_order(self, partner_id: str, order_id: UUID, order_data: OrderPatchRequest) -> OrderResponse: ...

    def delete_order(self, partner_id: str, order_id: UUID) -> None: ...
