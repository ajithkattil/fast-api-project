import json

import requests
from pydantic import ValidationError
from requests import HTTPError, RequestException
from requests.adapters import HTTPAdapter
from urllib3 import Retry

from src.core.config import settings
from src.core.exceptions import ServerError
from src.token_manager.models import TokenResponse
from src.utils.logger import ServiceLogger

logger = ServiceLogger().get_logger(__name__)


class ConnectClient:
    def __init__(self) -> None:
        self.token_url = f"https://connect.{settings.DEPLOY_ENV}.f--r.co/oauth/token"
        session = requests.Session()

        retry = Retry(
            total=settings.CONNECT_RETRY_COUNT,
            backoff_factor=0.5,  # ~0.5s, 1s, 2s, 4s
            status_forcelist=(429, 500, 502, 503, 504),
            allowed_methods=frozenset(["POST"]),
            raise_on_status=False,
            respect_retry_after_header=True,
        )

        adapter = HTTPAdapter(max_retries=retry)
        session.mount("https://", adapter)
        session.mount("http://", adapter)
        self.session = session

    def refresh_token(self, refresh_token: str, client_id: str, client_secret: str) -> TokenResponse:
        # Note: OAuth 2.0 refresh token flow typically doesn't require the access token in Authorization header
        # The refresh_token in the form body is sufficient for authentication
        headers = {
            "Content-Type": "application/x-www-form-urlencoded",
        }

        form = {
            "grant_type": "refresh_token",
            "refresh_token": refresh_token,
            "client_id": client_id,
            "client_secret": client_secret,
        }

        try:
            response = self.session.post(self.token_url, headers=headers, data=form)
            response.raise_for_status()
            token_response = TokenResponse.model_validate(response.json())
            return token_response

        except ValidationError as e:
            try:
                response_json = response.json()
                res_keys = list(response_json.keys())
            except json.JSONDecodeError:
                res_keys = []
            if res_keys:
                exp_str = f" Response keys: {res_keys}"
            else:
                exp_str = ""
            raise ValueError(f"Failed to refresh Connect token. Response format not expected.{exp_str}") from e
        except (HTTPError, RequestException) as e:
            raise ServerError("Failed to refresh Connect token") from e
