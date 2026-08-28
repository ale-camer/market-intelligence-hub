"""Global exception handlers for the FastAPI application."""

from typing import Any

from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse


def register_exception_handlers(app: FastAPI) -> None:
    """Register custom global exception handlers on the FastAPI app instance."""

    @app.exception_handler(Exception)
    async def global_exception_handler(request: Request, exc: Exception) -> JSONResponse:
        content: dict[str, Any] = {
            "error": "InternalServerError",
            "message": str(exc) or "An unexpected error occurred.",
            "path": str(request.url),
        }
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content=content,
        )
