"""FastAPI application factory module."""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.api.config import APIConfig
from src.api.exceptions import register_exception_handlers
from src.api.routers import health


def create_app() -> FastAPI:
    """Application factory for constructing and configuring the FastAPI instance."""
    app = FastAPI(
        title=APIConfig.APP_NAME,
        version=APIConfig.VERSION,
        docs_url="/docs",
        redoc_url="/redoc",
    )

    # Configure CORS middleware
    app.add_middleware(
        CORSMiddleware,
        allow_origins=APIConfig.CORS_ORIGINS,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Register global exception handlers
    register_exception_handlers(app)

    # Register routers
    app.include_router(health.router, prefix=APIConfig.API_PREFIX)
    app.include_router(health.router)  # Also include root-level /health

    return app


app = create_app()
