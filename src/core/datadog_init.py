# src/core/datadog_init.py

import os
from typing import Optional, Sequence

_dd_inited = False  # idempotency guard

def init_datadog() -> None:
    """Initialize Datadog tracing once, if the agent is available / enabled."""
    global _dd_inited
    if _dd_inited:
        return

    dd_agent_host = os.environ.get("DD_AGENT_HOST")
    dd_enabled = os.environ.get("DD_TRACE_ENABLED", "").lower() in {"1", "true", "yes"}

    if not (dd_agent_host or dd_enabled):
        # Tracing not requested; skip silently
        return

    try:
        from ddtrace import config, patch, tracer
        from ddtrace.filters import TraceFilter
    except ImportError:
        # Tracing was requested but ddtrace is missing → log it
        print(
            "[datadog] Tracing requested "
            "(DD_AGENT_HOST or DD_TRACE_ENABLED set) but 'ddtrace' is not installed. "
            "Install with: poetry add ddtrace"
        )
        return

    app_name = "recipes-api-service"

    # Keep analytics off unless explicitly enabled via env
    config.analytics.enabled = os.environ.get("DD_ANALYTICS_ENABLED", "").lower() in {"1", "true", "yes"}
    config.partial_flush.enabled = True

    # Nice service names per integration
    config.fastapi["service_name"] = app_name
    config.httpx["service_name"] = f"{app_name}-httpx"
    config.requests["service_name"] = f"{app_name}-requests"
    config.psycopg["service_name"] = f"{app_name}-postgres"
    config.redis["service_name"]  = f"{app_name}-redis"
    config.kafka["service_name"]  = f"{app_name}-kafka"

    # One consolidated patch call (prevents double instrumentation)
    patch(
        fastapi=True,
        httpx=True,
        requests=True,
        psycopg=True,
        redis=True,
        kafka=True,
    )

    class HealthCheckFilter(TraceFilter):
        # Drop traces for /health requests
        def process_trace(self, trace: Sequence[object]) -> Optional[Sequence[object]]:
            if trace and getattr(trace[0], "name", None) == "fastapi.request":
                url = getattr(trace[0], "get_tag", lambda *_: None)("http.url")
                if url and "/health" in url:
                    return None
            return trace

    tracer.configure(settings={"FILTERS": [HealthCheckFilter()]})

    _dd_inited = True
    print("[datadog] Tracing initialized")
