from fastapi import APIRouter, Depends, HTTPException, Request
from pydantic import BaseModel, Field
from datetime import datetime

from src.api.routes.v1.models import ErrorResponse, GetPantry
from src.core.config import Settings
from src.core.exceptions import NotFoundException
from src.core.middleware.partner_id_middleware import partner_id_ctx
from src.dependancies.culops_client import get_culops_client
from src.dependancies.pantry_db import get_pantry_db
from src.dependancies.partner_db import get_partner_db
from src.dependancies.recipe_db import get_recipes_db
from src.dependancies.token_service import get_token_service
from src.interfaces.culops_client_interface import CulopsClientInterface
from src.interfaces.pantry_db_interface import PantryDBInterface
from src.interfaces.partner_repo_interface import PartnerRepoInterface
from src.interfaces.recipes_repo_interface import RecipesRepoInterface
from src.interfaces.token_service_interface import TokenServiceInterface
from src.services.pantry import PantryService
from src.services.partner import PartnerService
from src.utils.paginator import PaginatedResponse, paginate_response

router = APIRouter(
    prefix="/pantry",
    responses={
        422: {"model": ErrorResponse, "description": "Unprocessable Entity"},
    },
)

settings = Settings()


class PantryQueryParams(BaseModel):
    page: int = Field(default=1, ge=1)
    page_size: int = Field(default=settings.DEFAULT_PAGE_SIZE, alias="pageSize", ge=1, le=settings.MAX_PAGE_SIZE)
    available_from: datetime | None = Field(default=None, alias="availableFrom")
    available_until: datetime | None = Field(default=None, alias="availableUntil")
    cost_start_date: datetime | None = Field(default=None, alias="costStartDate")
    cost_end_date: datetime | None = Field(default=None, alias="costEndDate")
    pantry_state_id: str = Field(default="", alias="pantryStateId")
    brand: str = Field(default="")


@router.get(
    "",
    responses={
        400: {"model": ErrorResponse, "description": "Bad request"},
        401: {"model": ErrorResponse, "description": "Unauthorized"},
        404: {"model": ErrorResponse, "description": "Not found"},
        500: {"model": ErrorResponse, "description": "Internal Server Error"},
    },
)
def get_pantry(
    request: Request,
    params: PantryQueryParams = Depends(),
    pantry_db: PantryDBInterface = Depends(get_pantry_db),
    partner_db: PartnerRepoInterface = Depends(get_partner_db),
    recipe_db: RecipesRepoInterface = Depends(get_recipes_db),
    token_svc: TokenServiceInterface = Depends(get_token_service),
    culops_client: CulopsClientInterface = Depends(get_culops_client),
) -> PaginatedResponse[GetPantry]:
    try:
        partner_id = partner_id_ctx.get()
        partner_service = PartnerService(partner_id=partner_id or "", partner_db=partner_db)
        # TODO uncomment below, commented out for staging testing while db migrations are broken
        # if not partner_service.validate_partner_id():
        #     raise AccessDeniedException(f"Failed to find partner {partner_id}")

        pantry_service = PantryService(
            pantry_db=pantry_db, culops_service=culops_client, partner_service=partner_service
        )
        all_brands = partner_service.get_branding()

        if params.brand and not any(brand.name == params.brand for brand in all_brands):
            raise NotFoundException(f"Brand {params.brand} not found")

        pantry, item_count = pantry_service.get_pantry(
            partner_id=partner_id or "",
            pantry_state_id=params.pantry_state_id,
            available_from=params.available_from,
            available_until=params.available_until,
            cost_start_date=params.cost_start_date,
            cost_end_date=params.cost_end_date,
            brand_name=params.brand or "",
            page_size=params.page_size,
            page=params.page,
        )

        return paginate_response(
            items=pantry.pantry_items,
            item_count=item_count,
            page=params.page,
            page_size=params.page_size,
            base_url=str(request.url).split("?")[0],
            url_params={
                "availableFrom": pantry.ingredients_available_from,
                "availableUntil": pantry.ingredients_available_until,
                "pageSize": str(params.page_size),
                "pantryStateId": pantry.pantry_state_id,
            },
            data_model=GetPantry(pantry=pantry),
            list_attr_path="pantry.pantry_items",
        )

    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e)) from None
