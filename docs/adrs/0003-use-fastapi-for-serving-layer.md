# ADR 0003: Use FastAPI for Serving Layer

## Status
Accepted

## Context
Once data is processed and stored in the data marts, we need a way to serve this data securely to external clients, dashboards, and internal applications. The framework needs to be performant, easy to develop, and support modern asynchronous Python capabilities.

## Decision
We decided to use **FastAPI** for building the Data Serving API.

## Consequences
- **Positive:**
  - High performance due to asynchronous support (Starlette).
  - Automatic interactive API documentation (Swagger UI/ReDoc) using OpenAPI.
  - Strict data validation and serialization out-of-the-box via Pydantic.
  - Quick to develop and highly Pythonic.
- **Negative:**
  - Newer ecosystem compared to Django/Flask.
  - Requires developers to be comfortable with `async`/`await` paradigms to avoid blocking the event loop.
