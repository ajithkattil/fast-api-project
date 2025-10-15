"""Rollbar initialization for error tracking."""

import os

from src.core.config import settings


def _get_rollbar_token() -> str | None:
    """Get Rollbar token from environment or Parameter Store."""
    # First check environment variable
    token = settings.ROLLBAR_SERVER_TOKEN
    if token:
        return token

    # Fall back to Parameter Store (only in deployed environments)
    try:
        import boto3
        from botocore.exceptions import ClientError, NoCredentialsError

        ssm = boto3.client('ssm', region_name='us-east-1')
        param_name = f"/{settings.DEPLOY_ENV}/applications/wms/recipes-api-service/environment/ROLLBAR_SERVER_TOKEN"

        response = ssm.get_parameter(Name=param_name, WithDecryption=True)
        return response['Parameter']['Value']
    except (ImportError, ClientError, KeyError, NoCredentialsError):
        # No credentials (tests/local dev) or parameter doesn't exist - skip Rollbar
        return None


def init_rollbar() -> None:
    """Initialize Rollbar if access token is available."""
    rollbar_token = _get_rollbar_token()

    if not rollbar_token:
        return

    try:
        import rollbar
    except ImportError:
        return

    environment = settings.ROLLBAR_ENV or settings.DEPLOY_ENV
    code_version = settings.ROLLBAR_CODE_VERSION or settings.VERSION

    rollbar.init(
        access_token=rollbar_token,
        environment=environment,
        code_version=code_version,
        locals={"enabled": False},
        capture_email=True,
        capture_username=True,
        populate_empty_backtraces=True,
        exception_level_filters=[
            ("fastapi.exceptions.HTTPException", "ignore"),
            ("starlette.exceptions.HTTPException", "ignore"),
            ("asyncio.TimeoutError", "warning"),
            ("httpx.TimeoutException", "warning"),
            ("requests.exceptions.Timeout", "warning"),
            ("httpx.ConnectError", "warning"),
            ("requests.exceptions.ConnectionError", "warning"),
        ],
    )


def get_rollbar_person_data(partner_id: str | None = None, user_id: str | None = None) -> dict:
    """Generate person data for Rollbar context."""
    person_data = {}

    if partner_id:
        person_data["id"] = f"partner_{partner_id}"
        person_data["partner_id"] = partner_id

    if user_id:
        person_data["username"] = user_id

    return person_data


def report_with_context(message: str, level: str = "error", extra_data: dict | None = None) -> None:
    """Report to Rollbar with additional context."""
    rollbar_token = _get_rollbar_token()

    if not rollbar_token:
        return

    try:
        import rollbar

        rollbar.report_message(message, level=level, extra_data=extra_data or {})
    except ImportError:
        pass
