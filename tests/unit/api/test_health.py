"""Unit tests for FastAPI application setup and health check router."""

from fastapi.testclient import TestClient

from src.api.main import create_app


def test_health_check_endpoint() -> None:
    """Test health check returns HTTP 200 and expected payload."""
    app = create_app()
    client = TestClient(app)

    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "ok"
    assert "version" in data

    # Test prefixed health route
    prefixed_response = client.get("/api/v1/health")
    assert prefixed_response.status_code == 200
    assert prefixed_response.json()["status"] == "ok"
