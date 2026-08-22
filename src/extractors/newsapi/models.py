"""Pydantic v2 response models for NewsAPI data."""

from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class NewsSource(BaseModel):
    """Metadata for a news article source."""

    model_config = ConfigDict(frozen=True, populate_by_name=True)

    id: str | None = None
    name: str


class NewsArticle(BaseModel):
    """Single news article model."""

    model_config = ConfigDict(frozen=True, populate_by_name=True)

    source: NewsSource
    author: str | None = None
    title: str
    description: str | None = None
    url: str
    url_to_image: str | None = Field(default=None, alias="urlToImage")
    published_at: datetime = Field(alias="publishedAt")
    content: str | None = None


class NewsResponse(BaseModel):
    """Paginated response wrapper from NewsAPI."""

    model_config = ConfigDict(frozen=True, populate_by_name=True)

    status: str
    total_results: int = Field(alias="totalResults")
    articles: list[NewsArticle]
