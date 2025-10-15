import jwt
from datetime import UTC, datetime

from src.clients.connect.client import ConnectClient
from src.clients.param_store.client import ParamStoreClient
from src.core.config import settings
from src.core.exceptions import ServerError
from src.token_manager.models import Param
from src.utils.logger import ServiceLogger

logger = ServiceLogger().get_logger(__name__)


class TokenManagerService:
    def __init__(self, param_store_client: ParamStoreClient, connect_client: ConnectClient):
        self._param_store_client = param_store_client
        self._connect_client = connect_client
        self._deploy_env = settings.DEPLOY_ENV
        self._param_base_path = settings.SERVICE_PARAMS_BASE_PATH
        self._token_param_names = [settings.CUL_OPS_ACCESS_TOKEN_PARAM_NAME, settings.CUL_OPS_REFRESH_TOKEN_PARAM_NAME]
        self._access_token_param_name = f"/{self._deploy_env}/{self._param_base_path}/{settings.CUL_OPS_ACCESS_TOKEN_PARAM_NAME}"
        self._refresh_token_param_name = f"/{self._deploy_env}/{self._param_base_path}/{settings.CUL_OPS_REFRESH_TOKEN_PARAM_NAME}"
        self._connect_client_id = settings.CONNECT_CLIENT_ID
        self._connect_client_secret = settings.CONNECT_CLIENT_SECRET

    def refresh_token(self) -> None:
        logger.info("Starting token refresh process")
        
        param_names = [self._access_token_param_name, self._refresh_token_param_name]
        try:
            params = self._param_store_client.get_params(param_names)
        except ServerError as e:
            logger.error("Failed to get token parameters from Parameter Store: %s", str(e))
            raise ServerError(
                f"Failed to get CulOps token parameters {param_names} from Parameter Store"
            ) from e
        except ValueError as e:
            logger.error("Invalid token parameters: %s", str(e))
            raise ServerError("Missing or invalid CulOps token parameters") from e

        access_token = next((p for p in params if p.name == self._access_token_param_name), None)
        refresh_token = next((p for p in params if p.name == self._refresh_token_param_name), None)

        if not access_token or not refresh_token:
            logger.error("Missing access_token or refresh_token in Parameter Store response")
            raise ServerError("Missing or invalid CulOps tokens")

        # Log current token expiry
        try:
            old_token_obj = jwt.decode(
                access_token.value, options={"verify_signature": False, "verify_exp": False}
            )
            old_exp = old_token_obj.get("exp")
            if old_exp:
                old_remaining = int(old_exp) - int(datetime.now(UTC).timestamp())
                logger.info(
                    "Current token expiry info",
                    extra={
                        "remaining_seconds": old_remaining,
                        "expired": old_remaining <= 0,
                        "expires_at": datetime.fromtimestamp(old_exp, UTC).isoformat()
                    }
                )
        except (jwt.DecodeError, KeyError, ValueError, TypeError) as e:
            logger.warning("Could not parse old token expiry: %s", str(e))

        try:
            logger.info("Calling Connect API to refresh token")
            token_response = self._connect_client.refresh_token(
                refresh_token.value, self._connect_client_id, self._connect_client_secret
            )
            logger.info(
                "Token refresh successful from Connect API",
                extra={
                    "expires_in_seconds": token_response.expires_in,
                    "token_type": token_response.token_type
                }
            )
        except (ServerError, ValueError) as e:
            logger.error("Failed to refresh token from Connect API: %s", str(e))
            raise ServerError("Failed to refresh CulOps token") from e

        # Log new token expiry
        try:
            new_token_obj = jwt.decode(
                token_response.access_token, options={"verify_signature": False, "verify_exp": False}
            )
            new_exp = new_token_obj.get("exp")
            if new_exp:
                new_remaining = int(new_exp) - int(datetime.now(UTC).timestamp())
                logger.info(
                    "New token expiry info",
                    extra={
                        "remaining_seconds": new_remaining,
                        "expires_at": datetime.fromtimestamp(new_exp, UTC).isoformat(),
                        "response_expires_in": token_response.expires_in
                    }
                )
        except (jwt.DecodeError, KeyError, ValueError, TypeError) as e:
            logger.warning("Could not parse new token expiry: %s", str(e))

        try:
            logger.info("Storing new tokens in Parameter Store")
            self._param_store_client.store_param(
                Param(name=self._access_token_param_name, value=token_response.access_token)
            )
            self._param_store_client.store_param(
                Param(name=self._refresh_token_param_name, value=token_response.refresh_token)
            )
            logger.info("Successfully stored new tokens in Parameter Store")
        except ServerError as e:
            logger.error("Failed to store tokens in Parameter Store: %s", str(e))
            raise ServerError(
                f"Failed to store CulOps token parameters {self._token_param_names} in Parameter Store"
            ) from e
        
        logger.info("Token refresh process completed successfully")
