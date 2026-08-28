"""FastAPI dependency injection providers."""

import os
from collections.abc import Generator

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer

from src.api.config import APIConfig
from src.api.security import decode_access_token
from src.loaders.postgres.repository import PostgresRepository

_repo_instance: PostgresRepository | None = None
oauth2_scheme = OAuth2PasswordBearer(tokenUrl=f"{APIConfig.API_PREFIX}/auth/token")


def get_postgres_repository() -> Generator[PostgresRepository, None, None]:
    """Dependency provider yielding a configured PostgresRepository instance."""
    global _repo_instance
    if _repo_instance is None:
        db_url = os.getenv("POSTGRES_URL", "sqlite:///:memory:")
        _repo_instance = PostgresRepository(database_url=db_url)
        _repo_instance.create_tables()
    yield _repo_instance


def get_current_user(token: str = Depends(oauth2_scheme)) -> str:
    """Validate bearer access token and return current authenticated user."""
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = decode_access_token(token)
        username: str | None = payload.get("sub")
        if username is None:
            raise credentials_exception
        return username
    except ValueError as err:
        raise credentials_exception from err
