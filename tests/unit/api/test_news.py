"""Unit tests for Financial News API router using dependency overrides."""

from datetime import UTC, datetime
from unittest.mock import MagicMock

from fastapi.testclient import TestClient

from src.api.dependencies import get_current_user, get_postgres_repository
from src.api.main import create_app
from src.loaders.postgres.models import FinancialArticleORM


def test_news_unauthenticated() -> None:
    """Test unauthenticated news request returns 401 Unauthorized."""
    app = create_app()
    client = TestClient(app)
    response = client.get("/api/v1/news")
    assert response.status_code == 401


def test_get_financial_news_success() -> None:
    """Test retrieving financial news returns list of articles."""
    app = create_app()

    mock_repo = MagicMock()
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
    app.dependency_overrides[get_current_user] = lambda: "admin"
    client = TestClient(app)

    response = client.get("/api/v1/news?category=general&limit=5")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["title"] == "Fed Interest Rates"
    assert data[0]["source_name"] == "Reuters"
