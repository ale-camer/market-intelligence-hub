"""Repository pattern implementation for GCP BigQuery loads."""

import pandas as pd
from google.cloud import bigquery

from src.loaders.bigquery.client import BigQueryClient
from src.loaders.bigquery.schemas import (
    FINANCIAL_NEWS_SCHEMA,
    MARKET_QUOTES_SCHEMA,
    PRICE_HISTORY_SCHEMA,
)


class BigQueryRepository:
    """Repository class for executing BigQuery DDL and Load Jobs."""

    def __init__(self, bq_client: BigQueryClient | None = None) -> None:
        """Initialize repository with BigQueryClient instance."""
        self.bq_client = bq_client or BigQueryClient()

    def create_tables_if_not_exist(self) -> None:
        """Ensure BigQuery dataset and target tables exist with proper schemas and partitioning."""
        client = self.bq_client.client
        dataset_ref = self.bq_client.dataset_ref

        # Create dataset if missing
        dataset = bigquery.Dataset(dataset_ref)
        dataset.location = "US"
        client.create_dataset(dataset, exists_ok=True)

        # 1. market_quotes table
        table_ref = self.bq_client.get_table_ref("market_quotes")
        table = bigquery.Table(table_ref, schema=MARKET_QUOTES_SCHEMA)
        table.time_partitioning = bigquery.TimePartitioning(
            type_=bigquery.TimePartitioningType.DAY, field="ingested_at"
        )
        client.create_table(table, exists_ok=True)

        # 2. financial_news table
        news_table_ref = self.bq_client.get_table_ref("financial_news")
        news_table = bigquery.Table(news_table_ref, schema=FINANCIAL_NEWS_SCHEMA)
        news_table.time_partitioning = bigquery.TimePartitioning(
            type_=bigquery.TimePartitioningType.DAY, field="published_at"
        )
        client.create_table(news_table, exists_ok=True)

        # 3. price_bars table
        price_table_ref = self.bq_client.get_table_ref("price_bars")
        price_table = bigquery.Table(price_table_ref, schema=PRICE_HISTORY_SCHEMA)
        price_table.time_partitioning = bigquery.TimePartitioning(
            type_=bigquery.TimePartitioningType.DAY, field="dt"
        )
        client.create_table(price_table, exists_ok=True)

    def load_market_quotes_from_dataframe(self, df: pd.DataFrame) -> bigquery.LoadJob:
        """Load market quotes DataFrame into BigQuery table via Load Job."""
        table_ref = self.bq_client.get_table_ref("market_quotes")
        job_config = bigquery.LoadJobConfig(
            schema=MARKET_QUOTES_SCHEMA,
            write_disposition=bigquery.WriteDisposition.WRITE_APPEND,
        )
        return self.bq_client.client.load_table_from_dataframe(df, table_ref, job_config=job_config)

    def load_news_articles_from_dataframe(self, df: pd.DataFrame) -> bigquery.LoadJob:
        """Load financial news DataFrame into BigQuery table via Load Job."""
        table_ref = self.bq_client.get_table_ref("financial_news")
        job_config = bigquery.LoadJobConfig(
            schema=FINANCIAL_NEWS_SCHEMA,
            write_disposition=bigquery.WriteDisposition.WRITE_APPEND,
        )
        return self.bq_client.client.load_table_from_dataframe(df, table_ref, job_config=job_config)

    def load_price_bars_from_dataframe(self, df: pd.DataFrame) -> bigquery.LoadJob:
        """Load OHLCV price history DataFrame into BigQuery table via Load Job."""
        table_ref = self.bq_client.get_table_ref("price_bars")
        job_config = bigquery.LoadJobConfig(
            schema=PRICE_HISTORY_SCHEMA,
            write_disposition=bigquery.WriteDisposition.WRITE_APPEND,
        )
        return self.bq_client.client.load_table_from_dataframe(df, table_ref, job_config=job_config)
