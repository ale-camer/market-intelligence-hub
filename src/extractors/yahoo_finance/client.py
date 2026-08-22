"""Synchronous HTTP client wrapping yfinance for Yahoo Finance data."""

from datetime import datetime
from typing import Any

import pandas as pd
import structlog
import yfinance as yf
from pydantic import ValidationError
from tenacity import (
    Retrying,
    retry_if_exception_type,
    stop_after_attempt,
    wait_exponential,
)

from src.extractors.exceptions import APIResponseError, ExtractorError
from src.extractors.yahoo_finance.config import YahooFinanceSettings
from src.extractors.yahoo_finance.models import (
    OHLCVBar,
    OHLCVSeries,
    TickerQuote,
)

logger = structlog.get_logger(__name__)


class _TransientYahooError(Exception):
    """Internal exception for retrying transient yfinance failures."""


class YahooFinanceClient:
    """Client for fetching stock and forex market data via yfinance."""

    def __init__(self, settings: YahooFinanceSettings | None = None) -> None:
        self.settings = settings or YahooFinanceSettings()

    def _execute_with_retry(
        self,
        action_name: str,
        func: Any,  # noqa: ANN401
        *args: Any,  # noqa: ANN401
        **kwargs: Any,  # noqa: ANN401
    ) -> Any:  # noqa: ANN401
        """Execute a callable with retry logic using tenacity."""
        try:
            for attempt in Retrying(
                stop=stop_after_attempt(self.settings.max_retries),
                wait=wait_exponential(min=1, max=10),
                retry=retry_if_exception_type(_TransientYahooError),
                reraise=True,
            ):
                with attempt:
                    try:
                        logger.info(
                            "yahoo_request_sent",
                            action=action_name,
                            args=args,
                        )
                        return func(*args, **kwargs)
                    except (ExtractorError, APIResponseError):
                        raise
                    except Exception as exc:
                        logger.warning(
                            "yahoo_request_retry",
                            action=action_name,
                            error=str(exc),
                        )
                        msg = f"Transient error during {action_name}: {exc}"
                        raise _TransientYahooError(msg) from exc
        except _TransientYahooError as exc:
            msg = f"Yahoo Finance request failed after retries for {action_name}: {exc}"
            raise ExtractorError(msg) from exc

    def get_ohlcv(
        self,
        ticker: str,
        start: str | datetime | None = None,
        end: str | datetime | None = None,
        interval: str | None = None,
    ) -> OHLCVSeries:
        """Fetch historical OHLCV bar series for a given ticker."""
        chosen_interval = interval or self.settings.default_interval

        def _fetch() -> pd.DataFrame:
            return yf.download(
                tickers=ticker,
                start=start,
                end=end,
                interval=chosen_interval,
                progress=False,
                auto_adjust=True,
            )

        try:
            df = self._execute_with_retry("get_ohlcv", _fetch)
        except Exception as exc:
            if isinstance(exc, ExtractorError):
                raise
            msg = f"Failed to download OHLCV data for ticker '{ticker}': {exc}"
            raise ExtractorError(msg) from exc

        if df is None or df.empty:
            logger.info("ohlcv_empty_result", ticker=ticker)
            return OHLCVSeries(ticker=ticker, interval=chosen_interval, bars=[])

        if isinstance(df.columns, pd.MultiIndex):
            df.columns = df.columns.get_level_values(0)

        df = df.reset_index()

        date_col = (
            "Date"
            if "Date" in df.columns
            else ("Datetime" if "Datetime" in df.columns else str(df.columns[0]))
        )

        bars: list[OHLCVBar] = []
        try:
            for _, row in df.iterrows():
                raw_date = row[date_col]
                if isinstance(raw_date, pd.Timestamp):
                    dt = raw_date.to_pydatetime()
                elif isinstance(raw_date, str):
                    dt = datetime.fromisoformat(raw_date)
                else:
                    dt = raw_date

                bar = OHLCVBar(
                    date=dt,
                    open=float(row["Open"]),
                    high=float(row["High"]),
                    low=float(row["Low"]),
                    close=float(row["Close"]),
                    volume=int(row["Volume"]),
                )
                bars.append(bar)
        except (KeyError, ValueError, ValidationError) as exc:
            msg = f"Failed to parse OHLCV DataFrame for '{ticker}': {exc}"
            raise APIResponseError(msg) from exc

        logger.info("ohlcv_fetch_success", ticker=ticker, bars_count=len(bars))
        return OHLCVSeries(ticker=ticker, interval=chosen_interval, bars=bars)

    def get_quote(self, ticker: str) -> TickerQuote:
        """Fetch current quote summary for a given ticker."""

        def _fetch() -> dict[str, Any]:
            t = yf.Ticker(ticker)
            info = t.info
            if not info or not isinstance(info, dict):
                msg = f"No info returned for ticker '{ticker}'"
                raise APIResponseError(msg)
            return info

        try:
            info = self._execute_with_retry("get_quote", _fetch)
        except APIResponseError:
            raise
        except Exception as exc:
            if isinstance(exc, ExtractorError):
                raise
            msg = f"Failed to fetch quote for ticker '{ticker}': {exc}"
            raise ExtractorError(msg) from exc

        try:
            price = info.get("currentPrice") or info.get("regularMarketPrice")
            cap = info.get("marketCap")
            return TickerQuote(
                ticker=ticker,
                short_name=info.get("shortName"),
                current_price=float(price) if price is not None else None,
                market_cap=int(cap) if cap is not None else None,
                currency=info.get("currency"),
                exchange=info.get("exchange"),
                quote_type=info.get("quoteType"),
            )
        except (ValueError, ValidationError) as exc:
            msg = f"Failed to parse quote data for '{ticker}': {exc}"
            raise APIResponseError(msg) from exc
