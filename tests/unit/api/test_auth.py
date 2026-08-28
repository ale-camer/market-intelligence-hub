"""Unit tests for Auth router, security utilities, and RateLimitMiddleware."""

import pytest
from fastapi.testclient import TestClient

from src.api.main import create_app
from src.api.security import (
    create_access_token,
    decode_access_token,
    get_password_hash,
    verify_password,
)


def test_password_hashing() -> None:
    """Test password hashing and verification."""
    password = "secretpassword"  # noqa: S105
    hashed = get_password_hash(password)
    assert verify_password(password, hashed)
    assert not verify_password("wrongpassword", hashed)


def test_jwt_token_roundtrip() -> None:
    """Test creating and decoding JWT access tokens."""
    payload = {"sub": "testuser"}
    token = create_access_token(payload)
    decoded = decode_access_token(token)
    assert decoded["sub"] == "testuser"


def test_jwt_invalid_token() -> None:
    """Test decoding an invalid JWT raises ValueError."""
    with pytest.raises(ValueError, match="Invalid or expired token"):
        decode_access_token("invalid.token.string")


def test_login_success() -> None:
    """Test login endpoint returning bearer token with valid credentials."""
    app = create_app()
    client = TestClient(app)

    response = client.post(
        "/api/v1/auth/token",
        data={"username": "admin", "password": "admin"},
    )
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"  # noqa: S105


def test_login_invalid_credentials() -> None:
    """Test login endpoint returning 401 Unauthorized for invalid credentials."""
    app = create_app()
    client = TestClient(app)

    response = client.post(
        "/api/v1/auth/token",
        data={"username": "admin", "password": "wrongpassword"},
    )
    assert response.status_code == 401


def test_rate_limit_exceeded() -> None:
    """Test rate limiting middleware triggers HTTP 429 when quota exceeded."""
    app = create_app()
    client = TestClient(app)

    # Fire multiple requests to test rate limit threshold
    for _ in range(60):
        client.get("/api/v1/market/quotes/BTC")

    # The 61st request should be blocked by RateLimitMiddleware
    response = client.get("/api/v1/market/quotes/BTC")
    assert response.status_code == 429
    assert "Rate limit exceeded" in response.json()["message"]
