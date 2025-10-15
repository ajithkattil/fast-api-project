from fastapi import Depends

from src.dependancies.culops_client import get_culops_client
from src.dependancies.fulfillment_client import get_fulfillment_client
from src.dependancies.fulfillment_producer import get_fulfillment_producer
from src.dependancies.fulfillment_response_producer import get_fulfillment_response_producer
from src.dependancies.pantry_db import get_pantry_db
from src.dependancies.partner_db import get_partner_db
from src.dependancies.recipe_db import get_recipes_db
from src.interfaces.culops_client_interface import CulopsClientInterface
from src.interfaces.fulfillment_engine_client_interface import FulfillmentEngineClientInterface
from src.interfaces.fulfillment_producer_interface import FulfillmentProducerInterface
from src.interfaces.fulfillment_response_producer_interface import FulfillmentResponseProducerInterface
from src.interfaces.order_service_interface import OrderServiceInterface
from src.interfaces.pantry_db_interface import PantryDBInterface
from src.interfaces.partner_repo_interface import PartnerRepoInterface
from src.interfaces.recipes_repo_interface import RecipesRepoInterface
from src.services.order import OrderService


def get_order_service(
    partner_repo: PartnerRepoInterface = Depends(get_partner_db),
    pantry_repo: PantryDBInterface = Depends(get_pantry_db),
    culops_client: CulopsClientInterface = Depends(get_culops_client),
    fulfillment_client: FulfillmentEngineClientInterface = Depends(get_fulfillment_client),
    fulfillment_producer: FulfillmentProducerInterface = Depends(get_fulfillment_producer),
    fulfillment_response_producer: FulfillmentResponseProducerInterface = Depends(get_fulfillment_response_producer),
    recipes_repo: RecipesRepoInterface = Depends(get_recipes_db),
) -> OrderServiceInterface:
    return OrderService(
        partner_repo=partner_repo,
        pantry_repo=pantry_repo,
        culops_client=culops_client,
        fulfillment_client=fulfillment_client,
        fulfillment_producer=fulfillment_producer,
        fulfillment_response_producer=fulfillment_response_producer,
        recipes_repo=recipes_repo,
    )
