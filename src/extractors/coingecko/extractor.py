"""High-level facade for CoinGecko data extraction."""

from types import TracebackType
from typing import Self

from src.extractors.coingecko.client import CoinGeckoClient
from src.extractors.coingecko.config import CoinGeckoSettings
from src.extractors.coingecko.models import CoinMarketData, MarketChartData


class CoinGeckoExtractor:
    """Facade for extracting market data and price history from CoinGecko."""

    def __init__(
        self,
        settings: CoinGeckoSettings | None = None,
        client: CoinGeckoClient | None = None,
    ) -> None:
        self.settings = settings or CoinGeckoSettings()
        self._client = client or CoinGeckoClient(settings=self.settings)

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
        """Close the underlying client resources."""
        await self._client.close()

    async def extract_market_data(
        self,
        coin_ids: list[str],
        vs_currency: str = "usd",
        per_page: int = 100,
        page: int = 1,
    ) -> list[CoinMarketData]:
        """Extract current market data for a list of coin IDs."""
        return await self._client.get_coins_markets(
            vs_currency=vs_currency,
            ids=coin_ids,
            per_page=per_page,
            page=page,
        )

    async def extract_price_history(
        self,
        coin_id: str,
        days: int | str = 30,
        vs_currency: str = "usd",
    ) -> MarketChartData:
        """Extract historical price data for a single coin ID."""
        return await self._client.get_coin_market_chart(
            coin_id=coin_id,
            vs_currency=vs_currency,
            days=days,
        )
