# Issue #3 — NewsAPI Extractor

**Branch**: `feature/issue-3-newsapi-extractor`
**Milestone**: M1 — Data Extraction
**Depends on**: Issue #1 ✅ (shared `exceptions.py` pattern)
**Status**: 🟡 In Progress

---

## Objective

Build an async HTTP client that extracts financial news articles from NewsAPI.org using `httpx`. The extractor must return Pydantic-validated models, handle errors and rate limits gracefully, and be fully covered by unit tests (≥80%).

---

## NewsAPI.org — Target Endpoints

| Endpoint | Purpose | Auth |
|:---------|:--------|:----:|
| `/v2/everything` | Full-text search across all articles (keywords, date range, domain) | `X-Api-Key` header |
| `/v2/top-headlines` | Breaking news filtered by country, category, or source | `X-Api-Key` header |

- **Base URL:** `https://newsapi.org`
- **Auth:** API key via `X-Api-Key` header (free tier: 100 requests/day)
- **Pagination:** `page` + `pageSize` (max 100 per page)
- **Rate Limit:** HTTP 429 on exhaustion

---

## Module Architecture

```
src/extractors/
├── __init__.py                 # (existing)
├── exceptions.py               # (existing, shared)
├── coingecko/                  # (existing, Issue #1)
├── yahoo_finance/              # (existing, Issue #2)
└── newsapi/
    ├── __init__.py
    ├── config.py               # Settings (api_key, base_url, timeouts)
    ├── client.py               # httpx async client with retry logic
    ├── models.py               # Pydantic v2 response models
    └── extractor.py            # High-level extractor facade
```

---

## Checklist

### 🌿 Step 1 — Branch & Dependencies
- [ ] `git checkout develop`
- [ ] `git checkout -b feature/issue-3-newsapi-extractor`
- [ ] `source .venv/bin/activate` — activate virtual environment
- [ ] Create `src/extractors/newsapi/__init__.py`
- [ ] `pip install -e ".[dev]"` — install all dependencies (no new deps needed, `httpx` already present)
- [ ] Verify: `python -c "import httpx; print('OK')"`

### ⚙️ Step 2 — Configuration (`src/extractors/newsapi/config.py`)
- [ ] `NewsAPISettings(BaseSettings)` with `env_prefix="NEWSAPI_"`
- [ ] Fields: `api_key` (`str`, required), `base_url` (`str`, default `"https://newsapi.org/v2"`), `timeout_seconds` (`float`, default `30.0`), `max_retries` (`int`, default `3`), `retry_wait_seconds` (`float`, default `2.0`), `page_size` (`int`, default `100`)
- [ ] Verify: `ruff check src/extractors/newsapi/config.py`
- [ ] Verify: `mypy src/extractors/newsapi/config.py`

### 📦 Step 3 — Response Models (`src/extractors/newsapi/models.py`)
- [ ] `NewsSource(BaseModel)` — article source metadata
  - Fields: `id` (`str | None`), `name` (`str`)
- [ ] `NewsArticle(BaseModel)` — single article
  - Fields: `source` (`NewsSource`), `author` (`str | None`), `title` (`str`), `description` (`str | None`), `url` (`str`), `url_to_image` (`str | None`), `published_at` (`datetime`), `content` (`str | None`)
- [ ] `NewsResponse(BaseModel)` — paginated API response wrapper
  - Fields: `status` (`str`), `total_results` (`int`), `articles` (`list[NewsArticle]`)
- [ ] Verify: `ruff check src/extractors/newsapi/models.py`
- [ ] Verify: `mypy src/extractors/newsapi/models.py`

### 🌐 Step 4 — Async Client (`src/extractors/newsapi/client.py`)
- [ ] `NewsAPIClient` class wrapping `httpx.AsyncClient`
- [ ] Constructor: accepts `NewsAPISettings`, injects `X-Api-Key` header
- [ ] Async context manager support (`__aenter__`, `__aexit__`)
- [ ] Method: `get_everything(q, from_date, to_date, sort_by, page) -> NewsResponse`
  - Calls `/everything` with keyword params
- [ ] Method: `get_top_headlines(country, category, q, page) -> NewsResponse`
  - Calls `/top-headlines` with filter params
- [ ] Retry with `tenacity.AsyncRetrying` on 429 and 5xx
- [ ] Structured logging with `structlog`
- [ ] Map errors → `RateLimitError`, `APIResponseError`, `ExtractorError`
- [ ] Verify: `ruff check src/extractors/newsapi/client.py`
- [ ] Verify: `mypy src/extractors/newsapi/client.py`

### 🎯 Step 5 — Extractor Facade (`src/extractors/newsapi/extractor.py`)
- [ ] `NewsAPIExtractor` class — high-level API for consumers
- [ ] Async context manager support
- [ ] Method: `extract_everything(q, from_date, to_date, sort_by, page) -> NewsResponse`
- [ ] Method: `extract_top_headlines(country, category, q, page) -> NewsResponse`
- [ ] Delegates to `NewsAPIClient`
- [ ] Update `src/extractors/newsapi/__init__.py` with exports
- [ ] Verify: `ruff check src/extractors/newsapi/extractor.py`
- [ ] Verify: `mypy src/extractors/newsapi/extractor.py`

### 🧪 Step 6 — Unit Tests (`tests/unit/extractors/test_newsapi.py`)
- [ ] `test_get_everything_success` — mock httpx response, validate `NewsResponse` parsing
- [ ] `test_get_everything_empty` — zero results returns empty articles list
- [ ] `test_get_top_headlines_success` — validate headline parsing
- [ ] `test_rate_limit_raises` — HTTP 429 → `RateLimitError`
- [ ] `test_server_error_raises` — HTTP 500 → `APIResponseError`
- [ ] `test_retry_on_transient_error` — verify retry fires on 503 then succeeds on 200
- [ ] `test_timeout_raises` — timeout → `ExtractorError`
- [ ] `test_api_key_header_injected` — verify `X-Api-Key` header
- [ ] `test_extractor_facade` — `NewsAPIExtractor` delegates correctly
- [ ] Verify: `pytest tests/unit/extractors/test_newsapi.py -v`

### ✅ Step 7 — Quality Gates
- [ ] `ruff format src/extractors/ tests/unit/extractors/` — no reformats
- [ ] `ruff check src/extractors/ tests/unit/extractors/` — passes
- [ ] `mypy src/extractors/` — passes (strict)
- [ ] `pytest tests/unit/extractors/ -v --cov=src/extractors --cov-report=term-missing` — ≥80% coverage
- [ ] All four gates green

### 🔀 Step 8 — Commit, Merge & Close
- [ ] `git add -A`
- [ ] `git commit -m "feat(extractors): NewsAPI extractor with everything and top-headlines support (#3)"`
- [ ] `git push origin feature/issue-3-newsapi-extractor`
- [ ] `git checkout develop`
- [ ] `git merge --squash feature/issue-3-newsapi-extractor`
- [ ] `git commit -m "feat(extractors): NewsAPI extractor (#3)"`
- [ ] `git push origin develop`
- [ ] `git branch -d feature/issue-3-newsapi-extractor`
- [ ] Issue #3 closed on GitHub

---

## Design Notes

- **Async client:** Follows the same `httpx.AsyncClient` + `tenacity.AsyncRetrying` pattern established in CoinGecko (Issue #1).
- **API Key required:** Unlike CoinGecko and Yahoo Finance, NewsAPI requires an API key. The `api_key` field has no default — must be set via `NEWSAPI_API_KEY` env var or `.env`.
- **Pagination:** NewsAPI limits `pageSize` to 100 and returns `totalResults` in the response. The client exposes `page` parameter; full pagination can be orchestrated at the DAG level.
- **Response shape:** NewsAPI wraps articles in `{"status": "ok", "totalResults": N, "articles": [...]}`, which maps cleanly to `NewsResponse`.
- Reuses `src/extractors/exceptions.py` — no new exception classes needed.
