"""Unit tests for Yahoo Finance extractor and client."""

from typing import Any
from unittest.mock import MagicMock

import pandas as pd
import pytest
from pytest_mock import MockerFixture

from src.extractors.exceptions import APIResponseError, ExtractorError
from src.extractors.yahoo_finance.client import YahooFinanceClient
from src.extractors.yahoo_finance.config import YahooFinanceSettings
from src.extractors.yahoo_finance.extractor import YahooFinanceExtractor
from src.extractors.yahoo_finance.models import (
    OHLCVSeries,
    TickerQuote,
)


@pytest.fixture
def fast_settings() -> YahooFinanceSettings:
    """Fast retries setting fixture for tests."""
    return YahooFinanceSettings(
        default_interval="1d",
        timeout_seconds=5.0,
        max_retries=2,
    )


@pytest.fixture
def mock_ohlcv_df() -> pd.DataFrame:
    """Fixture providing sample OHLCV DataFrame."""
    data = {
        "Date": [pd.Timestamp("2026-08-20"), pd.Timestamp("2026-08-21")],
        "Open": [150.0, 152.0],
        "High": [155.0, 156.0],
        "Low": [149.0, 151.0],
        "Close": [153.0, 154.5],
        "Volume": [1000000, 1200000],
    }
    return pd.DataFrame(data)


def test_get_ohlcv_success(
    fast_settings: YahooFinanceSettings,
    mock_ohlcv_df: pd.DataFrame,
    mocker: MockerFixture,
) -> None:
    """Test successful OHLCV download and parsing."""
    mocker.patch("yfinance.download", return_value=mock_ohlcv_df)

    client = YahooFinanceClient(settings=fast_settings)
    res = client.get_ohlcv(ticker="AAPL")

    assert isinstance(res, OHLCVSeries)
    assert res.ticker == "AAPL"
    assert len(res.bars) == 2
    assert res.bars[0].open == 150.0
    assert res.bars[0].close == 153.0
    assert res.bars[0].volume == 1000000


def test_get_ohlcv_empty_dataframe(
    fast_settings: YahooFinanceSettings, mocker: MockerFixture
) -> None:
    """Test empty DataFrame from yfinance returns empty bars list."""
    empty_df = pd.DataFrame()
    mocker.patch("yfinance.download", return_value=empty_df)

    client = YahooFinanceClient(settings=fast_settings)
    res = client.get_ohlcv(ticker="UNKNOWN")

    assert isinstance(res, OHLCVSeries)
    assert res.bars == []


def test_get_quote_success(fast_settings: YahooFinanceSettings, mocker: MockerFixture) -> None:
    """Test successful ticker quote retrieval."""
    mock_info: dict[str, Any] = {
        "shortName": "Apple Inc.",
        "currentPrice": 150.0,
        "marketCap": 2500000000000,
        "currency": "USD",
        "exchange": "NMS",
        "quoteType": "EQUITY",
    }
    mock_ticker = MagicMock()
    mock_ticker.info = mock_info
    mocker.patch("yfinance.Ticker", return_value=mock_ticker)

    client = YahooFinanceClient(settings=fast_settings)
    res = client.get_quote(ticker="AAPL")

    assert isinstance(res, TickerQuote)
    assert res.ticker == "AAPL"
    assert res.short_name == "Apple Inc."
    assert res.current_price == 150.0
    assert res.market_cap == 2500000000000


def test_get_quote_missing_fields(
    fast_settings: YahooFinanceSettings, mocker: MockerFixture
) -> None:
    """Test quote parsing when optional fields are missing."""
    mock_info: dict[str, Any] = {"shortName": "Unknown Co"}
    mock_ticker = MagicMock()
    mock_ticker.info = mock_info
    mocker.patch("yfinance.Ticker", return_value=mock_ticker)

    client = YahooFinanceClient(settings=fast_settings)
    res = client.get_quote(ticker="UNKN")

    assert res.current_price is None
    assert res.market_cap is None


def test_network_error_raises(fast_settings: YahooFinanceSettings, mocker: MockerFixture) -> None:
    """Test exception in yfinance raises ExtractorError."""
    mocker.patch("yfinance.download", side_effect=Exception("Connection refused"))

    client = YahooFinanceClient(settings=fast_settings)
    with pytest.raises(ExtractorError):
        client.get_ohlcv(ticker="AAPL")


def test_invalid_ticker_raises(fast_settings: YahooFinanceSettings, mocker: MockerFixture) -> None:
    """Test empty info dictionary from Ticker raises APIResponseError."""
    mock_ticker = MagicMock()
    mock_ticker.info = {}
    mocker.patch("yfinance.Ticker", return_value=mock_ticker)

    client = YahooFinanceClient(settings=fast_settings)
    with pytest.raises(APIResponseError):
        client.get_quote(ticker="INVALID")


def test_retry_on_transient_error(
    fast_settings: YahooFinanceSettings,
    mock_ohlcv_df: pd.DataFrame,
    mocker: MockerFixture,
) -> None:
    """Test retry logic recovers after transient error."""
    mock_download = mocker.patch(
        "yfinance.download",
        side_effect=[Exception("Transient network issue"), mock_ohlcv_df],
    )

    client = YahooFinanceClient(settings=fast_settings)
    res = client.get_ohlcv(ticker="AAPL")

    assert len(res.bars) == 2
    assert mock_download.call_count == 2


def test_extractor_facade() -> None:
    """Test YahooFinanceExtractor facade delegates calls to client."""
    mock_client = MagicMock(spec=YahooFinanceClient)
    mock_client.get_ohlcv.return_value = OHLCVSeries(ticker="AAPL", interval="1d", bars=[])
    mock_client.get_quote.return_value = TickerQuote(ticker="AAPL")

    extractor = YahooFinanceExtractor(client=mock_client)
    res_ohlcv = extractor.extract_ohlcv(ticker="AAPL")
    res_quote = extractor.extract_quote(ticker="AAPL")

    assert res_ohlcv.ticker == "AAPL"
    assert res_quote.ticker == "AAPL"
    mock_client.get_ohlcv.assert_called_once_with(
        ticker="AAPL", start=None, end=None, interval=None
    )
    mock_client.get_quote.assert_called_once_with(ticker="AAPL")
