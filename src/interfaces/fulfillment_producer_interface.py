from typing import Protocol

from src.services.models.orders import Order


class FulfillmentProducerInterface(Protocol):
    def send_fulfillment_message(self, order: Order) -> None: ...
