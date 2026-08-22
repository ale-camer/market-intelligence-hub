"""Pydantic v2 response models for Yahoo Finance data."""

from datetime import datetime

from pydantic import BaseModel, ConfigDict


class OHLCVBar(BaseModel):
    """Single OHLCV (Open, High, Low, Close, Volume) data bar."""

    model_config = ConfigDict(frozen=True)

    date: datetime
    open: float
    high: float
    low: float
    close: float
    volume: int


class OHLCVSeries(BaseModel):
    """Historical OHLCV data series for a given ticker and interval."""

    model_config = ConfigDict(frozen=True)

    ticker: str
    interval: str
    bars: list[OHLCVBar]


class TickerQuote(BaseModel):
    """Current quote and summary information for a ticker."""

    model_config = ConfigDict(frozen=True)

    ticker: str
    short_name: str | None = None
    current_price: float | None = None
    market_cap: int | None = None
    currency: str | None = None
    exchange: str | None = None
    quote_type: str | None = None
