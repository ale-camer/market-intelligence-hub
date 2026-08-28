"""Unit tests for Kafka producer and consumer using mocks and Avro serialization."""

from datetime import UTC, datetime
from unittest.mock import MagicMock

import pytest

from src.messaging.kafka.consumer import KafkaEventConsumer, deserialize_avro
from src.messaging.kafka.producer import (
    FINANCIAL_NEWS_AVRO_SCHEMA,
    MARKET_QUOTE_AVRO_SCHEMA,
    KafkaEventProducer,
    serialize_avro,
)
from src.schemas.enums import AssetClass, DataSource
from src.schemas.market import MarketQuote
from src.schemas.news import FinancialArticle


@pytest.fixture
def mock_producer() -> MagicMock:
    """Fixture supplying a mock confluent_kafka Producer."""
    return MagicMock()


@pytest.fixture
def mock_consumer() -> MagicMock:
    """Fixture supplying a mock confluent_kafka Consumer."""
    return MagicMock()


def test_avro_serialization_roundtrip() -> None:
    """Test serializing and deserializing a dictionary with Avro."""
    payload = {
        "source": "coingecko",
        "ticker": "ETH",
        "asset_class": "crypto",
        "name": "Ethereum",
        "current_price": 3000.0,
        "market_cap": 350000000000,
        "volume_24h": 15000000000.0,
        "currency": "USD",
        "exchange": "binance",
        "price_change_pct_24h": 2.5,
        "ingested_at": "2026-01-01T00:00:00Z",
    }
    encoded = serialize_avro(payload, MARKET_QUOTE_AVRO_SCHEMA)
    decoded = deserialize_avro(encoded, MARKET_QUOTE_AVRO_SCHEMA)
    assert decoded["ticker"] == "ETH"
    assert decoded["current_price"] == 3000.0


def test_producer_publish_market_quote(mock_producer: MagicMock) -> None:
    """Test publishing a MarketQuote produces a Kafka message."""
    producer_wrapper = KafkaEventProducer(producer=mock_producer)
    quote = MarketQuote(
        source=DataSource.COINGECKO,
        ticker="BTC",
        asset_class=AssetClass.CRYPTO,
        name="Bitcoin",
        current_price=65000.0,
    )

    producer_wrapper.publish_market_quote(quote, topic="test-market-topic")
    mock_producer.produce.assert_called_once()
    args, kwargs = mock_producer.produce.call_args
    assert args[0] == "test-market-topic"
    assert kwargs["key"] == b"BTC"
    assert isinstance(kwargs["value"], bytes)


def test_producer_publish_financial_news(mock_producer: MagicMock) -> None:
    """Test publishing a FinancialArticle produces a Kafka message."""
    producer_wrapper = KafkaEventProducer(producer=mock_producer)
    article = FinancialArticle(
        source=DataSource.NEWSAPI,
        title="Market Update",
        url="https://example.com/news/1",
        published_at=datetime.now(UTC),
        source_name="Bloomberg",
    )

    producer_wrapper.publish_financial_news(article, topic="test-news-topic")
    mock_producer.produce.assert_called_once()
    args, kwargs = mock_producer.produce.call_args
    assert args[0] == "test-news-topic"
    assert kwargs["key"] == b"https://example.com/news/1"


def test_producer_flush(mock_producer: MagicMock) -> None:
    """Test producer flush delegates to inner producer."""
    producer_wrapper = KafkaEventProducer(producer=mock_producer)
    producer_wrapper.flush(timeout=5.0)
    mock_producer.flush.assert_called_with(timeout=5.0)


def test_consumer_subscribe_and_poll(mock_consumer: MagicMock) -> None:
    """Test consumer subscribe, poll, and clean closing."""
    consumer_wrapper = KafkaEventConsumer(consumer=mock_consumer)
    consumer_wrapper.subscribe(["test-topic"])
    mock_consumer.subscribe.assert_called_with(["test-topic"])

    # Simulate empty message poll
    mock_consumer.poll.return_value = None
    result = consumer_wrapper.poll_and_deserialize(schema=FINANCIAL_NEWS_AVRO_SCHEMA)
    assert result is None

    # Simulate message with value
    sample_payload = {
        "source": "newsapi",
        "title": "Fed Rates",
        "description": None,
        "url": "https://example.com/fed",
        "article_url": None,
        "image_url": None,
        "author": None,
        "published_at": "2026-01-01T00:00:00Z",
        "content": None,
        "source_name": "Reuters",
        "source_id": None,
        "category": None,
        "ingested_at": "2026-01-01T00:00:00Z",
    }
    encoded = serialize_avro(sample_payload, FINANCIAL_NEWS_AVRO_SCHEMA)

    mock_msg = MagicMock()
    mock_msg.error.return_value = None
    mock_msg.value.return_value = encoded
    mock_consumer.poll.return_value = mock_msg

    result = consumer_wrapper.poll_and_deserialize(schema=FINANCIAL_NEWS_AVRO_SCHEMA)
    assert result is not None
    assert result["title"] == "Fed Rates"

    consumer_wrapper.close()
    mock_consumer.close.assert_called_once()
