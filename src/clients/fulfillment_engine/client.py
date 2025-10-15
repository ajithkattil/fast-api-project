import atexit
import threading
from datetime import datetime
from uuid import UUID

import grpc
from blueapron.proto.FulfillmentManagementService.Brand_pb2 import Brand
from blueapron.proto.FulfillmentManagementService.FulfillmentManagementService_pb2 import (
    GetFulfillmentRequest,
    GetFulfillmentResponse,
    MarkFulfillableRequest,
    MarkFulfillableResponse,
    UpdateFulfillmentRequest,
    UpdateFulfillmentResponse,
)
from blueapron.proto.FulfillmentManagementService.FulfillmentManagementService_pb2_grpc import (
    FulfillmentManagementServiceStub,
)
from blueapron.proto.FulfillmentManagementService.MessageFlow_pb2 import (
    CancelFulfillmentRequest,
    CancelFulfillmentResponse,
    Fulfillment,
    FulfillmentOptions as ProtoFulfillmentOptions,
    FulfillmentReferenceId,
    FulfillmentRequest,
    SalesChannelId,
    TargetArrival,
)
from blueapron.proto.shared.contacts.AssignedAddress_pb2 import (
    AssignedAddress,
    LocationType as ProtoLocationType,
)
from blueapron.proto.shared.contacts.PhoneNumber_pb2 import DialablePhone
from blueapron.proto.shared.LineItem_pb2 import LineItem
from blueapron.proto.vendor.google.rpc.code_pb2 import Code
from blueapron.proto.vendor.google.type.date_pb2 import Date
from blueapron.proto.vendor.google.type.postal_address_pb2 import PostalAddress as ProtoPostalAddress

from src.core.config import settings
from src.core.exceptions import OrderNotFoundError, ServerError
from src.interfaces.fulfillment_engine_client_interface import FulfillmentEngineClientInterface
from src.services.models.orders import (
    ContactNumber,
    FulfillmentOptions,
    LocationType,
    Order,
    OrderRecipe,
    PostalAddress,
    ShippingAddress,
    SpecialHandlings,
)


class FulfillmentEngineClient(FulfillmentEngineClientInterface):
    _shared_channel: grpc.Channel | None = None
    _channel_lock = threading.Lock()

    @classmethod
    def _get_channel(cls) -> grpc.Channel:
        if cls._shared_channel is None:
            with cls._channel_lock:
                if cls._shared_channel is None:
                    message_size = 4 * 1024 * 1024
                    options = [
                        ("grpc.keepalive_time_ms", 30000),
                        ("grpc.keepalive_timeout_ms", 5000),
                        ("grpc.keepalive_permit_without_calls", True),
                        ("grpc.http2.max_pings_without_data", 0),
                        ("grpc.max_receive_message_length", message_size),
                        ("grpc.max_send_message_length", message_size),
                    ]

                    cls._shared_channel = grpc.insecure_channel(
                        f"{settings.FES_GRPC_HOST}:{settings.GRPC_PORT}",
                        options=options,
                    )

                    atexit.register(cls._cleanup_channel)

        return cls._shared_channel

    @classmethod
    def _cleanup_channel(cls) -> None:
        if cls._shared_channel:
            cls._shared_channel.close()
            cls._shared_channel = None

    def __init__(self) -> None:
        self.channel = self._get_channel()
        self.client = FulfillmentManagementServiceStub(self.channel)

    def get_order(self, order_id: UUID) -> Order:
        req = GetFulfillmentRequest(fulfillment_reference_id=FulfillmentReferenceId(id=str(order_id)))

        try:
            res: GetFulfillmentResponse = self.client.GetFulfillment(req)
        except grpc.RpcError as e:
            raise ServerError(f"Failed to get order, internal error getting fulfillment order {order_id}") from e

        if res.status.code == Code.NOT_FOUND:
            raise OrderNotFoundError(f"Failed to get order, fulfillment not found for order {order_id}")
        elif res.status.code == Code.INVALID_ARGUMENT:
            mes = f"Failed to get order, invalid argument getting fulfillment order {order_id}"
            if res.status.message not in ["", None]:
                mes += f": {res.status.message}"
            raise ValueError(mes)
        elif res.status.code == Code.INTERNAL:
            mes = f"Failed to get order, internal error getting fulfillment order {order_id}"
            if res.status.message not in ["", None]:
                mes += f": {res.status.message}"
            raise ServerError(mes)

        fulfillment_order = res.fulfillment

        return self._map_fulfillment_order(order_id, fulfillment_order)

    def mark_fulfillable(self, order_id: UUID) -> Order:
        req = MarkFulfillableRequest(fulfillment_reference_id=FulfillmentReferenceId(id=str(order_id)))

        try:
            res: MarkFulfillableResponse = self.client.MarkFulfillable(req)
        except grpc.RpcError as e:
            raise ServerError(
                f"Failed to mark fulfillable, internal error marking fulfillment order {order_id} as fulfillable"
            ) from e

        if res.status.code == Code.NOT_FOUND:
            raise OrderNotFoundError(f"Failed to mark fulfillable, fulfillment not found for order {order_id}")
        elif res.status.code == Code.INVALID_ARGUMENT:
            mes = f"Failed to mark fulfillable, invalid argument marking fulfillment order {order_id} as fulfillable"
            if res.status.message not in ["", None]:
                mes += f": {res.status.message}"
            raise ValueError(mes)
        elif res.status.code == Code.INTERNAL:
            mes = f"Failed to mark fulfillable, internal error marking fulfillment order {order_id} as fulfillable"
            if res.status.message not in ["", None]:
                mes += f": {res.status.message}"
            raise ServerError(mes)

        order = self.get_order(order_id)
        if not order.fulfillable:
            raise ServerError(f"Failed to mark fulfillment order {order_id} as fulfillable")

        return order

    def update_order(self, order: Order) -> Order:
        fulfillment_request = self._map_order_to_fulfillment_request(order)

        try:
            req = UpdateFulfillmentRequest(fulfillment_request=fulfillment_request)
        except ValueError as e:
            raise ValueError(f"Failed to update order {order.id}") from e

        try:
            res: UpdateFulfillmentResponse = self.client.UpdateFulfillment(req)
        except grpc.RpcError as e:
            raise ServerError(f"Failed to update order, internal error updating fulfillment order {order.id}") from e

        if res.status.code == Code.NOT_FOUND:
            raise OrderNotFoundError(f"Failed to update order, fulfillment not found for order {order.id}")
        elif res.status.code == Code.INVALID_ARGUMENT:
            mes = f"Failed to update order, invalid argument updating fulfillment order {order.id}"
            if res.status.message not in ["", None]:
                mes += f": {res.status.message}"
            raise ValueError(mes)
        elif res.status.code == Code.INTERNAL:
            mes = f"Failed to update order, internal error updating fulfillment order {order.id}"
            if res.status.message not in ["", None]:
                mes += f": {res.status.message}"
            raise ServerError(mes)

        return order

    def cancel_order(self, order_id: UUID) -> None:
        cancel_fulfillment_request = CancelFulfillmentRequest(
            fulfillment_reference_id=FulfillmentReferenceId(id=str(order_id))
        )

        try:
            res: CancelFulfillmentResponse = self.client.CancelFulfillment(cancel_fulfillment_request)
        except grpc.RpcError as e:
            raise ServerError(f"Failed to cancel order, internal error canceling fulfillment order {order_id}") from e

        if res.status.code == Code.FAILED_PRECONDITION:
            raise OrderNotFoundError(f"Failed to cancel order, fulfillment not found for order {order_id}")

        elif res.status.code == Code.INTERNAL:
            mes = f"Failed to cancel order, internal error canceling fulfillment order {order_id}"
            if res.status.message not in ["", None]:
                mes += f": {res.status.message}"
            raise ServerError(mes)

    def _map_order_to_fulfillment_request(self, order: Order) -> FulfillmentRequest:
        try:
            postal_address = ProtoPostalAddress(
                postal_code=order.shipping_address.postal_address.postal_code,
                administrative_area=order.shipping_address.postal_address.administrative_area,
                locality=order.shipping_address.postal_address.locality,
                address_lines=order.shipping_address.postal_address.address_lines,
                recipients=order.shipping_address.postal_address.recipients,
            )

            location_type = self._map_order_location_type(order.shipping_address.location_type)

            shipping_address = AssignedAddress(
                postal_address=postal_address,
                contact_number=DialablePhone(phone_number=order.shipping_address.contact_number.phone_number),
                delivery_instructions=order.shipping_address.delivery_instructions,
                location_type=location_type,
            )

            assert order.fulfillment_options is not None, f"fulfillment_options is required for order {order.id}"

            fulfillment_req_kwargs = {
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
                "delivery_option_token": order.fulfillment_options.delivery_option_token,
            }

            if order.brand:
                fulfillment_req_kwargs["brand"] = Brand(name=order.brand)

            if order.sales_channel_id:
                fulfillment_req_kwargs["sales_channel_id"] = SalesChannelId(id=order.sales_channel_id)

            if order.fulfillment_options and order.fulfillment_options.special_handlings:
                special_handlings = self._map_special_handlings(order.fulfillment_options.special_handlings)
                fulfillment_req_kwargs["fulfillment_options"] = ProtoFulfillmentOptions(
                    special_handlings=special_handlings
                )

            return FulfillmentRequest(**fulfillment_req_kwargs)
        except ValueError as e:
            raise ValueError(f"Failed to map order {order.id} to fulfillment request") from e

    def _map_order_location_type(self, location_type: LocationType) -> ProtoLocationType:
        if location_type == LocationType.RESIDENTIAL:
            return ProtoLocationType.RESIDENTIAL
        elif location_type == LocationType.COMMERCIAL:
            return ProtoLocationType.COMMERCIAL
        else:
            raise ValueError(f"Invalid location type: {location_type}")

    def _map_order_status(self, fulfillable: bool) -> FulfillmentRequest.Status:
        return FulfillmentRequest.Status.FULFILLABLE if fulfillable else FulfillmentRequest.Status.COMMITTED

    def _map_special_handlings(
        self, special_handlings: list[SpecialHandlings]
    ) -> list[ProtoFulfillmentOptions.SpecialHandling]:
        mapped_handlings: list[ProtoFulfillmentOptions.SpecialHandling] = []
        for handling in special_handlings:
            if handling == SpecialHandlings.WHITE_GLOVE_BOX:
                mapped_handlings.append(ProtoFulfillmentOptions.SpecialHandling.WHITE_GLOVE_BOX)
            elif handling == SpecialHandlings.GUARANTEED_DELIVERY:
                mapped_handlings.append(ProtoFulfillmentOptions.SpecialHandling.GUARANTEED_DELIVERY)
            else:
                raise ValueError(f"Invalid special handling: {handling}")
        return mapped_handlings

    def _map_fulfillment_order(self, order_id: UUID, fulfillment_order: Fulfillment) -> Order:
        target_arrival = datetime(
            year=fulfillment_order.target_arrival.arrival_date.year,
            month=fulfillment_order.target_arrival.arrival_date.month,
            day=fulfillment_order.target_arrival.arrival_date.day,
        )

        fes_shipping_address = fulfillment_order.shipping_address

        postal_address = PostalAddress(
            postal_code=fes_shipping_address.postal_address.postal_code,
            administrative_area=fes_shipping_address.postal_address.administrative_area,
            locality=fes_shipping_address.postal_address.locality,
            address_lines=[al for al in fes_shipping_address.postal_address.address_lines],
            recipients=[r for r in fes_shipping_address.postal_address.recipients],
        )

        location_type_proto_to_enum_map = {
            ProtoLocationType.RESIDENTIAL: LocationType.RESIDENTIAL,
            ProtoLocationType.COMMERCIAL: LocationType.COMMERCIAL,
        }

        try:
            location_type = location_type_proto_to_enum_map[fes_shipping_address.location_type]
        except KeyError as e:
            location_type_name = ProtoLocationType.Name(fes_shipping_address.location_type)

            raise ServerError(f"Invalid location type: {location_type_name} in fulfillment for order {order_id}") from e
        delivery_instructions = fes_shipping_address.delivery_instructions or None

        shipping_address = ShippingAddress(
            postal_address=postal_address,
            contact_number=ContactNumber(
                phone_number=fes_shipping_address.contact_number.phone_number,
            ),
            location_type=location_type,
            delivery_instructions=delivery_instructions,
        )

        recipes = []
        for recipe in fulfillment_order.line_items:
            recipes.append(
                OrderRecipe(
                    quantity=recipe.quantity,
                    recipe_sku=recipe.sku,
                )
            )

        special_handling_proto_to_enum_map = {
            ProtoFulfillmentOptions.SpecialHandling.WHITE_GLOVE_BOX: SpecialHandlings.WHITE_GLOVE_BOX,
            ProtoFulfillmentOptions.SpecialHandling.GUARANTEED_DELIVERY: SpecialHandlings.GUARANTEED_DELIVERY,
        }

        special_handlings = []
        for special_handling in fulfillment_order.special_handlings:
            try:
                special_handlings.append(special_handling_proto_to_enum_map[special_handling])
            except KeyError as e:
                special_handling_name = ProtoFulfillmentOptions.SpecialHandling.Name(special_handling)
                raise ServerError(
                    f"Invalid special handling: {special_handling_name} in fulfillment for order {order_id}"
                ) from e

        delivery_option_token = fulfillment_order.shipments[0].shipping_method_id.id

        fulfillment_options = FulfillmentOptions(
            special_handlings=special_handlings,
            delivery_option_token=delivery_option_token,
        )

        order = Order(
            id=str(order_id),
            arrival_date=target_arrival,
            fulfillable=fulfillment_order.status == Fulfillment.Status.STATUS_ACTIVE,
            shipping_address=shipping_address,
            recipes=recipes,
            brand=(
                fulfillment_order.brand.name
                if fulfillment_order.HasField("brand") and fulfillment_order.brand.name
                else None
            ),
            sales_channel_id=(
                fulfillment_order.sales_channel_id.id
                if fulfillment_order.HasField("sales_channel_id") and fulfillment_order.sales_channel_id.id
                else None
            ),
            fulfillment_options=fulfillment_options,
        )
        return order
