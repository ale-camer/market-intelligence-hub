"""Unit tests for BigQuery client and repository using mocks."""

from unittest.mock import MagicMock

import pandas as pd
import pytest

from src.loaders.bigquery.client import BigQueryClient
from src.loaders.bigquery.repository import BigQueryRepository


@pytest.fixture
def mock_bq_client() -> MagicMock:
    """Fixture providing a mocked google.cloud.bigquery.Client."""
    mock_client = MagicMock()
    mock_client.dataset.return_value = MagicMock()
    return mock_client


@pytest.fixture
def bq_repository(mock_bq_client: MagicMock) -> BigQueryRepository:
    """Fixture providing a BigQueryRepository configured with a mocked client."""
    client_wrapper = BigQueryClient(
        project_id="test-project", dataset_id="test_dataset", client=mock_bq_client
    )
    return BigQueryRepository(bq_client=client_wrapper)


def test_bigquery_client_properties(mock_bq_client: MagicMock) -> None:
    """Test BigQueryClient initialization and property attributes."""
    client_wrapper = BigQueryClient(
        project_id="my-gcp-project", dataset_id="my_dataset", client=mock_bq_client
    )
    assert client_wrapper.project_id == "my-gcp-project"
    assert client_wrapper.dataset_id == "my_dataset"
    _ = client_wrapper.dataset_ref
    mock_bq_client.dataset.assert_called_with("my_dataset")


def test_create_tables_if_not_exist(
    bq_repository: BigQueryRepository, mock_bq_client: MagicMock
) -> None:
    """Test dataset and table DDL creation calls."""
    bq_repository.create_tables_if_not_exist()
    assert mock_bq_client.create_dataset.called
    assert mock_bq_client.create_table.call_count == 3


def test_load_market_quotes_from_dataframe(
    bq_repository: BigQueryRepository, mock_bq_client: MagicMock
) -> None:
    """Test load_market_quotes_from_dataframe invoking load_table_from_dataframe."""
    df = pd.DataFrame(
        [
            {
                "source": "coingecko",
                "ticker": "BTC",
                "asset_class": "crypto",
                "current_price": 50000.0,
                "currency": "USD",
                "ingested_at": "2026-01-01T00:00:00Z",
            }
        ]
    )

    bq_repository.load_market_quotes_from_dataframe(df)
    mock_bq_client.load_table_from_dataframe.assert_called_once()


def test_load_news_articles_from_dataframe(
    bq_repository: BigQueryRepository, mock_bq_client: MagicMock
) -> None:
    """Test load_news_articles_from_dataframe invoking load_table_from_dataframe."""
    df = pd.DataFrame(
        [
            {
                "source": "newsapi",
                "title": "Crypto Surge",
                "url": "https://example.com",
                "published_at": "2026-01-01T00:00:00Z",
                "source_name": "Reuters",
                "ingested_at": "2026-01-01T00:00:00Z",
            }
        ]
    )

    bq_repository.load_news_articles_from_dataframe(df)
    mock_bq_client.load_table_from_dataframe.assert_called_once()


def test_load_price_bars_from_dataframe(
    bq_repository: BigQueryRepository, mock_bq_client: MagicMock
) -> None:
    """Test load_price_bars_from_dataframe invoking load_table_from_dataframe."""
    df = pd.DataFrame(
        [
            {
                "source": "yahoo_finance",
                "ticker": "AAPL",
                "asset_class": "equity",
                "dt": "2026-01-01T00:00:00Z",
                "open": 150.0,
                "high": 155.0,
                "low": 149.0,
                "close": 154.0,
                "volume": 1000.0,
                "ingested_at": "2026-01-01T00:00:00Z",
            }
        ]
    )

    bq_repository.load_price_bars_from_dataframe(df)
    mock_bq_client.load_table_from_dataframe.assert_called_once()
