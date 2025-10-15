from src.clients.param_store.client import ParamStoreClient


def get_param_store_client() -> ParamStoreClient:
    return ParamStoreClient()
