"""FastAPI dependency injection providers."""

import os
from collections.abc import Generator

from src.loaders.postgres.repository import PostgresRepository

_repo_instance: PostgresRepository | None = None


def get_postgres_repository() -> Generator[PostgresRepository, None, None]:
    """Dependency provider yielding a configured PostgresRepository instance."""
    global _repo_instance
    if _repo_instance is None:
        db_url = os.getenv("POSTGRES_URL", "sqlite:///:memory:")
        _repo_instance = PostgresRepository(database_url=db_url)
        _repo_instance.create_tables()
    yield _repo_instance
