"""End-to-end integration tests for the FastAPI application."""

from datetime import UTC, datetime
from unittest.mock import MagicMock

from fastapi.testclient import TestClient

from src.api.dependencies import get_postgres_repository
from src.api.main import create_app
from src.loaders.postgres.models import FinancialArticleORM, MarketQuoteORM


def test_api_e2e_flow() -> None:
    """Test full E2E flow: login -> get token -> access protected endpoints."""
    app = create_app()

    # Mock the database repository for predictable E2E testing
    mock_repo = MagicMock()

    # Mock Market Quote
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

    # Mock News
    mock_article = FinancialArticleORM(
        id=5,
        source="newsapi",
        title="Fed Interest Rates",
        description="Fed holds rates steady",
        url="https://example.com/fed",
        image_url=None,
        author="John Doe",
        published_at=datetime.now(UTC),
        content="Full content here",
        source_name="Reuters",
        source_id="reuters",
        category="general",
        ingested_at=datetime.now(UTC),
    )
    mock_repo.get_news.return_value = [mock_article]

    app.dependency_overrides[get_postgres_repository] = lambda: mock_repo
    client = TestClient(app)

    # 1. Login to get JWT Token
    login_response = client.post(
        "/api/v1/auth/token",
        data={"username": "admin", "password": "admin"},
    )
    assert login_response.status_code == 200, "Login failed"
    token_data = login_response.json()
    assert "access_token" in token_data
    assert token_data["token_type"] == "bearer"  # noqa: S105
    token = token_data["access_token"]

    headers = {"Authorization": f"Bearer {token}"}

    # 2. Access protected market data endpoint
    market_response = client.get("/api/v1/market/quotes/BTC", headers=headers)
    assert market_response.status_code == 200, "Market endpoint access failed"
    market_data = market_response.json()
    assert market_data["ticker"] == "BTC"
    assert market_data["current_price"] == 65000.0

    # 3. Access protected news endpoint
    news_response = client.get("/api/v1/news", headers=headers)
    assert news_response.status_code == 200, "News endpoint access failed"
    news_data = news_response.json()
    assert isinstance(news_data, list)
    assert len(news_data) == 1
    assert news_data[0]["title"] == "Fed Interest Rates"
