# Data Dictionary

This document describes the structure and schemas of the Market Intelligence Hub data warehouse.

## 1. Raw Layer

The `raw` schema contains data exactly as extracted from the source systems (CoinGecko, Yahoo Finance, NewsAPI) without any transformations.

### Table: `market_quotes_raw`
Contains raw snapshots of market prices and volumes.
- `id` (String/UUID): Primary key.
- `ticker` (String): The financial instrument identifier (e.g., 'BTC', 'AAPL').
- `source` (String): Source of the data ('coingecko', 'yahoo').
- `price` (Float): Current price of the asset.
- `volume_24h` (Float): Trading volume in the last 24 hours.
- `market_cap` (Float): Market capitalization.
- `ingested_at` (Timestamp): When the record was fetched.

### Table: `news_articles_raw`
Contains raw financial news articles.
- `id` (String/UUID): Primary key.
- `title` (String): Article title.
- `description` (Text): Short summary.
- `content` (Text): Full article content (if available).
- `url` (String): Original source URL.
- `source_name` (String): Publisher (e.g., 'Bloomberg', 'Reuters').
- `published_at` (Timestamp): Original publication date.
- `ingested_at` (Timestamp): When the record was fetched.

---

## 2. Staging Layer

The `staging` models (managed by dbt) clean and standardize the raw tables. Field names are normalized, timestamps are cast to standard UTC, and duplicates are deduplicated.

### Model: `stg_market_quotes`
Standardized market quotes.
- `quote_id` (String): Surrogate key (hash of ticker + source + timestamp).
- `asset_symbol` (String): Standardized ticker symbol.
- `data_source` (String): Standardized source name.
- `usd_price` (Float): Price normalized to USD.
- `usd_volume_24h` (Float): Volume normalized to USD.
- `usd_market_cap` (Float): Market cap normalized to USD.
- `recorded_at` (Timestamp): Equivalent to `ingested_at`.

### Model: `stg_news_articles`
Standardized news data.
- `article_id` (String): Surrogate key.
- `headline` (String): Cleaned title.
- `summary` (Text): Cleaned description.
- `publisher` (String): Cleaned source name.
- `published_timestamp_utc` (Timestamp): Cast to UTC timezone.

---

## 3. Marts Layer

The `marts` schema exposes dimension and fact tables ready for business consumption, BI, and APIs.

### Table: `dim_assets`
Unique list of tracked financial assets.
- `asset_id` (String): Primary key (hash of asset_symbol).
- `asset_symbol` (String): Ticker (e.g., 'BTC').
- `asset_type` (String): Category ('crypto', 'stock').
- `first_tracked_at` (Timestamp): Date when the asset was first ingested.

### Table: `fact_market_snapshots`
Aggregated hourly/daily snapshots of market quotes.
- `snapshot_id` (String): Primary key.
- `asset_id` (String): Foreign key to `dim_assets`.
- `snapshot_timestamp` (Timestamp): Time of the snapshot (truncated to hour/day).
- `avg_price_usd` (Float): Average price in the time window.
- `total_volume_usd` (Float): Total volume in the time window.

### Table: `fact_news_sentiment`
*(To be populated by NLP service)*
Financial news enriched with sentiment analysis.
- `article_id` (String): Foreign key to `stg_news_articles`.
- `asset_id` (String): Foreign key to `dim_assets` (if article mentions specific asset).
- `sentiment_score` (Float): Continuous score [-1.0, 1.0].
- `sentiment_label` (String): 'Positive', 'Negative', 'Neutral'.
