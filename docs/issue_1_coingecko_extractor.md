# Issue #1 — CoinGecko Extractor

**Branch**: `feature/issue-1-coingecko-extractor`
**Milestone**: M1 — Data Extraction
**Depends on**: Issue #0 ✅
**Status**: 🟡 In Progress

---

## Objective

Build an async HTTP client that extracts crypto market data from the CoinGecko API v3 (Demo/Free tier). The extractor must return Pydantic-validated models, handle errors gracefully, and be fully covered by unit tests (≥80%).

---

## CoinGecko API — Target Endpoints

| Endpoint | Purpose | Free Tier |
|:---------|:--------|:---------:|
| `GET /coins/markets` | Current prices, market cap, volume for a list of coins | ✅ |
| `GET /coins/{id}/market_chart` | Historical price, market cap, volume (up to 1 year) | ✅ |

- **Base URL (Demo):** `https://api.coingecko.com/api/v3`
- **Rate Limit:** 100 calls/min, 10,000 calls/month
- **Auth:** Optional demo API key via `x-cg-demo-api-key` header

---

## Module Architecture

```
src/extractors/
├── __init__.py
├── coingecko/
│   ├── __init__.py
│   ├── config.py          # Settings (base URL, API key, timeouts, retries)
│   ├── client.py          # Async HTTP client (httpx) with retry logic
│   ├── models.py          # Pydantic v2 response models
│   └── extractor.py       # High-level extractor (orchestrates client + models)
└── exceptions.py          # Shared extractor exceptions
```

---

## Checklist

### 🌿 Step 1 — Branch & Dependencies
- [ ] `git checkout develop`
- [ ] `git checkout -b feature/issue-1-coingecko-extractor`
- [ ] `source .venv/bin/activate` — activate virtual environment
- [ ] Add `tenacity>=8.3.0` to `pyproject.toml` dependencies
- [ ] `pip install -e ".[dev]"` — install all dependencies
- [ ] Create `src/extractors/__init__.py`
- [ ] Create `src/extractors/coingecko/__init__.py`
- [ ] Verify: `python -c "import httpx, pydantic, structlog, tenacity; print('OK')"`

### 🚨 Step 2 — Shared Exceptions (`src/extractors/exceptions.py`)
- [ ] `ExtractorError(Exception)` — base exception for all extractors
- [ ] `RateLimitError(ExtractorError)` — HTTP 429
- [ ] `APIResponseError(ExtractorError)` — unexpected API response
- [ ] Verify: `ruff check src/extractors/exceptions.py`

### ⚙️ Step 3 — Configuration (`src/extractors/coingecko/config.py`)
- [ ] `CoinGeckoSettings(BaseSettings)` with `env_prefix="COINGECKO_"`
- [ ] Fields: `api_key`, `base_url`, `timeout_seconds`, `max_retries`, `retry_wait_seconds`
- [ ] All fields have sensible defaults (no key required for demo)
- [ ] Verify: `ruff check src/extractors/coingecko/config.py`
- [ ] Verify: `mypy src/extractors/coingecko/config.py`

### 📦 Step 4 — Response Models (`src/extractors/coingecko/models.py`)
- [ ] `CoinMarketData(BaseModel)` — maps `/coins/markets` items
  - Fields: `id`, `symbol`, `name`, `current_price`, `market_cap`, `market_cap_rank`, `total_volume`, `high_24h`, `low_24h`, `price_change_24h`, `price_change_percentage_24h`, `last_updated`
- [ ] `MarketChartData(BaseModel)` — maps `/coins/{id}/market_chart`
  - Fields: `prices`, `market_caps`, `total_volumes` (each `list[tuple[int, float]]`)
- [ ] Verify: `ruff check src/extractors/coingecko/models.py`
- [ ] Verify: `mypy src/extractors/coingecko/models.py`

### 🌐 Step 5 — Async HTTP Client (`src/extractors/coingecko/client.py`)
- [ ] `CoinGeckoClient` class wrapping `httpx.AsyncClient`
- [ ] Inject `x-cg-demo-api-key` header when API key is present
- [ ] Configurable timeout from `CoinGeckoSettings`
- [ ] Retry with `tenacity` on HTTP 429, 500, 502, 503, 504
- [ ] Structured logging with `structlog` (request URL, status, duration)
- [ ] Map HTTP errors → custom exceptions (`RateLimitError`, `APIResponseError`)
- [ ] Method: `get_coins_markets(vs_currency, ids, per_page, page) -> list[CoinMarketData]`
- [ ] Method: `get_coin_market_chart(coin_id, vs_currency, days) -> MarketChartData`
- [ ] Async context manager support (`async with`)
- [ ] Verify: `ruff check src/extractors/coingecko/client.py`
- [ ] Verify: `mypy src/extractors/coingecko/client.py`

### 🎯 Step 6 — Extractor Facade (`src/extractors/coingecko/extractor.py`)
- [ ] `CoinGeckoExtractor` class — high-level API for consumers
- [ ] Method: `extract_market_data(coin_ids, vs_currency) -> list[CoinMarketData]`
- [ ] Method: `extract_price_history(coin_id, days, vs_currency) -> MarketChartData`
- [ ] Initializes `CoinGeckoClient` internally from settings
- [ ] Verify: `ruff check src/extractors/coingecko/extractor.py`
- [ ] Verify: `mypy src/extractors/coingecko/extractor.py`

### 🧪 Step 7 — Unit Tests (`tests/unit/extractors/test_coingecko.py`)
- [ ] Create `tests/unit/extractors/__init__.py`
- [ ] `test_get_coins_markets_success` — mock 200, validate Pydantic parsing
- [ ] `test_get_coins_markets_empty` — empty list response returns `[]`
- [ ] `test_get_coin_market_chart_success` — happy path for historical data
- [ ] `test_rate_limit_raises` — HTTP 429 → `RateLimitError`
- [ ] `test_server_error_raises` — HTTP 500 → `APIResponseError`
- [ ] `test_retry_on_transient_error` — retry fires on 503, then succeeds
- [ ] `test_timeout_raises` — `httpx.TimeoutException` → `ExtractorError`
- [ ] `test_api_key_header_injected` — header present when key is set
- [ ] `test_api_key_header_absent` — no header when key is empty
- [ ] `test_extractor_facade` — `CoinGeckoExtractor` delegates correctly
- [ ] Mocking strategy: patch `httpx.AsyncClient` with pre-built JSON fixtures
- [ ] Verify: `pytest tests/unit/extractors/ -v`

### ✅ Step 8 — Quality Gates
- [ ] `ruff check src/extractors/ tests/unit/extractors/` — passes
- [ ] `mypy src/extractors/` — passes (strict)
- [ ] `pytest tests/unit/extractors/ -v --cov=src/extractors --cov-report=term-missing` — ≥80% coverage
- [ ] All three gates green

### 🔀 Step 9 — Commit, Merge & Close
- [ ] `git add -A`
- [ ] `git commit -m "feat(extractors): CoinGecko async extractor with retry and Pydantic models (#1)"`
- [ ] `git push origin feature/issue-1-coingecko-extractor`
- [ ] `git checkout develop`
- [ ] `git merge --squash feature/issue-1-coingecko-extractor`
- [ ] `git commit -m "feat(extractors): CoinGecko extractor (#1)"`
- [ ] `git push origin develop`
- [ ] `git branch -d feature/issue-1-coingecko-extractor`
- [ ] Issue #1 closed on GitHub

---

## Design Notes

- The Pydantic schemas here are **response models** (API → Python). Issue #4 will define the **domain schemas** used downstream by loaders and transformers.
- The extractor is **async** from day one — Airflow DAGs (Issue #9) can call it via `asyncio.run()`.
- `tenacity` is preferred over manual retry loops for clean exponential backoff + jitter.
- All nullable fields in `CoinMarketData` have `None` defaults — CoinGecko may omit fields for less popular coins.
