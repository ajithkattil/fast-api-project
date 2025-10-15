from __future__ import annotations

from datetime import date, datetime
from uuid import UUID, uuid4

from src.api.routes.v1.models import (
    Address as RouteAddress,
    ContactNumber as RouteContactNumber,
    FulfillmentOptions as RouteFulfillmentOptions,
    OrderPatchRequest,
    OrderPostRequest,
    OrderRecipe as RouteOrderRecipe,
    OrderResponse,
    PostalAddress as RoutePostalAddress,
    SpecialHandlings as RouteSpecialHandlings,
)
from src.core.exceptions import RecipeAlreadyDeletedError, RecipeNotFoundError, ServerError
from src.interfaces.culops_client_interface import CulopsClientInterface
from src.interfaces.fulfillment_engine_client_interface import FulfillmentEngineClientInterface
from src.interfaces.fulfillment_producer_interface import FulfillmentProducerInterface
from src.interfaces.fulfillment_response_producer_interface import FulfillmentResponseProducerInterface
from src.interfaces.order_service_interface import OrderServiceInterface
from src.interfaces.pantry_db_interface import PantryDBInterface
from src.interfaces.partner_repo_interface import PartnerRepoInterface
from src.interfaces.recipes_repo_interface import RecipesRepoInterface
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
from src.utils.datetime_helper import parse_to_datetime
from src.utils.logger import ServiceLogger
from src.utils.logger_context import set_logger_context_value
from src.utils.task_scheduler import TaskScheduler

logger = ServiceLogger().get_logger(__name__)


class OrderService(OrderServiceInterface):
    def __init__(
        self,
        partner_repo: PartnerRepoInterface,
        pantry_repo: PantryDBInterface,
        culops_client: CulopsClientInterface,
        fulfillment_client: FulfillmentEngineClientInterface,
        fulfillment_producer: FulfillmentProducerInterface,
        fulfillment_response_producer: FulfillmentResponseProducerInterface,
        recipes_repo: RecipesRepoInterface,
    ) -> None:
        self._partner_repo = partner_repo
        self._pantry_repo = pantry_repo
        self._culops_client = culops_client
        self._fulfillment_client = fulfillment_client
        self._fulfillment_producer = fulfillment_producer
        self._fulfillment_response_producer = fulfillment_response_producer
        self._recipes_repo = recipes_repo

    def create_order(
        self,
        partner_id: str,
        order_data: OrderPostRequest,
    ) -> OrderResponse:
        recipe_skus: list[tuple[str, int]] = []
        for recipe in order_data.recipes:
            sku = self._recipes_repo.get_recipe_sku_by_id(partner_id, recipe.recipe_id)
            if sku is None:
                raise RecipeNotFoundError(f"Recipe {recipe.recipe_id} not found")
            if sku[1].DELETED:
                raise RecipeAlreadyDeletedError(f"Recipe {recipe.recipe_id} is deleted")
            recipe_skus.append((sku[0], recipe.quantity))

        order = self._order_from_order_post_request(order_data, recipe_skus)

        t = TaskScheduler()
        _future = t.schedule_async_task(self._send_order_to_fes(order, partner_id))

        return self._order_response_from_order(order, order_data.recipes)

    async def _send_order_to_fes(self, o: Order, partner_id: str) -> None:
        set_logger_context_value("order_id", o.id)
        set_logger_context_value("partner_id", partner_id)

        try:
            self._fulfillment_producer.send_fulfillment_message(o)
        except ServerError as e:
            self._fulfillment_response_producer.send_fulfillment_response_failed(UUID(o.id), str(e), o.sales_channel_id)

    @staticmethod
    def _order_from_order_post_request(order_data: OrderPostRequest, recipe_skus: list[tuple[str, int]]) -> Order:
        contact_number = ContactNumber(phone_number=order_data.shipping_address.contact_number.phone_number)
        postal_address = PostalAddress(
            postal_code=order_data.shipping_address.postal_address.postal_code,
            administrative_area=order_data.shipping_address.postal_address.administrative_area,
            locality=order_data.shipping_address.postal_address.locality,
            address_lines=order_data.shipping_address.postal_address.address_lines
            if order_data.shipping_address.postal_address.address_lines
            else [],
            recipients=order_data.shipping_address.postal_address.recipients
            if order_data.shipping_address.postal_address.recipients
            else [],
        )
        shipping_address = ShippingAddress(
            postal_address=postal_address,
            contact_number=contact_number,
            location_type=LocationType(order_data.shipping_address.location_type),
            delivery_instructions=order_data.shipping_address.delivery_instructions,
        )
        fulfillment_options = None
        if order_data.fulfillment_options:
            special_handlings = [
                SpecialHandlings(handling) for handling in order_data.fulfillment_options.special_handlings
            ]
            fulfillment_options = FulfillmentOptions(
                order_data.fulfillment_options.delivery_option_token, special_handlings
            )

        recipes = [OrderRecipe(quantity=recipe[1], recipe_sku=recipe[0]) for recipe in recipe_skus]

        return Order(
            id=str(uuid4()),
            arrival_date=datetime.strptime(order_data.arrival_date, "%Y-%m-%d"),
            fulfillable=order_data.fulfillable,
            shipping_address=shipping_address,
            fulfillment_options=fulfillment_options,
            recipes=recipes,
            brand=order_data.brand_id,
            sales_channel_id=order_data.sales_channel_id,
        )

    @staticmethod
    def _order_response_from_order(order: Order, recipes: list[RouteOrderRecipe]) -> OrderResponse:
        contact_number = RouteContactNumber(phoneNumber=order.shipping_address.contact_number.phone_number)
        postal_address = RoutePostalAddress(
            postalCode=order.shipping_address.postal_address.postal_code,
            administrativeArea=order.shipping_address.postal_address.administrative_area,
            locality=order.shipping_address.postal_address.locality,
            addressLines=order.shipping_address.postal_address.address_lines,
            recipients=order.shipping_address.postal_address.recipients,
        )
        shipping_address = RouteAddress(
            postalAddress=postal_address,
            contactNumber=contact_number,
            locationType=order.shipping_address.location_type,
            deliveryInstructions=order.shipping_address.delivery_instructions,
        )

        fulfillment_options = None
        if (
            order.fulfillment_options
            and order.fulfillment_options.special_handlings is not None
            and len(order.fulfillment_options.special_handlings) > 0
        ):
            special_handlings = [
                RouteSpecialHandlings(str(handling)) for handling in order.fulfillment_options.special_handlings
            ]
            fulfillment_options = RouteFulfillmentOptions(
                deliveryOptionToken=order.fulfillment_options.delivery_option_token, specialHandlings=special_handlings
            )

        recipes = [RouteOrderRecipe(quantity=recipe.quantity, recipeId=recipe.recipe_id) for recipe in recipes]

        return OrderResponse(
            orderId=str(order.id),
            arrivalDate=order.arrival_date.strftime("%Y-%m-%d"),
            recipes=recipes,
            fulfillable=order.fulfillable,
            salesChannelId=order.sales_channel_id,
            brandId=order.brand,
            shippingAddress=shipping_address,
            fulfillmentOptions=fulfillment_options,
        )

    def update_order(self, partner_id: str, order_id: UUID, order_data: OrderPatchRequest) -> OrderResponse:
        try:
            if order_data.fulfillable and len(order_data.model_dump(exclude_none=True)) == 1:
                updated_fulfillment = self._fulfillment_client.mark_fulfillable(order_id=order_id)
            else:
                current_fulfillment = self._fulfillment_client.get_order(order_id=order_id)

                if not current_fulfillment:
                    raise ValueError(f"No fulfillment found for order ID: {order_id}")

                culops_recipe_skus = []
                if order_data.recipes:
                    for recipe in order_data.recipes:
                        result = self._recipes_repo.get_recipe_sku_by_id(
                            partner_id=partner_id, recipe_id=recipe.recipe_id
                        )
                        if result is None:
                            raise ValueError(f"No recipe SKU found for recipe ID {recipe.recipe_id}")

                        recipe_sku, status = result
                        if status.DELETED:
                            raise RecipeAlreadyDeletedError(f"Recipe {recipe.recipe_id} has been deleted")
                        culops_recipe_skus.append(OrderRecipe(recipe_sku=recipe_sku, quantity=recipe.quantity))

                updated_order = self._map_order_from_patch_request_order(
                    order_id, order_data, current_fulfillment, culops_recipe_skus
                )

                updated_fulfillment = self._fulfillment_client.update_order(order=updated_order)

            return self._map_order_to_order_response(updated_fulfillment)

        except Exception:
            raise

    def delete_order(self, partner_id: str, order_id: UUID) -> None:
        try:
            self._fulfillment_client.cancel_order(order_id=order_id)
        except (ServerError, ValueError) as e:
            raise ServerError(f"Failed to cancel order, internal error canceling fulfillment order {order_id}") from e

    @staticmethod
    def _map_order_to_order_response(order: Order) -> OrderResponse:
        postal_address = RoutePostalAddress(
            postalCode=order.shipping_address.postal_address.postal_code,
            administrativeArea=order.shipping_address.postal_address.administrative_area,
            locality=order.shipping_address.postal_address.locality,
            addressLines=order.shipping_address.postal_address.address_lines,
            recipients=order.shipping_address.postal_address.recipients,
        )

        contact_number = RouteContactNumber(phoneNumber=order.shipping_address.contact_number.phone_number)

        shipping_address = RouteAddress(
            postalAddress=postal_address,
            contactNumber=contact_number,
            locationType=order.shipping_address.location_type,
            deliveryInstructions=order.shipping_address.delivery_instructions,
        )

        return OrderResponse(
            orderId=str(order.id),
            arrivalDate=order.arrival_date.isoformat() if order.arrival_date else date.today().isoformat(),
            recipes=order.recipes or [],
            fulfillable=order.fulfillable if order.fulfillable is not None else True,
            salesChannelId=order.sales_channel_id,
            brandId=order.brand,
            shippingAddress=shipping_address,
            fulfillmentOptions=order.fulfillment_options,
        )

    @staticmethod
    def _map_order_from_patch_request_order(
        order_id: UUID, order_data: OrderPatchRequest, backup_data: Order, culops_recipe_skus: list[OrderRecipe]
    ) -> Order:
        arrival_date = (
            parse_to_datetime(order_data.arrival_date) if order_data.arrival_date else backup_data.arrival_date
        )

        shipping_address_data = order_data.shipping_address
        fulfillment_options_data = order_data.fulfillment_options
        backup_fulfillment_options = backup_data.fulfillment_options or FulfillmentOptions()

        return Order(
            id=str(order_id),
            arrival_date=arrival_date,
            fulfillable=backup_data.fulfillable,
            shipping_address=ShippingAddress(
                postal_address=RoutePostalAddress(
                    postalCode=(
                        shipping_address_data.postal_code
                        if shipping_address_data and shipping_address_data.postal_code
                        else backup_data.shipping_address.postal_address.postal_code
                    ),
                    administrativeArea=(
                        shipping_address_data.administrative_area
                        if shipping_address_data and shipping_address_data.administrative_area
                        else backup_data.shipping_address.postal_address.administrative_area
                    ),
                    locality=(
                        shipping_address_data.locality
                        if shipping_address_data and shipping_address_data.locality
                        else backup_data.shipping_address.postal_address.locality
                    ),
                    addressLines=(
                        shipping_address_data.addressLines
                        if shipping_address_data and shipping_address_data.addressLines
                        else backup_data.shipping_address.postal_address.address_lines
                    ),
                    recipients=(
                        shipping_address_data.recipients
                        if shipping_address_data and shipping_address_data.recipients
                        else backup_data.shipping_address.postal_address.recipients
                    ),
                ),
                contact_number=RouteContactNumber(
                    phoneNumber=(
                        shipping_address_data.phoneNumber
                        if shipping_address_data and shipping_address_data.phoneNumber
                        else backup_data.shipping_address.contact_number.phone_number
                    )
                ),
                location_type=(
                    fulfillment_options_data.location_type
                    if fulfillment_options_data and fulfillment_options_data.location_type
                    else backup_data.shipping_address.location_type
                ),
                delivery_instructions=(
                    fulfillment_options_data.delivery_instructions
                    if fulfillment_options_data and fulfillment_options_data.delivery_instructions
                    else backup_data.shipping_address.delivery_instructions
                ),
            ),
            recipes=culops_recipe_skus if culops_recipe_skus else backup_data.recipes,
            brand=order_data.brand_id or backup_data.brand,
            fulfillment_options=RouteFulfillmentOptions(
                specialHandlings=(
                    fulfillment_options_data.specialHandlings
                    if fulfillment_options_data and fulfillment_options_data.specialHandlings
                    else backup_fulfillment_options.special_handlings
                ),
                deliveryOptionToken=(
                    fulfillment_options_data.deliveryOptionToken
                    if fulfillment_options_data and fulfillment_options_data.deliveryOptionToken
                    else backup_fulfillment_options.delivery_option_token
                ),
            ),
            sales_channel_id=order_data.sales_channel_id or backup_data.sales_channel_id,
        )
