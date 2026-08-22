# Issue #4 — Pydantic v2 Schemas

**Branch**: `feature/issue-4-pydantic-schemas`
**Milestone**: M1 — Data Extraction
**Depends on**: Issues #1 ✅, #2 ✅, #3 ✅
**Status**: 🟡 Not Started

---

## Objective

Create a **unified schemas layer** (`src/schemas/`) that defines source-agnostic, canonical data models for the entire pipeline. These models normalize outputs from CoinGecko, Yahoo Finance, and NewsAPI extractors into a consistent format used by downstream transformers, storage loaders, and APIs.

---

## Why a Unified Schema Layer?

Each extractor returns source-specific models (e.g. `CoinMarketData`, `OHLCVSeries`, `NewsArticle`). While these are valid for the extraction phase, downstream consumers (dbt models, BigQuery loaders, API endpoints) need a consistent interface:

| Extractor Model | Canonical Schema |
|:----------------|:-----------------|
| `CoinMarketData` | `MarketQuote` |
| `MarketChartData` | `PriceHistory` |
| `OHLCVBar` / `OHLCVSeries` | `PriceHistory` |
| `TickerQuote` | `MarketQuote` |
| `NewsArticle` / `NewsResponse` | `FinancialArticle` |

---

## Module Architecture

```
src/schemas/
├── __init__.py                 # Exports all canonical schemas
├── base.py                     # Shared base model config
├── market.py                   # Market data schemas (quotes, OHLCV, price history)
├── news.py                     # Financial news article schemas
└── enums.py                    # Shared enumerations (AssetClass, DataSource, etc.)

tests/unit/schemas/
├── __init__.py
├── test_market.py              # Tests for market schemas
└── test_news.py                # Tests for news schemas
```

---

## Checklist

### 🌿 Step 1 — Branch & Setup
- [ ] `git checkout develop`
- [ ] `git checkout -b feature/issue-4-pydantic-schemas`
- [ ] Create `src/schemas/__init__.py`
- [ ] Create `tests/unit/schemas/__init__.py`

### 📋 Step 2 — Enumerations (`src/schemas/enums.py`)
- [ ] `DataSource(str, Enum)` — `COINGECKO`, `YAHOO_FINANCE`, `NEWSAPI`
- [ ] `AssetClass(str, Enum)` — `CRYPTO`, `EQUITY`, `FOREX`, `ETF`
- [ ] Verify: `ruff format src/schemas/enums.py && ruff check src/schemas/enums.py --fix && mypy src/schemas/enums.py`

### 🧱 Step 3 — Base Model (`src/schemas/base.py`)
- [ ] `BaseSchema(BaseModel)` — shared config for all canonical schemas
  - `model_config = ConfigDict(frozen=True, populate_by_name=True, ser_json_timedelta="iso8601")`
  - Common fields: `source` (`DataSource`), `ingested_at` (`datetime`, default factory `datetime.utcnow`)
- [ ] Verify: `ruff format src/schemas/base.py && ruff check src/schemas/base.py --fix && mypy src/schemas/base.py`

### 📈 Step 4 — Market Schemas (`src/schemas/market.py`)
- [ ] `MarketQuote(BaseSchema)` — normalized quote for any asset
  - Fields: `ticker` (`str`), `asset_class` (`AssetClass`), `name` (`str | None`), `current_price` (`float | None`), `market_cap` (`int | None`), `volume_24h` (`float | None`), `currency` (`str`), `exchange` (`str | None`), `price_change_pct_24h` (`float | None`)
- [ ] `PriceBar(BaseSchema)` — single OHLCV bar, source-agnostic
  - Fields: `ticker` (`str`), `asset_class` (`AssetClass`), `dt` (`datetime`), `open` (`float`), `high` (`float`), `low` (`float`), `close` (`float`), `volume` (`float`)
- [ ] `PriceHistory(BaseSchema)` — time series of price bars
  - Fields: `ticker` (`str`), `asset_class` (`AssetClass`), `interval` (`str`), `bars` (`list[PriceBar]`)
- [ ] Verify: `ruff format src/schemas/market.py && ruff check src/schemas/market.py --fix && mypy src/schemas/market.py`

### 📰 Step 5 — News Schemas (`src/schemas/news.py`)
- [ ] `FinancialArticle(BaseSchema)` — normalized news article
  - Fields: `title` (`str`), `description` (`str | None`), `url` (`str`), `image_url` (`str | None`), `author` (`str | None`), `published_at` (`datetime`), `content` (`str | None`), `source_name` (`str`), `source_id` (`str | None`), `category` (`str | None`)
- [ ] Verify: `ruff format src/schemas/news.py && ruff check src/schemas/news.py --fix && mypy src/schemas/news.py`

### 📦 Step 6 — Module Exports (`src/schemas/__init__.py`)
- [ ] Export all schemas and enums from `__init__.py`
- [ ] Verify: `python -c "from src.schemas import MarketQuote, PriceHistory, FinancialArticle; print('OK')"`

### 🧪 Step 7 — Unit Tests (`tests/unit/schemas/`)
- [ ] `test_market.py`:
  - `test_market_quote_creation` — instantiate with all fields, verify frozen
  - `test_market_quote_defaults` — verify `None` defaults and `ingested_at` auto-set
  - `test_price_bar_creation` — instantiate a single bar
  - `test_price_history_creation` — create history with bar list
  - `test_market_quote_frozen` — attempt mutation raises `ValidationError`
- [ ] `test_news.py`:
  - `test_financial_article_creation` — instantiate with all fields
  - `test_financial_article_defaults` — verify `None` defaults
  - `test_financial_article_frozen` — mutation raises `ValidationError`
- [ ] Verify: `pytest tests/unit/schemas/ -v`

### ✅ Step 8 — Quality Gates
- [ ] `ruff format src/schemas/ tests/unit/schemas/` — no reformats
- [ ] `ruff check src/schemas/ tests/unit/schemas/` — passes
- [ ] `mypy src/schemas/` — passes (strict)
- [ ] `pytest tests/unit/schemas/ -v --cov=src/schemas --cov-report=term-missing` — ≥80% coverage
- [ ] All four gates green

### 🔀 Step 9 — Commit, Merge & Close
- [ ] `git add -A`
- [ ] `git commit -m "feat(schemas): unified Pydantic v2 canonical schemas for market and news data (#4)"`
- [ ] `git push origin feature/issue-4-pydantic-schemas`
- [ ] `git checkout develop`
- [ ] `git merge --squash feature/issue-4-pydantic-schemas`
- [ ] `git commit -m "feat(schemas): Pydantic v2 Schemas (#4)"`
- [ ] `git push origin develop`
- [ ] `git branch -d feature/issue-4-pydantic-schemas`
- [ ] Issue #4 closed on GitHub

---

## Design Notes

- **Separation of concerns**: Extractor models (`src/extractors/*/models.py`) remain source-specific and map 1:1 to API responses. Canonical schemas (`src/schemas/`) are the shared contract for the rest of the pipeline.
- **`BaseSchema`** provides `source` and `ingested_at` as common metadata on every record, enabling lineage tracking.
- **Enums** provide type-safe classification of data sources and asset classes, enabling filtering and routing in transformers/loaders.
- **Frozen models**: All schemas are immutable (`frozen=True`), ensuring data integrity across the pipeline.
- The mapping logic from extractor models → canonical schemas will be implemented in Issue #6+ (dbt/transformation layer). This issue only defines the target schemas.
