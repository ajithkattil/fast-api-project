from fastapi import APIRouter

from src.api import health
from src.api.routes.v1.orders import routes as order
from src.api.routes.v1.recipes import routes as recipe

api_router = APIRouter()

api_router.include_router(health.router)

api_router.include_router(recipe.router)

api_router.include_router(order.router)
