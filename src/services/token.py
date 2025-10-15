import os
from datetime import UTC, datetime
from enum import Enum
from threading import RLock
from typing import Any, ClassVar

import jwt
from jwt import InvalidTokenError

from src.core.config import settings
from src.core.exceptions import ServerError
from src.interfaces.param_store_client_interface import ParamStoreClientInterface
from src.utils.logger import ServiceLogger

logger = ServiceLogger().get_logger(__name__)


class TokenName(Enum):
    CUL_OPS_ACCESS_TOKEN = settings.CUL_OPS_ACCESS_TOKEN_PARAM_NAME


class TokenService:
    _instance: ClassVar["TokenService | None"] = None

    def __new__(cls, *args: Any, **kwargs: Any) -> "TokenService":
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self, param_store_client: ParamStoreClientInterface):
        if not hasattr(self, "_initialized"):
            self._initialized = True
            self._param_store_client = param_store_client
            self._token_cache: dict[TokenName, str] = {}
            self._lock: RLock = RLock()
            self.token_expiry_buffer = settings.TOKEN_EXPIRY_BUFFER

    def get_token(self, token_name: TokenName) -> str:
        token = self._token_cache.get(token_name)
        if token and self._token_is_valid(token):
            logger.debug("Using cached token for %s", token_name.value)
            return token
        
        with self._lock:
            token = self._token_cache.get(token_name)
            if token and self._token_is_valid(token):
                logger.debug("Using cached token for %s (double-checked)", token_name.value)
                return token
            
            logger.info(
                "Token %s is invalid or expired, fetching fresh token from Parameter Store",
                token_name.value,
                extra={"token_name": token_name.value, "had_cached_token": token is not None}
            )
            try:
                token = self._fetch_token(token_name)
                self._token_cache[token_name] = token
                logger.info("Successfully fetched and cached fresh token for %s", token_name.value)
            except (ServerError, ValueError) as e:
                logger.error(
                    "Failed to fetch token %s",
                    token_name.value,
                    extra={"token_name": token_name.value, "error": str(e)}
                )
                raise ServerError(f"Failed to fetch and cache token {token_name.value}") from e
            return token

    def _fetch_token(self, token_name: TokenName) -> str:
        # Construct SSM parameter path
        param_path = f"/{settings.DEPLOY_ENV}/{settings.SERVICE_PARAMS_BASE_PATH}/{token_name.value}"
        
        try:
            # Fetch directly from SSM Parameter Store
            params = self._param_store_client.get_params([param_path])
            if not params:
                raise ValueError(f"Token {token_name.value} not found in Parameter Store at {param_path}")
            return params[0].value
        except (ServerError, ValueError) as e:
            # Fallback to environment variable for backward compatibility
            token = os.getenv(token_name.value)
            if token:
                return token
            raise ValueError(f"Token {token_name.value} not found in Parameter Store or environment") from e

    def _token_is_valid(self, token: str | None) -> bool:
        if not token:
            return False

        try:
            token_obj = jwt.decode(
                token, options={"verify_signature": False, "require": ["exp", "iat"], "verify_exp": False}
            )
            remaining = int(token_obj["exp"]) - int(datetime.now(UTC).timestamp())

            # Log token expiry info
            if remaining <= self.token_expiry_buffer:
                logger.warning(
                    "Token expires soon or has expired",
                    extra={
                        "remaining_seconds": remaining,
                        "expiry_buffer_seconds": self.token_expiry_buffer,
                        "token_expired": remaining <= 0,
                        "within_buffer": 0 < remaining <= self.token_expiry_buffer
                    }
                )
                return False
            else:
                logger.debug(
                    "Token is valid",
                    extra={
                        "remaining_seconds": remaining,
                        "expiry_buffer_seconds": self.token_expiry_buffer
                    }
                )
                return True

        except InvalidTokenError as e:
            logger.warning(
                "Token validation failed - token is not a valid JWT",
                extra={
                    "error": str(e),
                    "error_type": type(e).__name__
                }
            )
            return False
