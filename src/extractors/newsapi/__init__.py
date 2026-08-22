"""NewsAPI extractor module."""

from src.extractors.newsapi.client import NewsAPIClient
from src.extractors.newsapi.config import NewsAPISettings
from src.extractors.newsapi.extractor import NewsAPIExtractor
from src.extractors.newsapi.models import (
    NewsArticle,
    NewsResponse,
    NewsSource,
)

__all__ = [
    "NewsAPIClient",
    "NewsAPIExtractor",
    "NewsAPISettings",
    "NewsArticle",
    "NewsResponse",
    "NewsSource",
]
