"""Unit tests for Market Data API router using dependency overrides."""

from datetime import UTC, datetime
from unittest.mock import MagicMock

from fastapi.testclient import TestClient

from src.api.dependencies import get_postgres_repository
from src.api.main import create_app
from src.loaders.postgres.models import MarketQuoteORM, PriceHistoryORM


def test_get_market_quote_success() -> None:
    """Test retrieving market quote returns 200 OK and expected dict."""
    app = create_app()

    mock_repo = MagicMock()
    mock_quote = MarketQuoteORM(
        id=1,
        source="coingecko",
        ticker="BTC",
        asset_class="crypto",
        name="Bitcoin",
        current_price=65000.0,
        market_cap=1200000000000,
        volume_24h=30000000000.0,
        currency="USD",
        exchange="binance",
        price_change_pct_24h=1.5,
        ingested_at=datetime.now(UTC),
    )
    mock_repo.get_latest_market_quote.return_value = mock_quote

    app.dependency_overrides[get_postgres_repository] = lambda: mock_repo
    client = TestClient(app)

    response = client.get("/api/v1/market/quotes/BTC")
    assert response.status_code == 200
    data = response.json()
    assert data["ticker"] == "BTC"
    assert data["current_price"] == 65000.0


def test_get_market_quote_not_found() -> None:
    """Test retrieving non-existent market quote returns 404 Not Found."""
    app = create_app()

    mock_repo = MagicMock()
    mock_repo.get_latest_market_quote.return_value = None

    app.dependency_overrides[get_postgres_repository] = lambda: mock_repo
    client = TestClient(app)

    response = client.get("/api/v1/market/quotes/UNKNOWN")
    assert response.status_code == 404
    assert "not found" in response.json()["detail"].lower()


def test_get_price_bars_success() -> None:
    """Test retrieving price history bars returns list of bars."""
    app = create_app()

    mock_repo = MagicMock()
    mock_bar = PriceHistoryORM(
        id=10,
        source="yfinance",
        ticker="AAPL",
        asset_class="equity",
        dt=datetime.now(UTC),
        open=150.0,
        high=155.0,
        low=149.0,
        close=154.0,
        volume=1000000.0,
        ingested_at=datetime.now(UTC),
    )
    mock_repo.get_price_bars.return_value = [mock_bar]

    app.dependency_overrides[get_postgres_repository] = lambda: mock_repo
    client = TestClient(app)

    response = client.get("/api/v1/market/bars/AAPL?limit=10&offset=0")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["ticker"] == "AAPL"
    assert data[0]["close"] == 154.0
