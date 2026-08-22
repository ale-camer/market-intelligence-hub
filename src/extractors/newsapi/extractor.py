"""High-level facade for NewsAPI data extraction."""

from datetime import datetime
from types import TracebackType
from typing import Self

from src.extractors.newsapi.client import NewsAPIClient
from src.extractors.newsapi.config import NewsAPISettings
from src.extractors.newsapi.models import NewsResponse


class NewsAPIExtractor:
    """Facade for extracting financial news articles from NewsAPI.org."""

    def __init__(
        self,
        settings: NewsAPISettings | None = None,
        client: NewsAPIClient | None = None,
    ) -> None:
        self.settings = settings or NewsAPISettings()
        self._client = client or NewsAPIClient(settings=self.settings)

    async def __aenter__(self) -> Self:
        return self

    async def __aexit__(
        self,
        exc_type: type[BaseException] | None,
        exc_val: BaseException | None,
        exc_tb: TracebackType | None,
    ) -> None:
        await self.close()

    async def close(self) -> None:
        """Close the underlying client connection."""
        await self._client.close()

    async def extract_everything(
        self,
        q: str,
        from_date: str | datetime | None = None,
        to_date: str | datetime | None = None,
        sort_by: str = "publishedAt",
        page: int = 1,
    ) -> NewsResponse:
        """Extract news articles matching a search query."""
        return await self._client.get_everything(
            q=q,
            from_date=from_date,
            to_date=to_date,
            sort_by=sort_by,
            page=page,
        )

    async def extract_top_headlines(
        self,
        country: str | None = "us",
        category: str | None = "business",
        q: str | None = None,
        page: int = 1,
    ) -> NewsResponse:
        """Extract top breaking news headlines."""
        return await self._client.get_top_headlines(
            country=country,
            category=category,
            q=q,
            page=page,
        )
