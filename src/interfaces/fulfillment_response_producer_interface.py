from typing import Protocol
from uuid import UUID


class FulfillmentResponseProducerInterface(Protocol):
    def send_fulfillment_response_failed(
        self, order_id: UUID, reason: str, sales_channel_id: str | None = None
    ) -> None: ...
