"""Canonical market data schemas for the Market Intelligence Hub."""

from datetime import datetime

from src.schemas.base import BaseSchema
from src.schemas.enums import AssetClass


class MarketQuote(BaseSchema):
    """Normalized market quote for any asset class (crypto, equity, forex, ETF)."""

    ticker: str
    asset_class: AssetClass
    name: str | None = None
    current_price: float | None = None
    market_cap: int | None = None
    volume_24h: float | None = None
    currency: str = "USD"
    exchange: str | None = None
    price_change_pct_24h: float | None = None


class PriceBar(BaseSchema):
    """Single normalized OHLCV (Open, High, Low, Close, Volume) data bar."""

    ticker: str
    asset_class: AssetClass
    dt: datetime
    open: float
    high: float
    low: float
    close: float
    volume: float


class PriceHistory(BaseSchema):
    """Normalized time series of price bars for an asset."""

    ticker: str
    asset_class: AssetClass
    interval: str
    bars: list[PriceBar]
