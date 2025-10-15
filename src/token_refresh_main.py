import sys

from src.clients.connect.client import ConnectClient
from src.clients.param_store.client import ParamStoreClient
from src.core.exceptions import ServerError
from src.token_manager.service import TokenManagerService
from src.utils.logger import ServiceLogger

logger = ServiceLogger().get_logger(__name__)


def main() -> None:
    try:
        logger.info("Starting CulOps token refresh process")

        param_store_client = ParamStoreClient()
        connect_client = ConnectClient()
        token_manager = TokenManagerService(param_store_client, connect_client)
        token_manager.refresh_token()

        logger.info("CulOps token refresh completed successfully")
        sys.exit(0)

    except ServerError:
        logger.exception("Token refresh process failed")
        sys.exit(1)

    except Exception:
        logger.exception("Token refresh process failed with unexpected error")
        sys.exit(1)


if __name__ == "__main__":
    main()
