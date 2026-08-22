"""High-level facade for Yahoo Finance data extraction."""

from datetime import datetime

from src.extractors.yahoo_finance.client import YahooFinanceClient
from src.extractors.yahoo_finance.config import YahooFinanceSettings
from src.extractors.yahoo_finance.models import OHLCVSeries, TickerQuote


class YahooFinanceExtractor:
    """Facade for extracting OHLCV and quote data from Yahoo Finance."""

    def __init__(
        self,
        settings: YahooFinanceSettings | None = None,
        client: YahooFinanceClient | None = None,
    ) -> None:
        self.settings = settings or YahooFinanceSettings()
        self._client = client or YahooFinanceClient(settings=self.settings)

    def extract_ohlcv(
        self,
        ticker: str,
        start: str | datetime | None = None,
        end: str | datetime | None = None,
        interval: str | None = None,
    ) -> OHLCVSeries:
        """Extract historical OHLCV series for a stock or forex ticker."""
        return self._client.get_ohlcv(
            ticker=ticker,
            start=start,
            end=end,
            interval=interval,
        )

    def extract_quote(self, ticker: str) -> TickerQuote:
        """Extract current quote summary for a stock or forex ticker."""
        return self._client.get_quote(ticker=ticker)
