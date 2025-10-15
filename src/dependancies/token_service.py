from fastapi import Depends

from src.dependancies.param_store_client import get_param_store_client
from src.interfaces.param_store_client_interface import ParamStoreClientInterface
from src.interfaces.token_service_interface import TokenServiceInterface
from src.services.token import TokenService


def get_token_service(
    param_store_client: ParamStoreClientInterface = Depends(get_param_store_client),
) -> TokenServiceInterface:
    return TokenService(param_store_client=param_store_client)
