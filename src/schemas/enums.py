"""Domain enumerations for Market Intelligence Hub schemas."""

from enum import StrEnum


class DataSource(StrEnum):
    """Supported data ingestion sources."""

    COINGECKO = "coingecko"
    YAHOO_FINANCE = "yahoo_finance"
    NEWSAPI = "newsapi"


class AssetClass(StrEnum):
    """Supported financial asset classes."""

    CRYPTO = "crypto"
    EQUITY = "equity"
    FOREX = "forex"
    ETF = "etf"
