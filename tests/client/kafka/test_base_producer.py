from collections.abc import Generator
from unittest.mock import MagicMock, patch

import pytest
from google.protobuf.message import EncodeError, Message as ProtobufMessage
from kafka.errors import KafkaError

from src.clients.kafka.base_producer import BaseProducer
from src.core.exceptions import ServerError


@pytest.fixture
def mock_kafka_producer() -> Generator[MagicMock, None, None]:
    with patch("kafka.KafkaProducer") as mock_producer_class:
        mock_producer_instance = MagicMock()
        mock_producer_class.return_value = mock_producer_instance
        yield mock_producer_instance


@pytest.fixture
def base_producer(mock_kafka_producer: MagicMock) -> BaseProducer:
    return BaseProducer(topic="test-topic")


def test_produce_success(base_producer: BaseProducer, mock_kafka_producer: MagicMock) -> None:
    mock_future = MagicMock()
    mock_kafka_producer.send.return_value = mock_future

    base_producer.produce(message="test_message", key="test_key")

    mock_kafka_producer.send.assert_called_once_with(topic="test-topic", value="test_message", key="test_key")
    mock_future.get.assert_called_once_with(timeout=base_producer.settings.KAFKA_PRODUCER_GET_TIMEOUT)


def test_produce_success_without_key(base_producer: BaseProducer, mock_kafka_producer: MagicMock) -> None:
    mock_future = MagicMock()
    mock_kafka_producer.send.return_value = mock_future
    base_producer.produce(message="test_message")
    mock_kafka_producer.send.assert_called_once_with(topic="test-topic", value="test_message", key=None)

    mock_kafka_producer.send.assert_called_once_with(topic="test-topic", value="test_message", key=None)


def test_produce_kafka_error(base_producer: BaseProducer, mock_kafka_producer: MagicMock) -> None:
    mock_kafka_producer.send.side_effect = KafkaError("Test Kafka Error")

    with pytest.raises(ServerError, match="Failed to produce message to Kafka"):
        base_producer.produce(message="test_message", key="test_key")


def test_context_manager(mock_kafka_producer: MagicMock) -> None:
    with BaseProducer(topic="test-topic") as producer:
        producer.produce(message="test_message", key="test_key")

    mock_kafka_producer.flush.assert_called_once()
    mock_kafka_producer.close.assert_called_once()


def test_key_serializer() -> None:
    assert BaseProducer._key_serializer(None) is None
    assert BaseProducer._key_serializer("test_key") == b"test_key"


def test_value_serializer() -> None:
    assert BaseProducer._value_serializer(None) is None
    assert BaseProducer._value_serializer(b"test_bytes") == b"test_bytes"
    assert BaseProducer._value_serializer("test_string") == b"test_string"

    mock_proto_message = MagicMock(spec=ProtobufMessage)
    mock_proto_message.SerializeToString.return_value = b"serialized_proto"
    assert BaseProducer._value_serializer(mock_proto_message) == b"serialized_proto"

    mock_proto_message.SerializeToString.side_effect = EncodeError("Serialization Error")
    with pytest.raises(EncodeError):
        BaseProducer._value_serializer(mock_proto_message)
