from blueapron.proto.FulfillmentManagementService.Brand_pb2 import Brand
from blueapron.proto.FulfillmentManagementService.MessageFlow_pb2 import (
    ConsumerToFulfillmentMessage,
    FulfillmentOptions,
    FulfillmentReferenceId,
    FulfillmentRequest,
    MessageVersion,
    SalesChannelId,
    TargetArrival,
)
from blueapron.proto.shared.contacts.AssignedAddress_pb2 import (
    AssignedAddress,
    LocationType as ProtoLocationType,
)
from blueapron.proto.shared.contacts.PhoneNumber_pb2 import DialablePhone
from blueapron.proto.shared.LineItem_pb2 import LineItem
from blueapron.proto.vendor.google.type.date_pb2 import Date
from blueapron.proto.vendor.google.type.postal_address_pb2 import PostalAddress

from src.clients.kafka.base_producer import BaseProducer
from src.core.config import settings
from src.core.exceptions import ServerError
from src.services.models.orders import LocationType, Order, SpecialHandlings


class FulfillmentProducer(BaseProducer):
    def __init__(self) -> None:
        super().__init__(topic=settings.FULFILLMENT_TOPIC)

    def send_fulfillment_message(self, order: Order) -> None:
        postal_address = PostalAddress(
            postal_code=order.shipping_address.postal_address.postal_code,
            administrative_area=order.shipping_address.postal_address.administrative_area,
            locality=order.shipping_address.postal_address.locality,
            address_lines=order.shipping_address.postal_address.address_lines,
            recipients=order.shipping_address.postal_address.recipients,
        )

        try:
            location_type = self._map_order_location_type(order.shipping_address.location_type)
        except ValueError as e:
            raise ValueError(f"Invalid location type for order {order.id}") from e

        shipping_address = AssignedAddress(
            postal_address=postal_address,
            contact_number=DialablePhone(phone_number=order.shipping_address.contact_number.phone_number),
            delivery_instructions=order.shipping_address.delivery_instructions,
            location_type=location_type,
        )

        fulfillment_req_kwargs = {
            "message_version": MessageVersion(version=1),
            "fulfillment_reference_id": FulfillmentReferenceId(id=order.id),
            "shipping_address": shipping_address,
            "target_arrival": TargetArrival(
                arrival_date=Date(
                    year=order.arrival_date.year, month=order.arrival_date.month, day=order.arrival_date.day
                )
            ),
            "line_items": [
                LineItem(
                    sku=recipe.recipe_sku,
                    quantity=recipe.quantity,
                )
                for recipe in order.recipes
            ],
            "status": self._map_order_status(order.fulfillable),
        }

        if order.brand:
            fulfillment_req_kwargs["brand"] = Brand(name=order.brand)

        if order.sales_channel_id:
            fulfillment_req_kwargs["sales_channel_id"] = SalesChannelId(id=order.sales_channel_id)

        if order.fulfillment_options and order.fulfillment_options.delivery_option_token:
            fulfillment_req_kwargs["delivery_option_token"] = order.fulfillment_options.delivery_option_token

        if order.fulfillment_options and order.fulfillment_options.special_handlings:
            try:
                special_handlings = self._map_special_handlings(order.fulfillment_options.special_handlings)
                fulfillment_req_kwargs["fulfillment_options"] = FulfillmentOptions(special_handlings=special_handlings)
            except ValueError as e:
                raise ValueError(f"Invalid special handling options for order {order.id}") from e

        fulfillment_req = FulfillmentRequest(**fulfillment_req_kwargs)

        consumer_fulfillment_msg = ConsumerToFulfillmentMessage(fulfillment_request=fulfillment_req)

        try:
            self.produce(consumer_fulfillment_msg)
        except Exception as e:
            raise ServerError(
                f"Failed to produce fulfillment message to topic{settings.FULFILLMENT_TOPIC} for order {order.id}"
            ) from e

    @staticmethod
    def _map_order_status(fulfillable: bool) -> FulfillmentRequest.Status:
        return FulfillmentRequest.Status.FULFILLABLE if fulfillable else FulfillmentRequest.Status.COMMITTED

    @staticmethod
    def _map_special_handlings(special_handlings: list[SpecialHandlings]) -> list[FulfillmentOptions.SpecialHandling]:
        mapped_handlings: list[FulfillmentOptions.SpecialHandling] = []
        for handling in special_handlings:
            if handling == SpecialHandlings.WHITE_GLOVE_BOX:
                mapped_handlings.append(FulfillmentOptions.SpecialHandling.WHITE_GLOVE_BOX)
            elif handling == SpecialHandlings.GUARANTEED_DELIVERY:
                mapped_handlings.append(FulfillmentOptions.SpecialHandling.GUARANTEED_DELIVERY)
            else:
                raise ValueError(f"Invalid special handling: {handling}")
        return mapped_handlings

    @staticmethod
    def _map_order_location_type(location_type: LocationType) -> ProtoLocationType:
        if location_type == LocationType.RESIDENTIAL:
            return ProtoLocationType.RESIDENTIAL
        elif location_type == LocationType.COMMERCIAL:
            return ProtoLocationType.COMMERCIAL
        else:
            raise ValueError(f"Invalid location type: {location_type}")
