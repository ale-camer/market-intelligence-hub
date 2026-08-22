"""Unit tests for market canonical schemas."""

from datetime import UTC, datetime

import pytest
from pydantic import ValidationError

from src.schemas.enums import AssetClass, DataSource
from src.schemas.market import MarketQuote, PriceBar, PriceHistory


def test_market_quote_creation() -> None:
    """Test creating a MarketQuote with full parameters."""
    quote = MarketQuote(
        source=DataSource.COINGECKO,
        ticker="BTC",
        asset_class=AssetClass.CRYPTO,
        name="Bitcoin",
        current_price=50000.0,
        market_cap=1000000000000,
        volume_24h=25000000000.0,
        currency="USD",
        exchange="CoinGecko",
        price_change_pct_24h=2.5,
    )

    assert quote.source == DataSource.COINGECKO
    assert quote.ticker == "BTC"
    assert quote.asset_class == AssetClass.CRYPTO
    assert quote.name == "Bitcoin"
    assert quote.current_price == 50000.0
    assert quote.currency == "USD"
    assert quote.ingested_at is not None


def test_market_quote_defaults() -> None:
    """Test MarketQuote default fields and automatic ingested_at assignment."""
    quote = MarketQuote(
        source=DataSource.YAHOO_FINANCE,
        ticker="AAPL",
        asset_class=AssetClass.EQUITY,
    )

    assert quote.source == DataSource.YAHOO_FINANCE
    assert quote.ticker == "AAPL"
    assert quote.name is None
    assert quote.current_price is None
    assert quote.currency == "USD"
    assert isinstance(quote.ingested_at, datetime)


def test_market_quote_frozen() -> None:
    """Test that MarketQuote is immutable."""
    quote = MarketQuote(
        source=DataSource.YAHOO_FINANCE,
        ticker="AAPL",
        asset_class=AssetClass.EQUITY,
    )

    with pytest.raises(ValidationError):
        quote.current_price = 150.0  # type: ignore[misc]


def test_price_bar_creation() -> None:
    """Test creating a PriceBar."""
    now = datetime.now(UTC)
    bar = PriceBar(
        source=DataSource.YAHOO_FINANCE,
        ticker="AAPL",
        asset_class=AssetClass.EQUITY,
        dt=now,
        open=150.0,
        high=155.0,
        low=149.0,
        close=154.0,
        volume=1000000.0,
    )

    assert bar.ticker == "AAPL"
    assert bar.close == 154.0
    assert bar.dt == now


def test_price_history_creation() -> None:
    """Test creating a PriceHistory container."""
    now = datetime.now(UTC)
    bar = PriceBar(
        source=DataSource.YAHOO_FINANCE,
        ticker="AAPL",
        asset_class=AssetClass.EQUITY,
        dt=now,
        open=150.0,
        high=155.0,
        low=149.0,
        close=154.0,
        volume=1000000.0,
    )
    history = PriceHistory(
        source=DataSource.YAHOO_FINANCE,
        ticker="AAPL",
        asset_class=AssetClass.EQUITY,
        interval="1d",
        bars=[bar],
    )

    assert history.ticker == "AAPL"
    assert history.interval == "1d"
    assert len(history.bars) == 1
    assert history.bars[0].close == 154.0
