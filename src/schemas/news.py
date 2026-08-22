"""Canonical news schemas for the Market Intelligence Hub."""

from datetime import datetime

from src.schemas.base import BaseSchema


class FinancialArticle(BaseSchema):
    """Normalized financial news article schema for downstream processing."""

    title: str
    description: str | None = None
    url: str
    image_url: str | None = None
    author: str | None = None
    published_at: datetime
    content: str | None = None
    source_name: str
    source_id: str | None = None
    category: str | None = None
