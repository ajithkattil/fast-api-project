from src.db.recipes_repo import RecipesRepo
from src.interfaces.recipes_repo_interface import RecipesRepoInterface


def get_recipes_db() -> RecipesRepoInterface:
    return RecipesRepo()
