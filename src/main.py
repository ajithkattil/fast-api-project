import requests
from fastapi import FastAPI, HTTPException
from fastapi.exceptions import RequestValidationError
from fastapi.middleware import Middleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware

from src.api.router import api_router
from src.clients.culops.mocks.session import MockedSession
from src.core.config import settings
from src.core.datadog_init import init_datadog
from src.core.exception_handlers import (
    general_exception_handler,
    request_validation_exception_handler,
)
from src.core.middleware.partner_id_middleware import PartnerIDMiddleware
from src.core.middleware.rollbar_middleware import RollbarMiddleware
from src.core.middleware.route_context_middleware import RouteContextMiddleware
from src.core.rollbar_init import init_rollbar
from src.utils.logger import ServiceLogger
from src.utils.task_scheduler import TaskScheduler

init_rollbar()
init_datadog()

# Override the requests.Session with the mocked session for testing
if settings.MOCK_CULOPS_API:
    requests.Session = MockedSession

logger = ServiceLogger().get_logger(__name__)

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    middleware=[
        Middleware(TrustedHostMiddleware, allowed_hosts=["*"]),
    ],
)

app.add_middleware(PartnerIDMiddleware)
app.add_middleware(RouteContextMiddleware)
app.add_middleware(RollbarMiddleware)

app.add_exception_handler(Exception, general_exception_handler)
app.add_exception_handler(HTTPException, general_exception_handler)
app.add_exception_handler(RequestValidationError, request_validation_exception_handler)
app.include_router(api_router)

task_scheduler = TaskScheduler()
app.add_event_handler("startup", task_scheduler.start)
app.add_event_handler("shutdown", task_scheduler.shutdown)
