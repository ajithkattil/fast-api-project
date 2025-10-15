from collections.abc import Callable
from typing import Any, ClassVar
from urllib.parse import urlparse

import jwt
import requests
from requests.exceptions import HTTPError
from requests.models import Response

from src.clients.culops.mocks.response_handlers.culinary_ingredient_specs import (
    get_culinary_ingredient_specifications_response_handler,
)
from src.clients.culops.mocks.response_handlers.recipes import patch_recipe_update_response_handler
from src.core.config import settings


class MockedSession(requests.Session):
    ROUTES: ClassVar[dict[str, dict[str, Callable]]] = {
        "/api/culinary-ingredient-specifications": {"GET": get_culinary_ingredient_specifications_response_handler},
        "/api/recipes/": {"PATCH": patch_recipe_update_response_handler},
    }

    CULOPS_API_HOST = settings.CULOPS_API_HOST

    def request(self, method: str, url: str, *args: Any, **kwargs: Any) -> Response:  # type: ignore[override]
        parsed = urlparse(url)
        params = kwargs.get("params", None)
        loc = parsed.netloc

        # Only intercept CulOps API calls, let all other requests pass through
        if loc != MockedSession.CULOPS_API_HOST:
            return super().request(method, url, *args, **kwargs)

        # Validate token only for CulOps API calls
        headers = kwargs.get("headers", None)
        if headers:
            self._validate_token(headers)

        path = parsed.path

        if path in MockedSession.ROUTES and method in MockedSession.ROUTES[path]:
            response_handler = MockedSession.ROUTES[path][method]
            res: Response = response_handler(headers, params)
            return res

        # Wildcard match: check for any registered prefix ending with '/'
        for route_prefix, methods in MockedSession.ROUTES.items():
            if path.startswith(route_prefix) and method in methods:
                response_handler = methods[method]

                # Use json body for PATCH/POST, else params
                if method in {"PATCH", "POST", "PUT"}:
                    body = kwargs.get("json", {})
                    res = response_handler(headers, body)
                else:
                    res = response_handler(headers, params)
                return res

        res = Response()
        res.status_code = 404
        res._content = b'{"error": "No mock route found."}'
        return res

    def _validate_token(self, headers: dict | None) -> None:
        if not headers or "Authorization" not in headers:
            res = Response()
            res.status_code = 401
            res._content = b'{"error": "Missing Authorization header"}'
            raise HTTPError("Missing Authorization header", response=res)

        token = headers["Authorization"].replace("Bearer ", "")
        try:
            jwt.decode(token, options={"verify_signature": False})
        except jwt.DecodeError:
            res = Response()
            res.status_code = 403
            res._content = b'{"error": "Invalid JWT token"}'
            raise HTTPError("Invalid JWT token.", response=res) from None
