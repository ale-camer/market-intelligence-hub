"""Kafka Producer wrapper for serializing and publishing events using fastavro."""

import io
from typing import Any

import fastavro
from confluent_kafka import Producer

from src.messaging.kafka.config import KafkaConfig
from src.schemas.market import MarketQuote
from src.schemas.news import FinancialArticle

MARKET_QUOTE_AVRO_SCHEMA: dict[str, Any] = {
    "type": "record",
    "name": "MarketQuoteRecord",
    "namespace": "com.marketintelligence.events",
    "fields": [
        {"name": "source", "type": "string"},
        {"name": "ticker", "type": "string"},
        {"name": "asset_class", "type": "string"},
        {"name": "name", "type": ["null", "string"], "default": None},
        {"name": "current_price", "type": ["null", "double"], "default": None},
        {"name": "market_cap", "type": ["null", "long"], "default": None},
        {"name": "volume_24h", "type": ["null", "double"], "default": None},
        {"name": "currency", "type": "string", "default": "USD"},
        {"name": "exchange", "type": ["null", "string"], "default": None},
        {"name": "price_change_pct_24h", "type": ["null", "double"], "default": None},
        {"name": "ingested_at", "type": "string"},
    ],
}

FINANCIAL_NEWS_AVRO_SCHEMA: dict[str, Any] = {
    "type": "record",
    "name": "FinancialArticleRecord",
    "namespace": "com.marketintelligence.events",
    "fields": [
        {"name": "source", "type": "string"},
        {"name": "title", "type": "string"},
        {"name": "description", "type": ["null", "string"], "default": None},
        {"name": "url", "type": "string"},
        {"name": "image_url", "type": ["null", "string"], "default": None},
        {"name": "author", "type": ["null", "string"], "default": None},
        {"name": "published_at", "type": "string"},
        {"name": "content", "type": ["null", "string"], "default": None},
        {"name": "source_name", "type": "string"},
        {"name": "source_id", "type": ["null", "string"], "default": None},
        {"name": "category", "type": ["null", "string"], "default": None},
        {"name": "ingested_at", "type": "string"},
    ],
}


def serialize_avro(record: dict[str, Any], schema: dict[str, Any]) -> bytes:
    """Serialize a python dict into bytes using fastavro schemaless writer."""
    out = io.BytesIO()
    parsed_schema = fastavro.parse_schema(schema)
    fastavro.schemaless_writer(out, parsed_schema, record)
    return out.getvalue()


class KafkaEventProducer:
    """Producer class for serializing and publishing domain events to Kafka topics."""

    def __init__(
        self, bootstrap_servers: str | None = None, producer: Producer | None = None
    ) -> None:
        """Initialize Kafka producer client."""
        self.bootstrap_servers = bootstrap_servers or KafkaConfig.BOOTSTRAP_SERVERS
        self.producer = producer or Producer({"bootstrap.servers": self.bootstrap_servers})

    def publish_market_quote(
        self, quote: MarketQuote, topic: str = KafkaConfig.MARKET_EVENTS_TOPIC
    ) -> None:
        """Serialize and publish a MarketQuote event."""
        payload = {
            "source": quote.source.value,
            "ticker": quote.ticker,
            "asset_class": quote.asset_class.value,
            "name": quote.name,
            "current_price": quote.current_price,
            "market_cap": quote.market_cap,
            "volume_24h": quote.volume_24h,
            "currency": quote.currency,
            "exchange": quote.exchange,
            "price_change_pct_24h": quote.price_change_pct_24h,
            "ingested_at": quote.ingested_at.isoformat(),
        }
        bytes_data = serialize_avro(payload, MARKET_QUOTE_AVRO_SCHEMA)
        self.producer.produce(topic, key=quote.ticker.encode("utf-8"), value=bytes_data)

    def publish_financial_news(
        self, article: FinancialArticle, topic: str = KafkaConfig.NEWS_EVENTS_TOPIC
    ) -> None:
        """Serialize and publish a FinancialArticle event."""
        payload = {
            "source": article.source.value,
            "title": article.title,
            "description": article.description,
            "url": article.url,
            "image_url": article.image_url,
            "author": article.author,
            "published_at": article.published_at.isoformat(),
            "content": article.content,
            "source_name": article.source_name,
            "source_id": article.source_id,
            "category": article.category,
            "ingested_at": article.ingested_at.isoformat(),
        }
        bytes_data = serialize_avro(payload, FINANCIAL_NEWS_AVRO_SCHEMA)
        self.producer.produce(topic, key=article.url.encode("utf-8"), value=bytes_data)

    def flush(self, timeout: float = 10.0) -> int:
        """Flush outstanding messages in producer queue."""
        return self.producer.flush(timeout=timeout)
