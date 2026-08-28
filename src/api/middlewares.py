"""Custom middleware for rate limiting and request tracking."""

import time
from collections import defaultdict
from collections.abc import Awaitable, Callable

from fastapi import Request, Response, status
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.types import ASGIApp


class RateLimitMiddleware(BaseHTTPMiddleware):
    """Simple in-memory sliding window rate limiting middleware."""

    def __init__(self, app: ASGIApp, requests_per_minute: int = 60) -> None:
        super().__init__(app)
        self.requests_per_minute = requests_per_minute
        self.client_requests: dict[str, list[float]] = defaultdict(list)

    async def dispatch(
        self, request: Request, call_next: Callable[[Request], Awaitable[Response]]
    ) -> Response:
        # Exclude health check and docs from rate limiting
        path = request.url.path
        if path.endswith("/health") or path.startswith(("/docs", "/redoc", "/openapi.json")):
            return await call_next(request)

        client_ip = request.client.host if request.client else "unknown"
        now = time.time()
        window_start = now - 60.0

        # Clean old timestamps
        timestamps = [t for t in self.client_requests[client_ip] if t > window_start]
        self.client_requests[client_ip] = timestamps

        if len(timestamps) >= self.requests_per_minute:
            return JSONResponse(
                status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                content={
                    "error": "TooManyRequests",
                    "message": (
                        "Rate limit exceeded. "
                        f"Maximum {self.requests_per_minute} requests per minute allowed."
                    ),
                },
            )

        self.client_requests[client_ip].append(now)
        return await call_next(request)
