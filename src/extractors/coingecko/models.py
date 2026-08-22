"""Pydantic v2 response models for CoinGecko API data."""

from datetime import datetime

from pydantic import BaseModel, ConfigDict


class CoinMarketData(BaseModel):
    """Data model for coin market data returned by /coins/markets."""

    model_config = ConfigDict(frozen=True)

    id: str
    symbol: str
    name: str
    current_price: float | None = None
    market_cap: int | None = None
    market_cap_rank: int | None = None
    total_volume: float | None = None
    high_24h: float | None = None
    low_24h: float | None = None
    price_change_24h: float | None = None
    price_change_percentage_24h: float | None = None
    last_updated: datetime | None = None


class MarketChartData(BaseModel):
    """Data model for historical market chart data returned by /coins/{id}/market_chart."""

    model_config = ConfigDict(frozen=True)

    prices: list[tuple[int, float]]
    market_caps: list[tuple[int, float]]
    total_volumes: list[tuple[int, float]]
