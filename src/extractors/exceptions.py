"""Custom exceptions for data extractors."""


class ExtractorError(Exception):
    """Base exception for all extractors."""


class RateLimitError(ExtractorError):
    """Raised when API rate limit is exceeded (HTTP 429)."""


class APIResponseError(ExtractorError):
    """Raised when API returns an unexpected response."""
