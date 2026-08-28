"""Health check router for API monitoring."""

from typing import Any

from fastapi import APIRouter

from src.api.config import APIConfig

router = APIRouter(tags=["Health"])


@router.get("/health", response_model=dict[str, Any])
def health_check() -> dict[str, Any]:
    """Health check endpoint to verify system status and API availability."""
    return {
        "status": "ok",
        "app_name": APIConfig.APP_NAME,
        "version": APIConfig.VERSION,
    }
