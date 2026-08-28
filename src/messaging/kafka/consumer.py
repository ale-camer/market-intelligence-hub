"""Kafka Consumer wrapper for subscribing to topics and deserializing Avro payloads."""

import io
from typing import Any, cast

import fastavro
from confluent_kafka import Consumer

from src.messaging.kafka.config import KafkaConfig


def deserialize_avro(data: bytes, schema: dict[str, Any]) -> dict[str, Any]:
    """Deserialize raw bytes payload into a Python dict using fastavro."""
    inp = io.BytesIO(data)
    parsed_schema = fastavro.parse_schema(schema)
    return cast("dict[str, Any]", fastavro.schemaless_reader(inp, parsed_schema))


class KafkaEventConsumer:
    """Consumer class for subscribing to Kafka topics and consuming Avro messages."""

    def __init__(
        self,
        group_id: str | None = None,
        bootstrap_servers: str | None = None,
        consumer: Consumer | None = None,
    ) -> None:
        """Initialize Kafka consumer with consumer group and broker settings."""
        self.bootstrap_servers = bootstrap_servers or KafkaConfig.BOOTSTRAP_SERVERS
        self.group_id = group_id or KafkaConfig.DEFAULT_CONSUMER_GROUP
        self.consumer = consumer or Consumer(
            {
                "bootstrap.servers": self.bootstrap_servers,
                "group.id": self.group_id,
                "auto.offset.reset": "earliest",
            }
        )

    def subscribe(self, topics: list[str]) -> None:
        """Subscribe consumer to a list of Kafka topics."""
        self.consumer.subscribe(topics)

    def poll_and_deserialize(
        self, schema: dict[str, Any], timeout: float = 1.0
    ) -> dict[str, Any] | None:
        """Poll a message from Kafka and deserialize using provided Avro schema."""
        msg = self.consumer.poll(timeout=timeout)
        if msg is None or msg.error():
            return None
        value_bytes: bytes | None = msg.value()
        if value_bytes is None:
            return None
        return deserialize_avro(value_bytes, schema)

    def close(self) -> None:
        """Close Kafka consumer session cleanly."""
        self.consumer.close()
