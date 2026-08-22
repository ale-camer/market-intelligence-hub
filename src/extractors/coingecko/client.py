"""Async HTTP client for CoinGecko API v3."""

from types import TracebackType
from typing import Any, Self

import httpx
import structlog
from pydantic import ValidationError
from tenacity import (
    AsyncRetrying,
    retry_if_exception_type,
    stop_after_attempt,
    wait_exponential,
)

from src.extractors.coingecko.config import CoinGeckoSettings
from src.extractors.coingecko.models import CoinMarketData, MarketChartData
from src.extractors.exceptions import APIResponseError, ExtractorError, RateLimitError

logger = structlog.get_logger(__name__)


class _TransientHTTPError(Exception):
    """Internal exception for retrying transient server errors (5xx)."""


class _TransientRateLimitError(Exception):
    """Internal exception for retrying rate limits (429)."""


class CoinGeckoClient:
    """Async HTTP client for fetching crypto data from CoinGecko API v3."""

    def __init__(
        self,
        settings: CoinGeckoSettings | None = None,
        client: httpx.AsyncClient | None = None,
    ) -> None:
        self.settings = settings or CoinGeckoSettings()
        headers: dict[str, str] = {
            "Accept": "application/json",
        }
        if self.settings.api_key:
            headers["x-cg-demo-api-key"] = self.settings.api_key

        self._external_client = client is not None
        self._client = client or httpx.AsyncClient(
            base_url=self.settings.base_url,
            headers=headers,
            timeout=httpx.Timeout(self.settings.timeout_seconds),
        )

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
        """Close the underlying HTTP client if managed internally."""
        if not self._external_client:
            await self._client.aclose()

    async def _make_request(self, endpoint: str, params: dict[str, Any] | None = None) -> Any:  # noqa: ANN401
        """Execute an HTTP GET request with retries and structured error handling."""
        clean_params = {k: str(v) for k, v in (params or {}).items() if v is not None}

        try:
            async for attempt in AsyncRetrying(
                stop=stop_after_attempt(self.settings.max_retries),
                wait=wait_exponential(min=self.settings.retry_wait_seconds, max=10),
                retry=retry_if_exception_type((_TransientHTTPError, _TransientRateLimitError)),
                reraise=True,
            ):
                with attempt:
                    try:
                        logger.info(
                            "api_request_sent",
                            endpoint=endpoint,
                            params=clean_params,
                        )
                        response = await self._client.get(endpoint, params=clean_params)

                        if response.status_code == 429:
                            logger.warning("rate_limit_exceeded", endpoint=endpoint)
                            msg = "CoinGecko API rate limit exceeded (HTTP 429)"
                            raise _TransientRateLimitError(msg)

                        if response.status_code in (500, 502, 503, 504):
                            logger.warning(
                                "transient_server_error",
                                status_code=response.status_code,
                                endpoint=endpoint,
                            )
                            msg = f"Server error HTTP {response.status_code}"
                            raise _TransientHTTPError(msg)

                        response.raise_for_status()
                        logger.info(
                            "api_request_success",
                            status_code=response.status_code,
                            endpoint=endpoint,
                        )
                        return response.json()
                    except httpx.HTTPStatusError as exc:
                        logger.error(
                            "api_response_error",
                            status_code=exc.response.status_code,
                            endpoint=endpoint,
                        )
                        status = exc.response.status_code
                        msg = f"CoinGecko API returned HTTP {status}: {exc}"
                        raise APIResponseError(msg) from exc
                    except httpx.RequestError as exc:
                        logger.error(
                            "api_request_failed",
                            endpoint=endpoint,
                            error=str(exc),
                        )
                        msg = f"HTTP request to CoinGecko failed: {exc}"
                        raise ExtractorError(msg) from exc
        except _TransientRateLimitError as exc:
            msg = "CoinGecko API rate limit exceeded (HTTP 429)."
            raise RateLimitError(msg) from exc
        except _TransientHTTPError as exc:
            msg = f"CoinGecko API request failed after retries: {exc}"
            raise APIResponseError(msg) from exc

    async def get_coins_markets(
        self,
        vs_currency: str = "usd",
        ids: list[str] | None = None,
        per_page: int = 100,
        page: int = 1,
    ) -> list[CoinMarketData]:
        """Fetch market data for coins from /coins/markets endpoint."""
        params: dict[str, Any] = {
            "vs_currency": vs_currency,
            "per_page": per_page,
            "page": page,
        }
        if ids:
            params["ids"] = ",".join(ids)

        data = await self._make_request("/coins/markets", params=params)
        if not isinstance(data, list):
            res_type = type(data).__name__
            msg = f"Expected list response from /coins/markets, got {res_type}"
            raise APIResponseError(msg)

        try:
            return [CoinMarketData.model_validate(item) for item in data]
        except ValidationError as exc:
            msg = f"Failed to parse CoinMarketData response: {exc}"
            raise APIResponseError(msg) from exc

    async def get_coin_market_chart(
        self,
        coin_id: str,
        vs_currency: str = "usd",
        days: int | str = 30,
    ) -> MarketChartData:
        """Fetch historical market chart data from /coins/{id}/market_chart."""
        params: dict[str, Any] = {
            "vs_currency": vs_currency,
            "days": days,
        }
        endpoint = f"/coins/{coin_id}/market_chart"
        data = await self._make_request(endpoint, params=params)
        if not isinstance(data, dict):
            res_type = type(data).__name__
            msg = f"Expected dict response from {endpoint}, got {res_type}"
            raise APIResponseError(msg)

        try:
            return MarketChartData.model_validate(data)
        except ValidationError as exc:
            msg = f"Failed to parse MarketChartData response: {exc}"
            raise APIResponseError(msg) from exc
