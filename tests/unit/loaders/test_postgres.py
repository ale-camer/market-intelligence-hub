"""Unit tests for PostgresRepository loader using SQLite in-memory database."""

from datetime import UTC, datetime

import pytest

from src.loaders.postgres.models import FinancialArticleORM, MarketQuoteORM, PriceHistoryORM
from src.loaders.postgres.repository import PostgresRepository
from src.schemas.enums import AssetClass, DataSource
from src.schemas.market import MarketQuote, PriceBar
from src.schemas.news import FinancialArticle


@pytest.fixture
def repository() -> PostgresRepository:
    """Fixture to supply a clean SQLite in-memory database repository."""
    repo = PostgresRepository(database_url="sqlite:///:memory:")
    repo.create_tables()
    return repo


def test_upsert_market_quote(repository: PostgresRepository) -> None:
    """Test saving a market quote into the database."""
    quote = MarketQuote(
        source=DataSource.COINGECKO,
        ticker="BTC",
        asset_class=AssetClass.CRYPTO,
        name="Bitcoin",
        current_price=65000.50,
        volume_24h=123456789.0,
        currency="USD",
    )

    orm_obj = repository.upsert_market_quote(quote)
    assert orm_obj.id is not None
    assert orm_obj.ticker == "BTC"
    assert orm_obj.source == "coingecko"

    with repository.get_session() as session:
        queried = session.query(MarketQuoteORM).filter_by(ticker="BTC").first()
        assert queried is not None
        assert queried.current_price == 65000.50


def test_bulk_insert_news(repository: PostgresRepository) -> None:
    """Test bulk insertion of news articles."""
    articles = [
        FinancialArticle(
            source=DataSource.NEWSAPI,
            title=f"Article {i}",
            description="Test description",
            url=f"https://example.com/article/{i}",
            published_at=datetime.now(UTC),
            source_name="Reuters",
        )
        for i in range(3)
    ]

    inserted_count = repository.bulk_insert_news(articles)
    assert inserted_count == 3

    with repository.get_session() as session:
        count = session.query(FinancialArticleORM).count()
        assert count == 3


def test_bulk_insert_price_bars(repository: PostgresRepository) -> None:
    """Test bulk insertion of OHLCV price bars."""
    bars = [
        PriceBar(
            source=DataSource.YAHOO_FINANCE,
            ticker="AAPL",
            asset_class=AssetClass.EQUITY,
            dt=datetime.now(UTC),
            open=150.0,
            high=155.0,
            low=149.0,
            close=154.0,
            volume=10000.0,
        )
    ]

    inserted_count = repository.bulk_insert_price_bars(bars)
    assert inserted_count == 1

    with repository.get_session() as session:
        queried = session.query(PriceHistoryORM).filter_by(ticker="AAPL").first()
        assert queried is not None
        assert queried.close == 154.0
