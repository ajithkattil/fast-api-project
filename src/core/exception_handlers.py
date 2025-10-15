from fastapi import HTTPException, Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

from src.core.config import settings
from src.core.exceptions import AccessDeniedException
from src.utils.logger import ServiceLogger

logger = ServiceLogger().get_logger(__name__)


async def general_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    if isinstance(exc, AccessDeniedException):
        logger.error(f"Access Denied: {exc}")
        return JSONResponse(
            status_code=401,
            content={"error": str(exc)},
        )
    elif isinstance(exc, HTTPException):
        logger.exception(f"{exc.status_code} | {exc.detail} | path={request.url.path}")
        return JSONResponse(status_code=exc.status_code, content={"error": exc.detail})
    else:
        logger.exception(f"Unhandled exception: {exc}")

        if settings.ROLLBAR_SERVER_TOKEN:
            try:
                import rollbar

                partner_id = getattr(request.state, "partner_id", None)
                extra_data = {
                    "request_context": {
                        "url": str(request.url),
                        "method": request.method,
                        "partner_id": partner_id,
                        "path": request.url.path,
                        "query_params": dict(request.query_params),
                    },
                    "exception_type": type(exc).__name__,
                }
                rollbar.report_exc_info(extra_data=extra_data)
            except ImportError:
                pass

        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={"error": "Internal Server Error"},
        )


async def request_validation_exception_handler(request: Request, exc: RequestValidationError) -> JSONResponse:
    logger.exception(f"{exc.errors()} | path={request.url.path}")
    err_attrs: list[str] = []
    for error in exc.errors():
        loc = error.get("loc", ())
        if loc:
            field = loc[-1]

        type_validation_error = error.get("type", "")
        if not type_validation_error:
            type_validation_error = "Invalid"
        else:
            type_validation_error = type_validation_error.capitalize()

            err_attrs.append(f"{type_validation_error} {field}")

    err_msg = ", ".join(err_attrs)
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={"error": err_msg},
    )
