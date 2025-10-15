"""Rollbar middleware for FastAPI applications."""

from collections.abc import Callable

from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware

from src.core.config import settings


class RollbarMiddleware(BaseHTTPMiddleware):
    """Middleware to automatically report exceptions to Rollbar with request context."""

    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        if not settings.ROLLBAR_SERVER_TOKEN:
            return await call_next(request)

        try:
            import rollbar
        except ImportError:
            return await call_next(request)

        try:
            response = await call_next(request)
            return response

        except Exception as exc:
            partner_id = getattr(request.state, "partner_id", None)
            user_id = getattr(request.state, "user_id", None)

            # Get authorization header if present
            auth_header = request.headers.get("authorization", "")

            extra_data = {
                "request": {
                    "url": str(request.url),
                    "method": request.method,
                    "headers": dict(request.headers),
                    "path_params": request.path_params,
                    "query_params": dict(request.query_params),
                    "client": {
                        "host": request.client.host if request.client else None,
                        "port": request.client.port if request.client else None,
                    }
                    if request.client
                    else None,
                },
                "partner_id": partner_id,
                "user_id": user_id,
                "authorization": auth_header,
            }

            rollbar.report_exc_info(extra_data=extra_data)
            raise exc
