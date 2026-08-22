"""Unit tests for news canonical schemas."""

from datetime import UTC, datetime

import pytest
from pydantic import ValidationError

from src.schemas.enums import DataSource
from src.schemas.news import FinancialArticle


def test_financial_article_creation() -> None:
    """Test creating a FinancialArticle with full parameters."""
    published = datetime.now(UTC)
    article = FinancialArticle(
        source=DataSource.NEWSAPI,
        title="Federal Reserve Decision",
        description="Interest rates kept unchanged.",
        url="https://example.com/article",
        image_url="https://example.com/image.jpg",
        author="Jane Doe",
        published_at=published,
        content="Article content body...",
        source_name="Financial Times",
        source_id="financial-times",
        category="macroeconomics",
    )

    assert article.source == DataSource.NEWSAPI
    assert article.title == "Federal Reserve Decision"
    assert article.source_name == "Financial Times"
    assert article.published_at == published
    assert article.ingested_at is not None


def test_financial_article_defaults() -> None:
    """Test FinancialArticle default fields."""
    published = datetime.now(UTC)
    article = FinancialArticle(
        source=DataSource.NEWSAPI,
        title="Breaking News",
        url="https://example.com/news",
        published_at=published,
        source_name="Reuters",
    )

    assert article.description is None
    assert article.author is None
    assert article.content is None
    assert article.source_id is None
    assert isinstance(article.ingested_at, datetime)


def test_financial_article_frozen() -> None:
    """Test that FinancialArticle is immutable."""
    published = datetime.now(UTC)
    article = FinancialArticle(
        source=DataSource.NEWSAPI,
        title="Breaking News",
        url="https://example.com/news",
        published_at=published,
        source_name="Reuters",
    )

    with pytest.raises(ValidationError):
        article.title = "Updated Title"  # type: ignore[misc]
