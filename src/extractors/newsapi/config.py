"""Configuration settings for NewsAPI client."""

from pydantic_settings import BaseSettings, SettingsConfigDict


class NewsAPISettings(BaseSettings):
    """NewsAPI extractor configuration loaded from environment variables."""

    model_config = SettingsConfigDict(
        env_prefix="NEWSAPI_",
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    api_key: str = ""
    base_url: str = "https://newsapi.org/v2"
    timeout_seconds: float = 30.0
    max_retries: int = 3
    retry_wait_seconds: float = 2.0
    page_size: int = 100
