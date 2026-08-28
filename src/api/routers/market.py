"""Market data router for quotes and price history endpoints."""

from typing import Any

from fastapi import APIRouter, Depends, HTTPException, Query, status

from src.api.dependencies import get_current_user, get_postgres_repository
from src.loaders.postgres.repository import PostgresRepository

router = APIRouter(prefix="/market", tags=["Market Data"])


@router.get("/quotes/{ticker}", response_model=dict[str, Any])
def get_latest_quote(
    ticker: str,
    repo: PostgresRepository = Depends(get_postgres_repository),
    _current_user: str = Depends(get_current_user),
) -> dict[str, Any]:
    """Retrieve latest market quote for a given ticker symbol."""
    quote = repo.get_latest_market_quote(ticker=ticker.upper())
    if not quote:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Market quote for ticker '{ticker}' not found.",
        )
    return {
        "id": quote.id,
        "source": quote.source,
        "ticker": quote.ticker,
        "asset_class": quote.asset_class,
        "name": quote.name,
        "current_price": quote.current_price,
        "market_cap": quote.market_cap,
        "volume_24h": quote.volume_24h,
        "currency": quote.currency,
        "exchange": quote.exchange,
        "price_change_pct_24h": quote.price_change_pct_24h,
        "ingested_at": quote.ingested_at.isoformat() if quote.ingested_at else None,
    }


@router.get("/bars/{ticker}", response_model=list[dict[str, Any]])
def get_price_bars(
    ticker: str,
    limit: int = Query(default=100, ge=1, le=1000),
    offset: int = Query(default=0, ge=0),
    repo: PostgresRepository = Depends(get_postgres_repository),
    _current_user: str = Depends(get_current_user),
) -> list[dict[str, Any]]:
    """Retrieve historical price bars (OHLCV) for a given ticker."""
    bars = repo.get_price_bars(ticker=ticker.upper(), limit=limit, offset=offset)
    return [
        {
            "id": bar.id,
            "source": bar.source,
            "ticker": bar.ticker,
            "asset_class": bar.asset_class,
            "dt": bar.dt.isoformat() if bar.dt else None,
            "open": bar.open,
            "high": bar.high,
            "low": bar.low,
            "close": bar.close,
            "volume": bar.volume,
            "ingested_at": bar.ingested_at.isoformat() if bar.ingested_at else None,
        }
        for bar in bars
    ]
