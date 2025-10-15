from fastapi import APIRouter

from src.api.routes.v1.recipes.recipe_elements.pantry import routes as pantry_routes

router = APIRouter(prefix="/recipeelements")

router.include_router(pantry_routes.router)
