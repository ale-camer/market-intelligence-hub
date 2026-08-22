# Issue #2 — Yahoo Finance Extractor

**Branch**: `feature/issue-2-yahoo-finance-extractor`
**Milestone**: M1 — Data Extraction
**Depends on**: Issue #1 ✅ (shared `exceptions.py` pattern)
**Status**: 🟡 In Progress

---

## Objective

Build a synchronous client that extracts stock and forex price data (OHLCV) using the `yfinance` library. The extractor must return Pydantic-validated models, handle errors gracefully, and be fully covered by unit tests (≥80%).

---

## yfinance Library — Target Operations

| Operation | Purpose | Auth Required |
|:----------|:--------|:-------------:|
| `yf.download(tickers, start, end, interval)` | Historical OHLCV for stocks/forex | ❌ |
| `yf.Ticker(symbol).info` | Current quote summary (price, market cap, etc.) | ❌ |

- **Library:** `yfinance` (wraps unofficial Yahoo Finance endpoints)
- **No API key required**
- **Rate Limit:** Unofficial; requires retry logic for HTTP 429
- **Forex tickers:** Use `EURUSD=X` format

---

## Module Architecture

```
src/extractors/
├── __init__.py                 # (existing)
├── exceptions.py               # (existing, shared)
├── coingecko/                  # (existing, Issue #1)
└── yahoo_finance/
    ├── __init__.py
    ├── config.py               # Settings (default tickers, period, interval)
    ├── client.py               # yfinance wrapper with retry logic
    ├── models.py               # Pydantic v2 response models
    └── extractor.py            # High-level extractor facade
```

---

## Checklist

### 🌿 Step 1 — Branch & Dependencies
- [ ] `git checkout develop`
- [ ] `git checkout -b feature/issue-2-yahoo-finance-extractor`
- [ ] `source .venv/bin/activate` — activate virtual environment
- [ ] Add `yfinance>=0.2.40` to `pyproject.toml` dependencies
- [ ] `pip install -e ".[dev]"` — install all dependencies
- [ ] Create `src/extractors/yahoo_finance/__init__.py`
- [ ] Verify: `python -c "import yfinance; print('OK')"`

### ⚙️ Step 2 — Configuration (`src/extractors/yahoo_finance/config.py`)
- [ ] `YahooFinanceSettings(BaseSettings)` with `env_prefix="YFINANCE_"`
- [ ] Fields: `default_interval` (`str`, default `"1d"`), `timeout_seconds` (`float`, default `30.0`), `max_retries` (`int`, default `3`)
- [ ] Verify: `ruff check src/extractors/yahoo_finance/config.py`
- [ ] Verify: `mypy src/extractors/yahoo_finance/config.py`

### 📦 Step 3 — Response Models (`src/extractors/yahoo_finance/models.py`)
- [ ] `OHLCVBar(BaseModel)` — single OHLCV bar
  - Fields: `date` (`datetime`), `open` (`float`), `high` (`float`), `low` (`float`), `close` (`float`), `volume` (`int`)
- [ ] `OHLCVSeries(BaseModel)` — list of bars for a ticker
  - Fields: `ticker` (`str`), `interval` (`str`), `bars` (`list[OHLCVBar]`)
- [ ] `TickerQuote(BaseModel)` — current quote info
  - Fields: `ticker` (`str`), `short_name` (`str | None`), `current_price` (`float | None`), `market_cap` (`int | None`), `currency` (`str | None`), `exchange` (`str | None`), `quote_type` (`str | None`)
- [ ] Verify: `ruff check src/extractors/yahoo_finance/models.py`
- [ ] Verify: `mypy src/extractors/yahoo_finance/models.py`

### 🌐 Step 4 — Client (`src/extractors/yahoo_finance/client.py`)
- [ ] `YahooFinanceClient` class wrapping `yfinance`
- [ ] Method: `get_ohlcv(ticker, start, end, interval) -> OHLCVSeries`
  - Uses `yf.download()` internally
  - Converts DataFrame rows to `OHLCVBar` list
- [ ] Method: `get_quote(ticker) -> TickerQuote`
  - Uses `yf.Ticker(ticker).info` internally
  - Maps relevant fields to `TickerQuote`
- [ ] Retry with `tenacity` on exceptions (network errors, rate limits)
- [ ] Structured logging with `structlog`
- [ ] Map errors → `ExtractorError`, `APIResponseError`
- [ ] Verify: `ruff check src/extractors/yahoo_finance/client.py`
- [ ] Verify: `mypy src/extractors/yahoo_finance/client.py`

### 🎯 Step 5 — Extractor Facade (`src/extractors/yahoo_finance/extractor.py`)
- [ ] `YahooFinanceExtractor` class — high-level API for consumers
- [ ] Method: `extract_ohlcv(ticker, start, end, interval) -> OHLCVSeries`
- [ ] Method: `extract_quote(ticker) -> TickerQuote`
- [ ] Delegates to `YahooFinanceClient`
- [ ] Verify: `ruff check src/extractors/yahoo_finance/extractor.py`
- [ ] Verify: `mypy src/extractors/yahoo_finance/extractor.py`

### 🧪 Step 6 — Unit Tests (`tests/unit/extractors/test_yahoo_finance.py`)
- [ ] `test_get_ohlcv_success` — mock `yf.download`, validate `OHLCVSeries` parsing
- [ ] `test_get_ohlcv_empty_dataframe` — empty DataFrame returns empty `bars`
- [ ] `test_get_quote_success` — mock `yf.Ticker().info`, validate `TickerQuote`
- [ ] `test_get_quote_missing_fields` — missing keys map to `None`
- [ ] `test_network_error_raises` — network exception → `ExtractorError`
- [ ] `test_invalid_ticker_raises` — invalid ticker → `APIResponseError`
- [ ] `test_retry_on_transient_error` — verify retry logic fires
- [ ] `test_extractor_facade` — `YahooFinanceExtractor` delegates correctly
- [ ] Mocking strategy: patch `yfinance.download` and `yfinance.Ticker` with fixtures
- [ ] Verify: `pytest tests/unit/extractors/test_yahoo_finance.py -v`

### ✅ Step 7 — Quality Gates
- [ ] `ruff check src/extractors/ tests/unit/extractors/` — passes
- [ ] `mypy src/extractors/` — passes (strict)
- [ ] `pytest tests/unit/extractors/ -v --cov=src/extractors --cov-report=term-missing` — ≥80% coverage
- [ ] All three gates green

### 🔀 Step 8 — Commit, Merge & Close
- [ ] `git add -A`
- [ ] `git commit -m "feat(extractors): Yahoo Finance extractor with OHLCV and quote support (#2)"`
- [ ] `git push origin feature/issue-2-yahoo-finance-extractor`
- [ ] `git checkout develop`
- [ ] `git merge --squash feature/issue-2-yahoo-finance-extractor`
- [ ] `git commit -m "feat(extractors): Yahoo Finance extractor (#2)"`
- [ ] `git push origin develop`
- [ ] `git branch -d feature/issue-2-yahoo-finance-extractor`
- [ ] Issue #2 closed on GitHub

---

## Design Notes

- **Synchronous client:** Unlike CoinGecko (`httpx.AsyncClient`), `yfinance` is synchronous (uses `requests` internally). The client wraps it directly; async adaptation can happen at the DAG level via `asyncio.to_thread()`.
- The existing `src/extractors/exceptions.py` is reused — no new exception classes needed.
- `yfinance.download()` returns a `pandas.DataFrame`, so the client must convert rows to Pydantic models. This is the only extractor with a pandas dependency in the data path.
- Forex tickers use the `EURUSD=X` format in Yahoo Finance.
- `yfinance` has no official rate limit documentation; retries with exponential backoff protect against transient failures.
