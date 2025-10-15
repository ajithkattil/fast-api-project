from contextvars import ContextVar

import jwt
from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint

from src.core.exceptions import AccessDeniedException
from src.utils.logger import ServiceLogger
from src.utils.logger_context import set_logger_context_value

partner_id_ctx: ContextVar[str | None] = ContextVar("partner_id", default=None)

logger = ServiceLogger().get_logger(__name__)


def _extract_partner_id_from_auth_header(auth_header: str | None) -> str | None:
    try:
        if not auth_header:
            return None
        parts = auth_header.split()
        if len(parts) != 2:
            return None
        token = parts[1]
        payload = jwt.decode(token, options={"verify_signature": False, "verify_exp": False})
        logger.info(f"payload: {payload}")
        value = payload.get("custom:partner_id")
        if isinstance(value, str) and value:
            return value
        return None
    except Exception:
        return None


class PartnerIDMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next: RequestResponseEndpoint) -> Response:
        if request.url.path == "/health":
            return await call_next(request)

        if request.method == "OPTIONS":
            return await call_next(request)
        logger.info(f"headers: {request.headers}")

        auth_header = request.headers.get("Authorization")
        partner_id = _extract_partner_id_from_auth_header(auth_header)
        if not partner_id:
            raise AccessDeniedException("No partner ID found in access token")
        token = partner_id_ctx.set(partner_id)
        set_logger_context_value("partner_id", partner_id)

        try:
            response = await call_next(request)
        finally:
            partner_id_ctx.reset(token)
        return response
