from src.clients.fulfillment_engine.client import FulfillmentEngineClient
from src.interfaces.fulfillment_engine_client_interface import FulfillmentEngineClientInterface


def get_fulfillment_client() -> FulfillmentEngineClientInterface:
    return FulfillmentEngineClient()
