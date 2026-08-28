"""FastAPI application configuration settings."""

import os


class APIConfig:
    """Configuration class for the FastAPI application."""

    APP_NAME: str = os.getenv("API_APP_NAME", "Market Intelligence Hub API")
    VERSION: str = os.getenv("API_VERSION", "1.0.0")
    API_PREFIX: str = os.getenv("API_PREFIX", "/api/v1")
    CORS_ORIGINS: list[str] = os.getenv("API_CORS_ORIGINS", "*").split(",")
    HOST: str = os.getenv("API_HOST", "0.0.0.0")  # noqa: S104
    PORT: int = int(os.getenv("API_PORT", "8000"))
    SECRET_KEY: str = os.getenv("API_SECRET_KEY", "super-secret-key-change-in-production")
    ALGORITHM: str = os.getenv("API_ALGORITHM", "HS256")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = int(os.getenv("API_ACCESS_TOKEN_EXPIRE_MINUTES", "60"))
    RATE_LIMIT_PER_MINUTE: int = int(os.getenv("API_RATE_LIMIT_PER_MINUTE", "60"))
