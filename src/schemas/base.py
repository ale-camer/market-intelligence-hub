"""Base model configuration for canonical schemas."""

from datetime import UTC, datetime

from pydantic import BaseModel, ConfigDict, Field

from src.schemas.enums import DataSource


class BaseSchema(BaseModel):
    """Base schema for all domain models in the Market Intelligence Hub."""

    model_config = ConfigDict(
        frozen=True,
        populate_by_name=True,
        ser_json_timedelta="iso8601",
    )

    source: DataSource
    ingested_at: datetime = Field(default_factory=lambda: datetime.now(UTC))
