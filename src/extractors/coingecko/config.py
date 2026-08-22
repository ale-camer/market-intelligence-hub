"""Configuration settings for CoinGecko API client."""

from pydantic_settings import BaseSettings, SettingsConfigDict


class CoinGeckoSettings(BaseSettings):
    """CoinGecko API configuration loaded from environment variables."""

    model_config = SettingsConfigDict(
        env_prefix="COINGECKO_",
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    api_key: str = ""
    base_url: str = "https://api.coingecko.com/api/v3"
    timeout_seconds: float = 30.0
    max_retries: int = 3
    retry_wait_seconds: float = 2.0
