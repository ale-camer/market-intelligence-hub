"""FastAPI application factory module."""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.api.config import APIConfig
from src.api.exceptions import register_exception_handlers
from src.api.middlewares import RateLimitMiddleware
from src.api.routers import auth, health, market, news


def create_app() -> FastAPI:
    """Application factory for constructing and configuring the FastAPI instance."""
    app = FastAPI(
        title=APIConfig.APP_NAME,
        version=APIConfig.VERSION,
        docs_url="/docs",
        redoc_url="/redoc",
    )

    # Configure CORS and Rate Limit middlewares
    app.add_middleware(
        CORSMiddleware,
        allow_origins=APIConfig.CORS_ORIGINS,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    app.add_middleware(
        RateLimitMiddleware,
        requests_per_minute=APIConfig.RATE_LIMIT_PER_MINUTE,
    )

    # Register global exception handlers
    register_exception_handlers(app)

    # Register routers
    app.include_router(health.router, prefix=APIConfig.API_PREFIX)
    app.include_router(health.router)  # Also include root-level /health
    app.include_router(auth.router, prefix=APIConfig.API_PREFIX)
    app.include_router(market.router, prefix=APIConfig.API_PREFIX)
    app.include_router(news.router, prefix=APIConfig.API_PREFIX)

    return app


app = create_app()
