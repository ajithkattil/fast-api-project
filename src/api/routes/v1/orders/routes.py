from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Body, Depends, Header, HTTPException, Path, Request, status

from src.api.routes.v1.models import ErrorResponse, OrderPatchRequest, OrderPostRequest, PostOrderData, SpecialHandlings
from src.core.exceptions import (
    AccessDeniedException,
    BadRequestException,
    ConflictException,
    GoneException,
    InternalException,
    OrderNotFoundError,
    RecipeAlreadyDeletedError,
    RecipeNotFoundError,
    ServerError,
    UnprocessableException,
)
from src.dependancies.idempotency_db import get_idempotency_db
from src.dependancies.order_service import get_order_service
from src.dependancies.partner_service import get_partner_service
from src.interfaces.idempotency_key_repo_interface import IdempotencyKeyRepoInterface
from src.interfaces.order_service_interface import OrderServiceInterface
from src.interfaces.partner_service_interface import PartnerServiceInterface
from src.utils.logger_context import set_logger_context_value
from src.utils.paginator import PaginatedResponse, paginate_response
from src.utils.validation import is_valid_uuid

router = APIRouter(
    prefix="/v1/orders",
    responses={
        422: {"model": ErrorResponse, "description": "Unprocessable Entity"},
    },
)


@router.get("")
def get_orders() -> None:
    return


order_body = Body(...)


@router.post(
    "",
    status_code=202,
    responses={
        400: {"model": ErrorResponse, "description": "Bad request"},
        401: {"model": ErrorResponse, "description": "Unauthorized"},
        409: {"model": ErrorResponse, "description": "Conflict"},
        422: {"model": ErrorResponse, "description": "Unprocessable Entity"},
        500: {"model": ErrorResponse, "description": "Internal Server Error"},
    },
)
def post_order(
    request: Request,
    idempotency_key: Annotated[str, Header(..., alias="Idempotency-Key")],
    order_post: OrderPostRequest = order_body,
    partner_service: PartnerServiceInterface = Depends(get_partner_service),
    idempotency_key_repo: IdempotencyKeyRepoInterface = Depends(get_idempotency_db),
    order_service: OrderServiceInterface = Depends(get_order_service),
) -> PaginatedResponse[PostOrderData]:
    try:
        if not partner_service.validate_partner_id():
            raise AccessDeniedException(f"Failed to find partner {partner_service.partner_id}")

        if not idempotency_key:
            raise BadRequestException("Missing Idempotency-Key")

        if idempotency_key_repo.idempotency_key_exists(UUID(idempotency_key)):
            raise ConflictException("Idempotency key already exists")
        idempotency_key_repo.add_idempotency_key(UUID(idempotency_key), "order_post")

        if order_post.sales_channel_id is not None:
            sales_channel = partner_service.get_sales_channels()
            for channel in sales_channel:
                if channel.name == order_post.sales_channel_id:
                    order_post.sales_channel_id = str(channel.fes_name)
                    break
            else:
                raise ValueError("Invalid sales channel id")

        all_brands = partner_service.get_branding()

        if order_post.brand_id and not any(brand.name == order_post.brand_id for brand in all_brands):
            raise ValueError(f"Brand {order_post.brand_id} not found")

        special_handlings_keys = SpecialHandlings._member_map_

        if order_post.fulfillment_options is not None:
            if order_post.fulfillment_options.special_handlings is not None:
                mapped_values = []
                for item in order_post.fulfillment_options.special_handlings:
                    if item not in special_handlings_keys:
                        raise ValueError(f"Invalid special_handling: {item}")
                    mapped_values.append(str(special_handlings_keys[item].value))

                order_post.fulfillment_options.special_handlings = mapped_values

            token = order_post.fulfillment_options.delivery_option_token
            if token and not is_valid_uuid(token):
                raise ValueError("Delivery option token is not valid")

        res = order_service.create_order(partner_service.partner_id, order_post)

        return paginate_response(
            items=order_post.recipes,
            base_url=str(f"{request.url}/{'order_post.order_id'}"),
            data_model=PostOrderData(order=res),
            list_attr_path="order.recipes",
        )

    except RecipeNotFoundError as e:
        raise UnprocessableException(str(e)) from None
    except RecipeAlreadyDeletedError as e:
        raise UnprocessableException(str(e)) from None
    except ServerError as e:
        raise InternalException(str(e)) from None
    except ValueError as e:
        raise BadRequestException(str(e)) from None


@router.patch(
    "/{orderId}",
    responses={
        400: {"model": ErrorResponse, "description": "Bad request"},
        401: {"model": ErrorResponse, "description": "Unauthorized"},
        422: {"model": ErrorResponse, "description": "Unprocessable Entity"},
        500: {"model": ErrorResponse, "description": "Internal Server Error"},
    },
)
def patch_order(
    request: Request,
    order_id: Annotated[UUID, Path(..., alias="orderId")],
    order_patch: OrderPatchRequest = order_body,
    partner_service: PartnerServiceInterface = Depends(get_partner_service),
    order_service: OrderServiceInterface = Depends(get_order_service),
) -> PaginatedResponse[PostOrderData]:
    try:
        set_logger_context_value("order_id", str(order_id))
        if not partner_service.validate_partner_id():
            raise AccessDeniedException(f"Failed to find partner {partner_service.partner_id}")

        if order_patch.sales_channel_id is not None:
            sales_channel = partner_service.get_sales_channels()
            for channel in sales_channel:
                if channel.name == order_patch.sales_channel_id:
                    order_patch.sales_channel_id = str(channel.fes_name)
                    break
            else:
                raise ValueError(f"Invalid sales channel id {order_patch.sales_channel_id} for PATCH order {order_id}")

        all_brands = partner_service.get_branding()

        if order_patch.brand_id and not any(brand.name == order_patch.brand_id for brand in all_brands):
            raise ValueError(f"Brand {order_patch.brand_id} not found")

        special_handlings_keys = SpecialHandlings._member_map_

        if order_patch.fulfillment_options is not None:
            if (
                order_patch.fulfillment_options.special_handlings is not None
                and len(order_patch.fulfillment_options.special_handlings) > 0
            ):
                mapped_values = []
                for item in order_patch.fulfillment_options.special_handlings:
                    if item not in special_handlings_keys:
                        raise ValueError(f"Invalid special_handling: {item}")
                    mapped_values.append(str(special_handlings_keys[item].value))

                order_patch.fulfillment_options.special_handlings = mapped_values

            token = order_patch.fulfillment_options.delivery_option_token
            if token and not is_valid_uuid(token):
                raise ValueError("Delivery option token is not valid")

        res = order_service.update_order(partner_service.partner_id, order_id, order_patch)

        return paginate_response(
            items=res.recipes,
            base_url=str(f"{request.url}"),
            data_model=PostOrderData(order=res),
            list_attr_path="order.recipes",
        )

    except RecipeNotFoundError as e:
        raise BadRequestException(str(e)) from None
    except RecipeAlreadyDeletedError as e:
        raise GoneException(str(e)) from None
    except ServerError as e:
        raise InternalException(str(e)) from None
    except ValueError as e:
        raise BadRequestException(str(e)) from None


@router.delete(
    "/{orderId}",
    status_code=204,
    responses={
        401: {"model": ErrorResponse, "description": "Unauthorized"},
        404: {"model": ErrorResponse, "description": "Not found"},
        500: {"model": ErrorResponse, "description": "Internal Server Error"},
    },
)
def delete_order(
    order_id: Annotated[UUID, Path(..., alias="orderId")],
    partner_service: PartnerServiceInterface = Depends(get_partner_service),
    order_service: OrderServiceInterface = Depends(get_order_service),
) -> None:
    try:
        set_logger_context_value("order_id", str(order_id))
        if not partner_service.validate_partner_id():
            raise AccessDeniedException(f"Failed to find partner {partner_service.partner_id}")

        order_service.delete_order(partner_service.partner_id, order_id)

    except OrderNotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e)) from None
    except ServerError as e:
        raise InternalException(str(e)) from None
