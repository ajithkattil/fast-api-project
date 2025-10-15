import json
import logging
import sys

from pythonjsonlogger import jsonlogger

from src.core.config import settings
from src.utils.logger_context import get_logger_context


class ConsoleFormatter(logging.Formatter):
    def __init__(self) -> None:
        super().__init__("%(asctime)s - %(name)s - %(levelname)s - %(message)s")

    def format(self, record: logging.LogRecord) -> str:
        context = get_logger_context()
        current_log = super().format(record)

        log_parts = current_log.split(" - ")
        context_parts = [f"{key}: {value}" for key, value in context.items()]
        modified_log = " - ".join(log_parts[:3] + context_parts + log_parts[3:])

        return modified_log


class CustomJSONFormatter(jsonlogger.JsonFormatter):
    def format(self, record: logging.LogRecord) -> str:
        context = get_logger_context()

        current_output = super().format(record)
        output_dict = json.loads(current_output)

        new_output = {**output_dict, **context}
        svc_name = settings.APP_NAME.lower()
        new_output["service"] = svc_name

        return json.dumps(new_output, default=str)


class ServiceLogger:
    def __init__(self) -> None:
        self.settings = settings

    def get_logger(self, name: str) -> logging.Logger:
        logger = logging.getLogger(name)
        if not logger.handlers:
            logger.setLevel(self.settings.LOG_LEVEL)

            handler = logging.StreamHandler()
            handler.setLevel(self.settings.LOG_LEVEL)

            handler.setStream(sys.stdout)

            if self.settings.DEPLOY_ENV.lower() not in ["production", "staging", "prod", "stage"]:
                handler.setFormatter(ConsoleFormatter())
                logger.addHandler(handler)
            else:
                handler.setFormatter(CustomJSONFormatter())
                logger.addHandler(handler)

            # Add Rollbar handler for error and warning logs
            if settings.ROLLBAR_SERVER_TOKEN:
                try:
                    from rollbar.logger import RollbarHandler

                    rollbar_handler = RollbarHandler()
                    rollbar_handler.setLevel(logging.WARNING)  # Only WARNING and ERROR logs
                    logger.addHandler(rollbar_handler)
                except ImportError:
                    pass

        return logger
