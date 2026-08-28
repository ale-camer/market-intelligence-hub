"""BigQuery schema definitions for market quotes, news, and price history tables."""

from google.cloud import bigquery

MARKET_QUOTES_SCHEMA: list[bigquery.SchemaField] = [
    bigquery.SchemaField("source", "STRING", mode="REQUIRED"),
    bigquery.SchemaField("ticker", "STRING", mode="REQUIRED"),
    bigquery.SchemaField("asset_class", "STRING", mode="REQUIRED"),
    bigquery.SchemaField("name", "STRING", mode="NULLABLE"),
    bigquery.SchemaField("current_price", "FLOAT64", mode="NULLABLE"),
    bigquery.SchemaField("market_cap", "INT64", mode="NULLABLE"),
    bigquery.SchemaField("volume_24h", "FLOAT64", mode="NULLABLE"),
    bigquery.SchemaField("currency", "STRING", mode="REQUIRED"),
    bigquery.SchemaField("exchange", "STRING", mode="NULLABLE"),
    bigquery.SchemaField("price_change_pct_24h", "FLOAT64", mode="NULLABLE"),
    bigquery.SchemaField("ingested_at", "TIMESTAMP", mode="REQUIRED"),
]

FINANCIAL_NEWS_SCHEMA: list[bigquery.SchemaField] = [
    bigquery.SchemaField("source", "STRING", mode="REQUIRED"),
    bigquery.SchemaField("title", "STRING", mode="REQUIRED"),
    bigquery.SchemaField("description", "STRING", mode="NULLABLE"),
    bigquery.SchemaField("url", "STRING", mode="REQUIRED"),
    bigquery.SchemaField("article_url", "STRING", mode="NULLABLE"),
    bigquery.SchemaField("image_url", "STRING", mode="NULLABLE"),
    bigquery.SchemaField("author", "STRING", mode="NULLABLE"),
    bigquery.SchemaField("published_at", "TIMESTAMP", mode="REQUIRED"),
    bigquery.SchemaField("content", "STRING", mode="NULLABLE"),
    bigquery.SchemaField("source_name", "STRING", mode="REQUIRED"),
    bigquery.SchemaField("source_id", "STRING", mode="NULLABLE"),
    bigquery.SchemaField("category", "STRING", mode="NULLABLE"),
    bigquery.SchemaField("ingested_at", "TIMESTAMP", mode="REQUIRED"),
]

PRICE_HISTORY_SCHEMA: list[bigquery.SchemaField] = [
    bigquery.SchemaField("source", "STRING", mode="REQUIRED"),
    bigquery.SchemaField("ticker", "STRING", mode="REQUIRED"),
    bigquery.SchemaField("asset_class", "STRING", mode="REQUIRED"),
    bigquery.SchemaField("dt", "TIMESTAMP", mode="REQUIRED"),
    bigquery.SchemaField("open", "FLOAT64", mode="REQUIRED"),
    bigquery.SchemaField("high", "FLOAT64", mode="REQUIRED"),
    bigquery.SchemaField("low", "FLOAT64", mode="REQUIRED"),
    bigquery.SchemaField("close", "FLOAT64", mode="REQUIRED"),
    bigquery.SchemaField("volume", "FLOAT64", mode="REQUIRED"),
    bigquery.SchemaField("ingested_at", "TIMESTAMP", mode="REQUIRED"),
]
