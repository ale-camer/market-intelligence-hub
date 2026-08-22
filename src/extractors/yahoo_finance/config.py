"""Configuration settings for Yahoo Finance API client."""

from pydantic_settings import BaseSettings, SettingsConfigDict


class YahooFinanceSettings(BaseSettings):
    """Yahoo Finance extractor configuration loaded from environment variables."""

    model_config = SettingsConfigDict(
        env_prefix="YFINANCE_",
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    default_interval: str = "1d"
    timeout_seconds: float = 30.0
    max_retries: int = 3
