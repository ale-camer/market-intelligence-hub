"""Unit tests for NewsAPI extractor and client."""

from typing import Any
from unittest.mock import AsyncMock

import httpx
import pytest

from src.extractors.exceptions import (
    APIResponseError,
    ExtractorError,
    RateLimitError,
)
from src.extractors.newsapi.client import NewsAPIClient
from src.extractors.newsapi.config import NewsAPISettings
from src.extractors.newsapi.extractor import NewsAPIExtractor
from src.extractors.newsapi.models import NewsResponse

pytestmark = pytest.mark.asyncio


@pytest.fixture
def fast_settings() -> NewsAPISettings:
    """Fixture with fast retries for testing."""
    return NewsAPISettings(
        api_key="test_key",
        base_url="https://newsapi.org/v2",
        timeout_seconds=5.0,
        max_retries=2,
        retry_wait_seconds=0.01,
    )


@pytest.fixture
def mock_articles_response() -> dict[str, Any]:
    """Sample JSON response from NewsAPI."""
    return {
        "status": "ok",
        "totalResults": 2,
        "articles": [
            {
                "source": {"id": "reuters", "name": "Reuters"},
                "author": "John Doe",
                "title": "Fed announces interest rate decision",
                "description": "The Federal Reserve held rates steady.",
                "url": "https://reuters.com/article/fed-rates",
                "urlToImage": "https://reuters.com/image.jpg",
                "publishedAt": "2026-08-22T10:00:00Z",
                "content": "Full article content...",
            },
            {
                "source": {"id": None, "name": "Bloomberg"},
                "author": None,
                "title": "Stock market reaches new high",
                "description": "Tech stocks lead rally.",
                "url": "https://bloomberg.com/article/stocks",
                "urlToImage": None,
                "publishedAt": "2026-08-22T11:00:00Z",
                "content": None,
            },
        ],
    }


async def test_get_everything_success(
    fast_settings: NewsAPISettings, mock_articles_response: dict[str, Any]
) -> None:
    """Test successful search request via /everything."""
    mock_httpx = AsyncMock(spec=httpx.AsyncClient)
    mock_httpx.get.return_value = httpx.Response(
        200,
        json=mock_articles_response,
        request=httpx.Request("GET", "https://newsapi.org/v2/everything"),
    )

    async with NewsAPIClient(settings=fast_settings, client=mock_httpx) as client:
        res = await client.get_everything(q="economy")

    assert isinstance(res, NewsResponse)
    assert res.status == "ok"
    assert res.total_results == 2
    assert len(res.articles) == 2
    assert res.articles[0].source.name == "Reuters"
    assert res.articles[0].title == "Fed announces interest rate decision"
    assert res.articles[1].source.id is None


async def test_get_everything_empty(fast_settings: NewsAPISettings) -> None:
    """Test empty results response from /everything."""
    empty_payload = {"status": "ok", "totalResults": 0, "articles": []}
    mock_httpx = AsyncMock(spec=httpx.AsyncClient)
    mock_httpx.get.return_value = httpx.Response(
        200,
        json=empty_payload,
        request=httpx.Request("GET", "https://newsapi.org/v2/everything"),
    )

    async with NewsAPIClient(settings=fast_settings, client=mock_httpx) as client:
        res = await client.get_everything(q="nonexistentquery")

    assert res.total_results == 0
    assert res.articles == []


async def test_get_top_headlines_success(
    fast_settings: NewsAPISettings, mock_articles_response: dict[str, Any]
) -> None:
    """Test fetching top headlines via /top-headlines."""
    mock_httpx = AsyncMock(spec=httpx.AsyncClient)
    mock_httpx.get.return_value = httpx.Response(
        200,
        json=mock_articles_response,
        request=httpx.Request("GET", "https://newsapi.org/v2/top-headlines"),
    )

    async with NewsAPIClient(settings=fast_settings, client=mock_httpx) as client:
        res = await client.get_top_headlines(country="us", category="business")

    assert isinstance(res, NewsResponse)
    assert res.total_results == 2


async def test_rate_limit_raises(fast_settings: NewsAPISettings) -> None:
    """Test HTTP 429 response raises RateLimitError."""
    mock_httpx = AsyncMock(spec=httpx.AsyncClient)
    mock_httpx.get.return_value = httpx.Response(
        429,
        request=httpx.Request("GET", "https://newsapi.org/v2/everything"),
    )

    async with NewsAPIClient(settings=fast_settings, client=mock_httpx) as client:
        with pytest.raises(RateLimitError):
            await client.get_everything(q="inflation")


async def test_server_error_raises(fast_settings: NewsAPISettings) -> None:
    """Test HTTP 500 response raises APIResponseError after retries."""
    mock_httpx = AsyncMock(spec=httpx.AsyncClient)
    mock_httpx.get.return_value = httpx.Response(
        500,
        request=httpx.Request("GET", "https://newsapi.org/v2/everything"),
    )

    async with NewsAPIClient(settings=fast_settings, client=mock_httpx) as client:
        with pytest.raises(APIResponseError):
            await client.get_everything(q="crypto")


async def test_retry_on_transient_error(
    fast_settings: NewsAPISettings, mock_articles_response: dict[str, Any]
) -> None:
    """Test retry logic recovers after initial 503 error."""
    mock_httpx = AsyncMock(spec=httpx.AsyncClient)
    req = httpx.Request("GET", "https://newsapi.org/v2/everything")
    mock_httpx.get.side_effect = [
        httpx.Response(503, request=req),
        httpx.Response(200, json=mock_articles_response, request=req),
    ]

    async with NewsAPIClient(settings=fast_settings, client=mock_httpx) as client:
        res = await client.get_everything(q="stocks")

    assert res.total_results == 2
    assert mock_httpx.get.call_count == 2


async def test_timeout_raises(fast_settings: NewsAPISettings) -> None:
    """Test request timeout raises ExtractorError."""
    mock_httpx = AsyncMock(spec=httpx.AsyncClient)
    req = httpx.Request("GET", "https://newsapi.org/v2/everything")
    mock_httpx.get.side_effect = httpx.TimeoutException("Connection timed out", request=req)

    async with NewsAPIClient(settings=fast_settings, client=mock_httpx) as client:
        with pytest.raises(ExtractorError):
            await client.get_everything(q="tech")


async def test_api_key_header_injected(fast_settings: NewsAPISettings) -> None:
    """Test X-Api-Key header is injected into underlying httpx client."""
    client = NewsAPIClient(settings=fast_settings)
    assert client._client.headers.get("X-Api-Key") == "test_key"
    await client.close()


async def test_extractor_facade() -> None:
    """Test NewsAPIExtractor facade delegates calls to client."""
    mock_client = AsyncMock(spec=NewsAPIClient)
    expected_res = NewsResponse(status="ok", totalResults=0, articles=[])
    mock_client.get_everything.return_value = expected_res
    mock_client.get_top_headlines.return_value = expected_res

    async with NewsAPIExtractor(client=mock_client) as extractor:
        res_everything = await extractor.extract_everything(q="market")
        res_headlines = await extractor.extract_top_headlines()

    assert res_everything == expected_res
    assert res_headlines == expected_res
    mock_client.get_everything.assert_called_once_with(
        q="market", from_date=None, to_date=None, sort_by="publishedAt", page=1
    )
    mock_client.get_top_headlines.assert_called_once_with(
        country="us", category="business", q=None, page=1
    )
