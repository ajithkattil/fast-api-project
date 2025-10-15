import logging
import threading
from collections.abc import Generator
from io import StringIO

import pytest

from src.utils.logger import ConsoleFormatter
from src.utils.logger_context import clear_logger_context, get_logger_context, set_logger_context_value


@pytest.fixture(scope="function", autouse=True)
def clean_context_after_test() -> Generator[None, None, None]:
    yield
    clear_logger_context()


def test_set_and_get_logger_context_value() -> None:
    set_logger_context_value("user_id", "user_123")
    set_logger_context_value("action", "login")

    context = get_logger_context()
    assert context["user_id"] == "user_123"
    assert context["action"] == "login"


def test_clear_logger_context() -> None:
    set_logger_context_value("test_key", "test_value")
    clear_logger_context()

    context = get_logger_context()
    assert "test_key" not in context


def test_thread_isolation_of_logger_context() -> None:
    results = {}

    def thread_function(thread_id: int) -> None:
        set_logger_context_value("thread_id", thread_id)
        results[thread_id] = get_logger_context()["thread_id"]

    threads = [threading.Thread(target=thread_function, args=(i,)) for i in range(5)]

    for thread in threads:
        thread.start()
    for thread in threads:
        thread.join()

    for i in range(5):
        assert results[i] == i


def test_multiple_context_values() -> None:
    set_logger_context_value("user_id", "user_123")
    set_logger_context_value("request_count", 42)
    set_logger_context_value("is_authenticated", True)
    set_logger_context_value("response_time", 1.23)

    context = get_logger_context()
    assert context["user_id"] == "user_123"
    assert context["request_count"] == 42
    assert context["is_authenticated"] is True
    assert context["response_time"] == 1.23
    assert len(context) == 4


def test_overwrite_context_value() -> None:
    set_logger_context_value("status", "pending")
    assert get_logger_context()["status"] == "pending"

    set_logger_context_value("status", "completed")
    assert get_logger_context()["status"] == "completed"


def test_empty_context_initially() -> None:
    context = get_logger_context()
    assert context == {}
    assert len(context) == 0


def test_context_immutability() -> None:
    set_logger_context_value("original_key", "original_value")

    context = get_logger_context()
    context["new_key"] = "new_value"  # This should not affect the stored context

    fresh_context = get_logger_context()
    assert "new_key" not in fresh_context
    assert fresh_context["original_key"] == "original_value"


def test_context_persistence_within_thread() -> None:
    set_logger_context_value("persistent_key", "persistent_value")

    def check_context() -> str | int | float | bool:
        return get_logger_context().get("persistent_key", "not_found")

    assert check_context() == "persistent_value"

    set_logger_context_value("another_key", "another_value")
    assert get_logger_context()["persistent_key"] == "persistent_value"
    assert get_logger_context()["another_key"] == "another_value"


def test_logger_integration() -> None:
    logger = logging.getLogger("test_logger")
    logger.setLevel(logging.INFO)

    log_stream = StringIO()
    handler = logging.StreamHandler(log_stream)
    handler.setFormatter(ConsoleFormatter())
    logger.addHandler(handler)

    try:
        logger.info("Message without context")

        set_logger_context_value("user_id", "test_user_123")
        set_logger_context_value("action", "test_action")
        logger.info("Message with context")

        log_output = log_stream.getvalue()
        lines = log_output.strip().split("\n")

        assert "Message without context" in lines[0]
        assert "[" not in lines[0]

        assert "Message with context" in lines[1]
        assert "user_id: test_user_123" in lines[1]
        assert "action: test_action" in lines[1]

    finally:
        logger.removeHandler(handler)


def test_clear_context_in_thread_isolation() -> None:
    results = {}

    def thread_function(thread_id: int, should_clear: bool) -> None:
        set_logger_context_value("thread_id", thread_id)
        set_logger_context_value("data", f"data_{thread_id}")

        if should_clear:
            clear_logger_context()
            results[thread_id] = get_logger_context().copy()
        else:
            results[thread_id] = get_logger_context().copy()

    threads = [
        threading.Thread(target=thread_function, args=(0, False)),
        threading.Thread(target=thread_function, args=(1, True)),
        threading.Thread(target=thread_function, args=(2, False)),
    ]

    for thread in threads:
        thread.start()
    for thread in threads:
        thread.join()

    assert results[0]["thread_id"] == 0
    assert results[0]["data"] == "data_0"
    assert results[1] == {}
    assert results[2]["thread_id"] == 2
    assert results[2]["data"] == "data_2"
