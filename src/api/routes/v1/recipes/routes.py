from typing import Annotated, TypeVar
from uuid import UUID

from fastapi import APIRouter, Body, Depends, Header, HTTPException, Path, Query, Request
from pydantic import BaseModel, Field

from src.api.routes.v1.models import (
    ErrorResponse,
    GetRecipesData,
    PostRecipeData,
    RecipePatchRequest,
    RecipePostRequest,
)
from src.api.routes.v1.recipes.recipe_elements import routes as recipe_elements_routes
from src.core.config import Settings
from src.core.exceptions import (
    AccessDeniedException,
    BadRequestException,
    ConflictException,
    GoneException,
    InternalException,
    NotFoundException,
    RecipeAlreadyDeletedError,
    RecipeNotFoundError,
    ServerError,
    UnprocessableException,
)
from src.dependancies.idempotency_db import get_idempotency_db
from src.dependancies.partner_service import get_partner_service
from src.dependancies.recipe_service import get_recipe_service
from src.interfaces.idempotency_key_repo_interface import IdempotencyKeyRepoInterface
from src.interfaces.partner_service_interface import PartnerServiceInterface
from src.interfaces.recipe_service_interface import RecipeServiceInterface
from src.utils.paginator import PaginatedResponse, paginate_response
from src.utils.validation import validate_cycle_date

router = APIRouter(
    prefix="/v1/recipes",
    responses={
        422: {"model": ErrorResponse, "description": "Unprocessable Entity"},
    },
)

router.include_router(recipe_elements_routes.router)

settings = Settings()


class RecipeGetCycleDateQueryParams(BaseModel):
    page: int = Field(default=1, ge=1)
    page_size: int = Field(default=settings.DEFAULT_PAGE_SIZE, alias="pageSize", ge=1, le=settings.MAX_PAGE_SIZE)
    recipe_ids: str | None = Field(alias="recipeIds", default=None)


T = TypeVar("T", bound=BaseModel)


class RecipeGetQueryParams(BaseModel):
    product_skus: str | None = Field(alias="product-skus", default=None)
    return_options: str | None = Field(alias="return-options", default="recipe-id-sku-mapping")
    page: int = Field(default=1, ge=1)
    page_size: int = Field(default=settings.DEFAULT_PAGE_SIZE, alias="pageSize", ge=1, le=settings.MAX_PAGE_SIZE)


@router.get(
    "",
    responses={
        400: {"model": ErrorResponse, "description": "Bad request"},
        401: {"model": ErrorResponse, "description": "Unauthorized"},
        404: {"model": ErrorResponse, "description": "Not found"},
        422: {"model": ErrorResponse, "description": "Unprocessable Entity"},
    },
)
def get_recipes(
    request: Request,
    params: RecipeGetQueryParams = Depends(),
    recipe_service: RecipeServiceInterface = Depends(get_recipe_service),
    partner_service: PartnerServiceInterface = Depends(get_partner_service),
) -> list[T] | PaginatedResponse[GetRecipesData]:
    try:
        if not partner_service.validate_partner_id():
            raise AccessDeniedException(f"Failed to find partner {partner_service.partner_id}")

        # If product-skus provided, return SKU mapping
        if params.product_skus:
            product_sku_list = params.product_skus.split(",")
            match params.return_options:
                case "recipe-id-sku-mapping":
                    res: list[T] = recipe_service.get_recipe_ids_by_skus(
                        partner_id=partner_service.partner_id, product_skus=product_sku_list
                    )
                    if not res:
                        raise NotFoundException(f"Failed to find recipes for SKUs {params.product_skus}")
                    return res
                case _:
                    raise ServerError(f"Unknown return option: {params.return_options}")

        # Otherwise return all recipes for partner (no cycle date filter)
        res = recipe_service.get_all_recipes(partner_id=partner_service.partner_id) or []

        if not res:
            raise NotFoundException(f"Failed to find recipes for partner {partner_service.partner_id}")

        return paginate_response(
            items=res,
            page=params.page,
            page_size=params.page_size,
            base_url=str(request.url).split("?")[0],
            url_params={},
            data_model=GetRecipesData(recipes=res),
            list_attr_path="recipes",
        )

    except ServerError as e:
        raise UnprocessableException(str(e)) from e


@router.get(
    "/{cycleDate}",
    responses={
        401: {"model": ErrorResponse, "description": "Unauthorized"},
        404: {"model": ErrorResponse, "description": "Not found"},
        410: {"model": ErrorResponse, "description": "Gone"},
        500: {"model": ErrorResponse, "description": "Internal Server Error"},
    },
)
def get_recipes_by_cycle_date(
    request: Request,
    cycle_date: Annotated[str, Path(..., alias="cycleDate")],
    params: RecipeGetCycleDateQueryParams = Depends(),
    partner_service: PartnerServiceInterface = Depends(get_partner_service),
    recipe_service: RecipeServiceInterface = Depends(get_recipe_service),
) -> PaginatedResponse[GetRecipesData]:
    try:
        if not partner_service.validate_partner_id():
            raise AccessDeniedException(f"Failed to find partner {partner_service.partner_id}")

        validated_cycle_date = validate_cycle_date(cycle_date)

        res = (
            recipe_service.get_recipes(
                partner_id=partner_service.partner_id,
                cycle_date=validated_cycle_date,
                recipe_ids=params.recipe_ids.split(",") if params.recipe_ids else None,
            )
            or []
        )
        if not res:
            raise NotFoundException(f"Failed to find recipes in cycle date {validated_cycle_date}")

        return paginate_response(
            items=res,
            page=params.page,
            page_size=params.page_size,
            base_url=str(request.url),
            url_params={
                "recipe_ids": params.recipe_ids or "",
            },
            data_model=GetRecipesData(recipes=res),
            list_attr_path="recipes",
        )

    except ValueError as e:
        if isinstance(e, RecipeAlreadyDeletedError):
            raise GoneException(str(e)) from None
        elif isinstance(e, RecipeNotFoundError):
            raise NotFoundException(str(e)) from None
        else:
            raise BadRequestException(str(e)) from None


recipe_body = Body(...)


@router.post(
    "",
    status_code=201,
    responses={
        400: {"model": ErrorResponse, "description": "Bad request"},
        401: {"model": ErrorResponse, "description": "Unauthorized"},
        409: {"model": ErrorResponse, "description": "Conflict"},
        422: {"model": ErrorResponse, "description": "Unprocessable Entity"},
        500: {"model": ErrorResponse, "description": "Internal Server Error"},
    },
)
def post_recipe(
    request: Request,
    idempotency_key: Annotated[str, Header(..., alias="Idempotency-Key")],
    recipe_post: RecipePostRequest = recipe_body,
    partner_service: PartnerServiceInterface = Depends(get_partner_service),
    idempotency_key_repo: IdempotencyKeyRepoInterface = Depends(get_idempotency_db),
    recipe_service: RecipeServiceInterface = Depends(get_recipe_service),
) -> PaginatedResponse[PostRecipeData]:
    try:
        if not partner_service.validate_partner_id():
            raise AccessDeniedException(f"Failed to find partner {partner_service.partner_id}")

        if idempotency_key_repo.idempotency_key_exists(UUID(idempotency_key)):
            raise ConflictException("Idempotency key already exists")

        if recipe_post.recipe_tags and not partner_service.validate_tags(recipe_post.recipe_tags):
            raise BadRequestException("Invalid recipe tags")

        res = recipe_service.create_recipe(partner_service.partner_id, recipe_post)

        idempotency_key_repo.add_idempotency_key(UUID(idempotency_key), "recipe_post")

        return paginate_response(
            items=res.ingredients,
            base_url=str(f"{request.url}/{res.recipe_id}"),
            data_model=PostRecipeData(recipe=res),
            list_attr_path="recipe.ingredients",
        )

    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e)) from None


@router.patch(
    "/{recipeId}",
    responses={
        400: {"model": ErrorResponse, "description": "Bad request"},
        401: {"model": ErrorResponse, "description": "Unauthorized"},
        404: {"model": ErrorResponse, "description": "Not found"},
        410: {"model": ErrorResponse, "description": "Gone"},
        422: {"model": ErrorResponse, "description": "Unprocessable Entity"},
        500: {"model": ErrorResponse, "description": "Internal Server Error"},
    },
)
def patch_recipe(
    request: Request,
    recipe_id: Annotated[str, Path(..., alias="recipeId")],
    recipe_patch: RecipePatchRequest = recipe_body,
    partner_service: PartnerServiceInterface = Depends(get_partner_service),
    recipe_service: RecipeServiceInterface = Depends(get_recipe_service),
) -> PaginatedResponse[PostRecipeData]:
    try:
        if not partner_service.validate_partner_id():
            raise AccessDeniedException(f"Failed to find partner {partner_service.partner_id}")

        if recipe_patch.recipe_tags and not partner_service.validate_tags(recipe_patch.recipe_tags):
            raise BadRequestException("Invalid recipe tags")

        if not recipe_patch.model_dump(exclude_unset=True):
            raise BadRequestException("At least one updatable field must be provided.")

        res = recipe_service.update_recipe(partner_service.partner_id, recipe_id, recipe_patch)
        if res is None:
            raise NotFoundException(f"Failed to update recipe {recipe_id}")

        return paginate_response(
            items=res.ingredients,
            base_url=str(f"{request.url}/{res.recipe_id}"),
            data_model=PostRecipeData(recipe=res),
            list_attr_path="recipe.ingredients",
        )

    except RecipeNotFoundError as e:
        raise NotFoundException(str(e)) from e
    except RecipeAlreadyDeletedError as e:
        raise GoneException(str(e)) from e
    except ServerError as e:
        raise InternalException(str(e)) from e
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e)) from e


@router.delete(
    "/{recipeId}",
    status_code=204,
    responses={
        400: {"model": ErrorResponse, "description": "Bad request"},
        401: {"model": ErrorResponse, "description": "Unauthorized"},
        404: {"model": ErrorResponse, "description": "Not found"},
        410: {"model": ErrorResponse, "description": "Gone"},
        500: {"model": ErrorResponse, "description": "Internal Server Error"},
    },
)
def delete_recipe(
    recipe_id: Annotated[str, Path(..., alias="recipeId")],
    partner_service: PartnerServiceInterface = Depends(get_partner_service),
    recipe_service: RecipeServiceInterface = Depends(get_recipe_service),
) -> None:
    try:
        if not partner_service.validate_partner_id():
            raise AccessDeniedException(f"Failed to find partner {partner_service.partner_id}")

        recipe_service.delete_recipe(partner_service.partner_id, recipe_id)

    except RecipeNotFoundError as e:
        raise NotFoundException(str(e)) from e
    except RecipeAlreadyDeletedError as e:
        raise GoneException(str(e)) from e
    except ServerError as e:
        raise InternalException(str(e)) from e
    except ValueError as e:
        raise BadRequestException(str(e)) from e
