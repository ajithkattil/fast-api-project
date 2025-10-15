from collections.abc import Awaitable, Callable
from typing import Any

from fastapi import FastAPI, HTTPException, Request, Response
from fastapi.responses import JSONResponse
from fastapi.testclient import TestClient
from httpx import Response as HTTPXResponse
from starlette.middleware.base import BaseHTTPMiddleware

from src.core.middleware.partner_id_middleware import PartnerIDMiddleware, partner_id_ctx
from tests.conftest import encode_jwt


class CatchExceptionsMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next: Callable[[Request], Awaitable[Any]]) -> Response:
        try:
            return await call_next(request)
        except HTTPException as exc:
            return JSONResponse(status_code=exc.status_code, content={"detail": exc.detail})


def _build_app() -> TestClient:
    app = FastAPI()

    @app.get("/health")
    def health() -> dict[str, bool]:
        return {"ok": True}

    @app.get("/ping")
    def ping() -> dict[str, Any | None]:
        return {"partner_id": partner_id_ctx.get()}

    app.add_middleware(PartnerIDMiddleware)
    app.add_middleware(CatchExceptionsMiddleware)
    return TestClient(app, raise_server_exceptions=False)


def test_dispatch_authorization_uppercase_header_success() -> None:
    client = _build_app()
    token = encode_jwt({"custom:partner_id": "BA-MAIN"})
    resp: HTTPXResponse = client.get("/ping", headers={"Authorization": f"Bearer {token}"})
    assert resp.status_code == 200
    assert resp.json()["partner_id"] == "BA-MAIN"


def test_dispatch_authorization_lowercase_header_success() -> None:
    client = _build_app()
    token = encode_jwt({"custom:partner_id": "BA-MAIN"})
    resp: HTTPXResponse = client.get("/ping", headers={"authorization": f"Bearer {token}"})
    assert resp.status_code == 200
    assert resp.json()["partner_id"] == "BA-MAIN"


def test_dispatch_health_bypasses_partner_check() -> None:
    client = _build_app()
    resp: HTTPXResponse = client.get("/health")
    assert resp.status_code == 200
    assert resp.json() == {"ok": True}


def test_dispatch_options_bypasses_partner_check() -> None:
    client = _build_app()
    resp: HTTPXResponse = client.options("/ping")
    assert resp.status_code == 405


def test_dispatch_error_no_headers_returns_unauthorized_and_message() -> None:
    client = _build_app()
    resp: HTTPXResponse = client.get("/ping")
    assert resp.status_code == 401
    assert resp.json()["detail"] == "No partner ID found in access token"


def test_dispatch_error_jwt_missing_custom_partner_id_claim() -> None:
    client = _build_app()
    token = encode_jwt({})
    resp: HTTPXResponse = client.get("/ping", headers={"Authorization": f"Bearer {token}"})
    assert resp.status_code == 401
    assert resp.json()["detail"] == "No partner ID found in access token"
