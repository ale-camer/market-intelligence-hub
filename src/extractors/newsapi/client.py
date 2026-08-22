"""Async HTTP client for NewsAPI.org."""

from datetime import datetime
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

from src.extractors.exceptions import APIResponseError, ExtractorError, RateLimitError
from src.extractors.newsapi.config import NewsAPISettings
from src.extractors.newsapi.models import NewsResponse

logger = structlog.get_logger(__name__)


class _TransientHTTPError(Exception):
    """Internal exception for retrying transient server errors (5xx)."""


class _TransientRateLimitError(Exception):
    """Internal exception for retrying rate limits (429)."""


class NewsAPIClient:
    """Async HTTP client for fetching financial news articles from NewsAPI.org."""

    def __init__(
        self,
        settings: NewsAPISettings | None = None,
        client: httpx.AsyncClient | None = None,
    ) -> None:
        self.settings = settings or NewsAPISettings()
        headers: dict[str, str] = {
            "Accept": "application/json",
            "X-Api-Key": self.settings.api_key,
        }

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
                            "newsapi_request_sent",
                            endpoint=endpoint,
                            params=clean_params,
                        )
                        response = await self._client.get(endpoint, params=clean_params)

                        if response.status_code == 429:
                            logger.warning("rate_limit_exceeded", endpoint=endpoint)
                            msg = "NewsAPI rate limit exceeded (HTTP 429)"
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
                            "newsapi_request_success",
                            status_code=response.status_code,
                            endpoint=endpoint,
                        )
                        return response.json()
                    except httpx.HTTPStatusError as exc:
                        logger.error(
                            "newsapi_response_error",
                            status_code=exc.response.status_code,
                            endpoint=endpoint,
                        )
                        status = exc.response.status_code
                        msg = f"NewsAPI returned HTTP {status}: {exc}"
                        raise APIResponseError(msg) from exc
                    except httpx.RequestError as exc:
                        logger.error(
                            "newsapi_request_failed",
                            endpoint=endpoint,
                            error=str(exc),
                        )
                        msg = f"HTTP request to NewsAPI failed: {exc}"
                        raise ExtractorError(msg) from exc
        except _TransientRateLimitError as exc:
            msg = "NewsAPI rate limit exceeded (HTTP 429)."
            raise RateLimitError(msg) from exc
        except _TransientHTTPError as exc:
            msg = f"NewsAPI request failed after retries: {exc}"
            raise APIResponseError(msg) from exc

    async def get_everything(
        self,
        q: str,
        from_date: str | datetime | None = None,
        to_date: str | datetime | None = None,
        sort_by: str = "publishedAt",
        page: int = 1,
    ) -> NewsResponse:
        """Search across all news articles via /everything endpoint."""
        from_val = from_date.isoformat() if isinstance(from_date, datetime) else from_date
        to_val = to_date.isoformat() if isinstance(to_date, datetime) else to_date

        params: dict[str, Any] = {
            "q": q,
            "from": from_val,
            "to": to_val,
            "sortBy": sort_by,
            "pageSize": self.settings.page_size,
            "page": page,
        }

        data = await self._make_request("/everything", params=params)
        if not isinstance(data, dict):
            res_type = type(data).__name__
            msg = f"Expected dict response from /everything, got {res_type}"
            raise APIResponseError(msg)

        try:
            return NewsResponse.model_validate(data)
        except ValidationError as exc:
            msg = f"Failed to parse NewsResponse from /everything: {exc}"
            raise APIResponseError(msg) from exc

    async def get_top_headlines(
        self,
        country: str | None = "us",
        category: str | None = "business",
        q: str | None = None,
        page: int = 1,
    ) -> NewsResponse:
        """Fetch top breaking news headlines via /top-headlines endpoint."""
        params: dict[str, Any] = {
            "country": country,
            "category": category,
            "q": q,
            "pageSize": self.settings.page_size,
            "page": page,
        }

        data = await self._make_request("/top-headlines", params=params)
        if not isinstance(data, dict):
            res_type = type(data).__name__
            msg = f"Expected dict response from /top-headlines, got {res_type}"
            raise APIResponseError(msg)

        try:
            return NewsResponse.model_validate(data)
        except ValidationError as exc:
            msg = f"Failed to parse NewsResponse from /top-headlines: {exc}"
            raise APIResponseError(msg) from exc
