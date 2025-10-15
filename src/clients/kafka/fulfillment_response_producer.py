from uuid import UUID

from blueapron.proto.FulfillmentManagementService.MessageFlow_pb2 import (
    FulfillmentReferenceId,
    FulfillmentResponse,
    FulfillmentToConsumerMessage,
    SalesChannelId,
)
from blueapron.proto.vendor.google.rpc.status_pb2 import Status

from src.clients.kafka.base_producer import BaseProducer
from src.core.config import settings
from src.core.exceptions import ServerError


class FulfillmentResponseProducer(BaseProducer):
    def __init__(self) -> None:
        super().__init__(settings.FULFILLMENT_RESPONSE_TOPIC)

    # UNKNOWN is the only available status that indicates a service failure to process an order.
    # When protos become updateable, we can change this to a more specific status.
    def send_fulfillment_response_failed(
        self, order_id: UUID, reason: str, sales_channel_id: str | None = None
    ) -> None:
        if not reason or not order_id:
            raise ValueError("Reason and order_id are required for failed fulfillment response")

        fulfillment_response_kwargs = {
            "fulfillment_reference_id": FulfillmentReferenceId(id=str(order_id)),
            "status": Status(code=FulfillmentResponse.Status.UNKNOWN, message=reason),
        }

        if sales_channel_id:
            fulfillment_response_kwargs["sales_channel_id"] = SalesChannelId(id=sales_channel_id)

        fulfillment_response = FulfillmentResponse(**fulfillment_response_kwargs)

        consumer_fulfillment_msg = FulfillmentToConsumerMessage(
            fulfillment_response=fulfillment_response,
        )

        try:
            self.produce(consumer_fulfillment_msg)
        except ServerError as e:
            raise ServerError(
                "Failed to produce fulfillment response failed message "
                f"to topic{settings.FULFILLMENT_RESPONSE_TOPIC} for order {order_id}"
            ) from e
