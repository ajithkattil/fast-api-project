from fastapi import Depends

from src.dependancies.cabinet_client import get_cabinet_client
from src.dependancies.culops_client import get_culops_client
from src.dependancies.pantry_db import get_pantry_db
from src.dependancies.partner_db import get_partner_db
from src.dependancies.recipe_db import get_recipes_db
from src.interfaces.cabinet_client_interface import CabinetClientInterface
from src.interfaces.culops_client_interface import CulopsClientInterface
from src.interfaces.pantry_db_interface import PantryDBInterface
from src.interfaces.partner_repo_interface import PartnerRepoInterface
from src.interfaces.recipe_service_interface import RecipeServiceInterface
from src.interfaces.recipes_repo_interface import RecipesRepoInterface
from src.services.recipe import RecipeService


def get_recipe_service(
    partner_repo: PartnerRepoInterface = Depends(get_partner_db),
    pantry_repo: PantryDBInterface = Depends(get_pantry_db),
    recipes_repo: RecipesRepoInterface = Depends(get_recipes_db),
    culops_client: CulopsClientInterface = Depends(get_culops_client),
    cabinet_client: CabinetClientInterface = Depends(get_cabinet_client),
) -> RecipeServiceInterface:
    return RecipeService(
        partner_repo=partner_repo,
        pantry_repo=pantry_repo,
        recipes_repo=recipes_repo,
        culops_client=culops_client,
        cabinet_client=cabinet_client,
    )
