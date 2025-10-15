from typing import cast

import kafka
from google.protobuf.message import EncodeError, Message as ProtobufMessage
from kafka.errors import KafkaError

from src.core.config import settings
from src.core.exceptions import ServerError
from src.utils.logger import ServiceLogger

logger = ServiceLogger().get_logger(__name__)


class BaseProducer:
    def __init__(self, topic: str):
        self.settings = settings
        self.topic = topic
        config = {
            "bootstrap_servers": self.settings.KAFKA_BOOTSTRAP_SERVER,
            "client_id": "recipes-api-service",
            "key_serializer": self._key_serializer,
            "value_serializer": self._value_serializer,
            "acks": "all",
            "retries": 3,
            "retry_backoff_ms": 300,
            "request_timeout_ms": 5000,
        }
        self.producer = kafka.KafkaProducer(**config)

    def __enter__(self) -> "BaseProducer":
        return self

    def __exit__(self, exc_type: type | None, exc_val: BaseException | None, exc_tb: object | None) -> None:
        self.producer.flush()
        self.producer.close()

    def produce(self, message: str | ProtobufMessage | bytes, key: str | None = None) -> None:
        try:
            self.producer.send(topic=self.topic, value=message, key=key).get(
                timeout=self.settings.KAFKA_PRODUCER_GET_TIMEOUT
            )
        except (KafkaError, EncodeError) as e:
            logger.error("Error producing message to Kafka", exc_info=e)
            raise ServerError("Failed to produce message to Kafka") from e

    @staticmethod
    def _key_serializer(key: str | None) -> bytes | None:
        if key is None:
            return None
        return key.encode("utf-8")

    @staticmethod
    def _value_serializer(value: str | bytes | ProtobufMessage | None) -> bytes | None:
        if value is None:
            return None
        elif isinstance(value, bytes):
            return value
        elif isinstance(value, ProtobufMessage):
            return cast(bytes, value.SerializeToString())
        return value.encode("utf-8")
