"""Unit tests for CoinGecko extractor and async HTTP client."""

from typing import Any
from unittest.mock import AsyncMock, MagicMock

import httpx
import pytest
from pytest_mock import MockerFixture

from src.extractors.coingecko.client import CoinGeckoClient
from src.extractors.coingecko.config import CoinGeckoSettings
from src.extractors.coingecko.extractor import CoinGeckoExtractor
from src.extractors.coingecko.models import CoinMarketData, MarketChartData
from src.extractors.exceptions import APIResponseError, ExtractorError, RateLimitError


@pytest.fixture
def fast_settings() -> CoinGeckoSettings:
    """Fast retries setting fixture for tests."""
    return CoinGeckoSettings(
        api_key="",
        base_url="https://api.coingecko.com/api/v3",
        timeout_seconds=5.0,
        max_retries=2,
        retry_wait_seconds=0.001,
    )


@pytest.mark.asyncio
async def test_get_coins_markets_success(
    fast_settings: CoinGeckoSettings, mocker: MockerFixture
) -> None:
    """Test successful response parsing from /coins/markets."""
    mock_data: list[dict[str, Any]] = [
        {
            "id": "bitcoin",
            "symbol": "btc",
            "name": "Bitcoin",
            "current_price": 50000.0,
            "market_cap": 1000000000,
            "market_cap_rank": 1,
            "total_volume": 50000000.0,
            "high_24h": 51000.0,
            "low_24h": 49000.0,
            "price_change_24h": 1000.0,
            "price_change_percentage_24h": 2.04,
            "last_updated": "2026-08-22T20:00:00.000Z",
        }
    ]
    mock_response = MagicMock(spec=httpx.Response)
    mock_response.status_code = 200
    mock_response.json.return_value = mock_data

    async with CoinGeckoClient(settings=fast_settings) as client:
        mocker.patch.object(client._client, "get", return_value=mock_response)
        res = await client.get_coins_markets(ids=["bitcoin"])

        assert len(res) == 1
        assert isinstance(res[0], CoinMarketData)
        assert res[0].id == "bitcoin"
        assert res[0].current_price == 50000.0


@pytest.mark.asyncio
async def test_get_coins_markets_empty(
    fast_settings: CoinGeckoSettings, mocker: MockerFixture
) -> None:
    """Test empty response from /coins/markets returns empty list."""
    mock_response = MagicMock(spec=httpx.Response)
    mock_response.status_code = 200
    mock_response.json.return_value = []

    async with CoinGeckoClient(settings=fast_settings) as client:
        mocker.patch.object(client._client, "get", return_value=mock_response)
        res = await client.get_coins_markets(ids=["unknown"])

        assert res == []


@pytest.mark.asyncio
async def test_get_coin_market_chart_success(
    fast_settings: CoinGeckoSettings, mocker: MockerFixture
) -> None:
    """Test successful response parsing from /coins/{id}/market_chart."""
    mock_data: dict[str, Any] = {
        "prices": [[1700000000000, 50000.0]],
        "market_caps": [[1700000000000, 1000000000.0]],
        "total_volumes": [[1700000000000, 50000000.0]],
    }
    mock_response = MagicMock(spec=httpx.Response)
    mock_response.status_code = 200
    mock_response.json.return_value = mock_data

    async with CoinGeckoClient(settings=fast_settings) as client:
        mocker.patch.object(client._client, "get", return_value=mock_response)
        res = await client.get_coin_market_chart(coin_id="bitcoin", days=30)

        assert isinstance(res, MarketChartData)
        assert res.prices == [(1700000000000, 50000.0)]


@pytest.mark.asyncio
async def test_rate_limit_raises(fast_settings: CoinGeckoSettings, mocker: MockerFixture) -> None:
    """Test HTTP 429 raises RateLimitError after retries."""
    mock_response = MagicMock(spec=httpx.Response)
    mock_response.status_code = 429

    async with CoinGeckoClient(settings=fast_settings) as client:
        mocker.patch.object(client._client, "get", return_value=mock_response)
        with pytest.raises(RateLimitError):
            await client.get_coins_markets(ids=["bitcoin"])


@pytest.mark.asyncio
async def test_server_error_raises(fast_settings: CoinGeckoSettings, mocker: MockerFixture) -> None:
    """Test HTTP 500 raises APIResponseError after retries."""
    mock_response = MagicMock(spec=httpx.Response)
    mock_response.status_code = 500

    async with CoinGeckoClient(settings=fast_settings) as client:
        mocker.patch.object(client._client, "get", return_value=mock_response)
        with pytest.raises(APIResponseError):
            await client.get_coins_markets(ids=["bitcoin"])


@pytest.mark.asyncio
async def test_retry_on_transient_error(
    fast_settings: CoinGeckoSettings, mocker: MockerFixture
) -> None:
    """Test client retries on 503 and succeeds on subsequent 200."""
    resp_503 = MagicMock(spec=httpx.Response)
    resp_503.status_code = 503

    resp_200 = MagicMock(spec=httpx.Response)
    resp_200.status_code = 200
    resp_200.json.return_value = []

    async with CoinGeckoClient(settings=fast_settings) as client:
        mock_get = mocker.patch.object(client._client, "get", side_effect=[resp_503, resp_200])
        res = await client.get_coins_markets(ids=["bitcoin"])

        assert res == []
        assert mock_get.call_count == 2


@pytest.mark.asyncio
async def test_timeout_raises(fast_settings: CoinGeckoSettings, mocker: MockerFixture) -> None:
    """Test httpx.TimeoutException raises ExtractorError."""
    async with CoinGeckoClient(settings=fast_settings) as client:
        mocker.patch.object(
            client._client,
            "get",
            side_effect=httpx.TimeoutException("Timeout"),
        )
        with pytest.raises(ExtractorError):
            await client.get_coins_markets(ids=["bitcoin"])


def test_api_key_header_injected() -> None:
    """Test x-cg-demo-api-key header is injected when api_key is present."""
    settings = CoinGeckoSettings(api_key="demo_key_123")
    client = CoinGeckoClient(settings=settings)
    assert client._client.headers.get("x-cg-demo-api-key") == "demo_key_123"


def test_api_key_header_absent() -> None:
    """Test x-cg-demo-api-key header is absent when api_key is empty."""
    settings = CoinGeckoSettings(api_key="")
    client = CoinGeckoClient(settings=settings)
    assert "x-cg-demo-api-key" not in client._client.headers


@pytest.mark.asyncio
async def test_extractor_facade() -> None:
    """Test CoinGeckoExtractor facade delegates calls to underlying client."""
    mock_client = MagicMock(spec=CoinGeckoClient)
    mock_client.get_coins_markets = AsyncMock(return_value=[])
    mock_client.get_coin_market_chart = AsyncMock(
        return_value=MarketChartData(prices=[], market_caps=[], total_volumes=[])
    )
    mock_client.close = AsyncMock()

    async with CoinGeckoExtractor(client=mock_client) as extractor:
        res_markets = await extractor.extract_market_data(coin_ids=["bitcoin"])
        res_chart = await extractor.extract_price_history(coin_id="bitcoin", days=7)

        assert res_markets == []
        assert isinstance(res_chart, MarketChartData)
        mock_client.get_coins_markets.assert_awaited_once_with(
            vs_currency="usd", ids=["bitcoin"], per_page=100, page=1
        )
        mock_client.get_coin_market_chart.assert_awaited_once_with(
            coin_id="bitcoin", vs_currency="usd", days=7
        )
