"""Kafka messaging configuration module."""

import os


class KafkaConfig:
    """Configuration settings for Kafka Producer and Consumer clients."""

    BOOTSTRAP_SERVERS: str = os.getenv("KAFKA_BOOTSTRAP_SERVERS", "localhost:9092")
    MARKET_EVENTS_TOPIC: str = os.getenv("KAFKA_MARKET_EVENTS_TOPIC", "market-events")
    NEWS_EVENTS_TOPIC: str = os.getenv("KAFKA_NEWS_EVENTS_TOPIC", "news-events")
    DEFAULT_CONSUMER_GROUP: str = os.getenv(
        "KAFKA_CONSUMER_GROUP", "market-intelligence-consumer-group"
    )
