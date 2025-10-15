import logging
from collections.abc import Generator
from io import StringIO

import pytest

from src.utils.logger import ServiceLogger
from src.utils.logger_context import clear_logger_context, set_logger_context_value


@pytest.fixture(scope="function", autouse=True)
def clean_context_after_test() -> Generator[None, None, None]:
    yield
    clear_logger_context()


def test_service_logger_includes_context_in_formatted_output() -> None:
    logger = ServiceLogger().get_logger("test_service_logger")

    log_stream = StringIO()

    logger.handlers.clear()
    handler = logging.StreamHandler(log_stream)
    handler.setLevel(logging.INFO)

    from src.utils.logger import ConsoleFormatter

    handler.setFormatter(ConsoleFormatter())
    logger.addHandler(handler)

    try:
        logger.info("Message without context")

        set_logger_context_value("test_key", "test_value")
        set_logger_context_value("user_id", "user_123")
        logger.info("Message with context")

        log_output = log_stream.getvalue()
        lines = log_output.strip().split("\n")

        assert "Message without context" in lines[0]
        assert "test_key:" not in lines[0]
        assert "user_id:" not in lines[0]

        assert "Message with context" in lines[1]
        assert "test_key: test_value" in lines[1]
        assert "user_id: user_123" in lines[1]

    finally:
        logger.removeHandler(handler)


def test_service_logger_context_changes_dynamically() -> None:
    logger = ServiceLogger().get_logger("test_context_changes")

    log_stream = StringIO()
    logger.handlers.clear()
    handler = logging.StreamHandler(log_stream)
    handler.setLevel(logging.INFO)

    from src.utils.logger import ConsoleFormatter

    handler.setFormatter(ConsoleFormatter())
    logger.addHandler(handler)

    try:
        set_logger_context_value("status", "started")
        set_logger_context_value("request_id", "req_001")
        logger.info("First message")

        set_logger_context_value("status", "processing")
        set_logger_context_value("progress", "50%")
        logger.info("Second message")

        clear_logger_context()
        logger.info("Third message")

        log_output = log_stream.getvalue()
        lines = log_output.strip().split("\n")

        assert "First message" in lines[0]
        assert "status: started" in lines[0]
        assert "request_id: req_001" in lines[0]

        assert "Second message" in lines[1]
        assert "status: processing" in lines[1]
        assert "request_id: req_001" in lines[1]
        assert "progress: 50%" in lines[1]

        assert "Third message" in lines[2]
        assert "status:" not in lines[2]
        assert "request_id:" not in lines[2]
        assert "progress:" not in lines[2]

    finally:
        logger.removeHandler(handler)
