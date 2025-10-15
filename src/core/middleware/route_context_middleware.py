from collections.abc import Callable

from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.routing import Match

from src.utils.logger_context import set_logger_context_value


class RouteContextMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        try:
            router = request.app.router
            for route in getattr(router, "routes", []):
                match, child_scope = route.matches(request.scope)
                if match == Match.FULL:
                    for key, value in child_scope.get("path_params", {}).items():
                        set_logger_context_value(key, value)
                    break
        except Exception:
            pass

        response = await call_next(request)
        return response
