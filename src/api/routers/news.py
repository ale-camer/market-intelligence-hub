"""News data router for financial articles endpoints."""

from typing import Any

from fastapi import APIRouter, Depends, Query

from src.api.dependencies import get_current_user, get_postgres_repository
from src.loaders.postgres.repository import PostgresRepository

router = APIRouter(prefix="/news", tags=["Financial News"])


@router.get("", response_model=list[dict[str, Any]])
def get_financial_news(
    category: str | None = Query(default=None),
    source: str | None = Query(default=None),
    limit: int = Query(default=100, ge=1, le=1000),
    offset: int = Query(default=0, ge=0),
    repo: PostgresRepository = Depends(get_postgres_repository),
    _current_user: str = Depends(get_current_user),
) -> list[dict[str, Any]]:
    """Retrieve financial news articles with optional filters and pagination."""
    articles = repo.get_news(category=category, source=source, limit=limit, offset=offset)
    return [
        {
            "id": article.id,
            "source": article.source,
            "title": article.title,
            "description": article.description,
            "url": article.url,
            "image_url": article.image_url,
            "author": article.author,
            "published_at": article.published_at.isoformat() if article.published_at else None,
            "content": article.content,
            "source_name": article.source_name,
            "source_id": article.source_id,
            "category": article.category,
            "ingested_at": article.ingested_at.isoformat() if article.ingested_at else None,
        }
        for article in articles
    ]
