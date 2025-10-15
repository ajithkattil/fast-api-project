from contextvars import ContextVar

logger_context: ContextVar[dict[str, str | int | float | bool] | None] = ContextVar("logger_context", default=None)


def get_logger_context() -> dict[str, str | int | float | bool]:
    context = logger_context.get()
    if context is None:
        return {}
    return context.copy()


def set_logger_context_value(name: str, value: str | int | float | bool) -> None:
    context = logger_context.get()
    if context is None:
        current_context = {}
    else:
        current_context = context.copy()
    current_context[name] = value
    logger_context.set(current_context)


def clear_logger_context() -> None:
    logger_context.set({})
