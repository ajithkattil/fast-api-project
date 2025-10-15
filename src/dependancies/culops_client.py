from fastapi import Depends

from src.clients.culops.culops import CulOpsService
from src.dependancies.pantry_db import get_pantry_db
from src.dependancies.partner_db import get_partner_db
from src.dependancies.recipe_db import get_recipes_db
from src.dependancies.token_service import get_token_service
from src.interfaces.culops_client_interface import CulopsClientInterface
from src.interfaces.pantry_db_interface import PantryDBInterface
from src.interfaces.partner_repo_interface import PartnerRepoInterface
from src.interfaces.recipes_repo_interface import RecipesRepoInterface
from src.interfaces.token_service_interface import TokenServiceInterface


def get_culops_client(
    partner_repo: PartnerRepoInterface = Depends(get_partner_db),
    recipe_repo: RecipesRepoInterface = Depends(get_recipes_db),
    pantry_repo: PantryDBInterface = Depends(get_pantry_db),
    token_svc: TokenServiceInterface = Depends(get_token_service),
) -> CulopsClientInterface:
    return CulOpsService(
        partner_repo=partner_repo, recipe_repo=recipe_repo, pantry_repo=pantry_repo, token_svc=token_svc
    )
