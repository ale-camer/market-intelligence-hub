# Issue #0 — Day 0 Setup: Repository Scaffolding

**Branch**: `feature/day-0-setup`
**Milestone**: Pre-project setup
**Status**: 🟡 In Progress

---

## Objective

Initialize the project repository with the base skeleton: empty directory structure, configuration files, and initial documentation. No business logic code is written in this issue.

---

## Checklist

### 🌿 Git & Branching
- [x] `git init` — repository initialized
- [x] Empty commit on `main` branch
- [x] `develop` branch created from `main`
- [x] `feature/day-0-setup` branch created from `develop`

### 🐍 Virtual Environment
- [x] `.venv` created with `python3 -m venv .venv`
- [x] Python version verified: Python 3.14.5

### 📁 Directory Structure
- [x] `src/extractors/` — placeholder for data source extractors
- [x] `src/transformers/` — placeholder for transformation logic
- [x] `src/loaders/` — placeholder for storage loaders
- [x] `src/api/` — placeholder for FastAPI application
- [x] `dags/` — placeholder for Airflow DAGs
- [x] `tests/unit/` — placeholder for unit tests
- [x] `tests/integration/` — placeholder for integration tests
- [x] `infra/terraform/` — placeholder for GCP IaC
- [x] `infra/docker/` — placeholder for Dockerfiles
- [x] `docs/` — documentation directory
- [x] `.github/workflows/` — placeholder for CI/CD pipelines

### ⚙️ Configuration Files
- [x] `.gitignore` — Python, venv, IDE, Airflow, dbt, Terraform, secrets
- [x] `.env.example` — all environment variables documented
- [x] `pyproject.toml` — project metadata, dependencies, ruff/mypy/pytest config

### 📝 Documentation
- [x] `README.md` — architecture overview, tech stack, quick start, milestones
- [x] `docs/issue_0_setup.md` — this file (Day 0 tracking)

### 🌐 GitHub Remote
- [x] Public repository created: https://github.com/ale-camer/market-intelligence-hub
- [x] Remote added and initial commit pushed
- [x] Milestones created (M1–M5, numbers 1–5)
- [x] Issues created (#1–#23, 23 atomic issues across 5 milestones)
- [x] Branch `develop` pushed to remote
- [x] Branch `feature/day-0-setup` pushed to remote

### 🔀 Merge & Close
- [ ] PR: `feature/day-0-setup` → `develop`
- [ ] PR merged (squash)
- [ ] Issue #0 closed

---

## Milestone & Issues Plan

### M1 — Data Extraction
| Issue | Title | Description |
|:-----:|:------|:------------|
| #1 | CoinGecko Extractor | HTTP client for crypto prices (OHLCV, market cap) |
| #2 | Yahoo Finance Extractor | HTTP client for stock/forex prices |
| #3 | NewsAPI Extractor | HTTP client for financial news articles |
| #4 | Pydantic v2 Schemas | Strongly-typed models for all data sources |
| #5 | Unit Tests — Extractors | Mocked unit tests for all extractors, ≥80% coverage |

### M2 — Transformation & Quality
| Issue | Title | Description |
|:-----:|:------|:------------|
| #6 | dbt Models: raw → staging | Cleaning and standardization models |
| #7 | dbt Models: staging → mart | Analytical marts (price, sentiment, on-chain) |
| #8 | Great Expectations Suites | Data quality checkpoints for all sources |
| #9 | Airflow DAGs | Orchestration DAGs (extraction, transformation) |
| #10 | Integration Tests — Pipeline | End-to-end pipeline tests |

### M3 — Storage & Warehouse
| Issue | Title | Description |
|:-----:|:------|:------------|
| #11 | PostgreSQL Loader | SQLAlchemy ORM + Alembic migrations |
| #12 | BigQuery Loader | GCP BigQuery writer with schema management |
| #13 | Kafka Producer & Consumer | market-events and news-events topics |
| #14 | Unit Tests — Storage Layer | Mocked tests for loaders and Kafka, ≥80% coverage |

### M4 — API & Serving
| Issue | Title | Description |
|:-----:|:------|:------------|
| #15 | FastAPI Application Setup | App factory, routing, middleware |
| #16 | Market Data Endpoints | GET endpoints for prices, news, on-chain |
| #17 | Auth & Rate Limiting | JWT authentication + request rate limiting |
| #18 | API Tests | pytest tests for all endpoints |

### M5 — Infra & Observability
| Issue | Title | Description |
|:-----:|:------|:------------|
| #19 | Terraform — GCP Infrastructure | BigQuery datasets, GCS buckets, IAM |
| #20 | Docker Compose | Full local stack (Airflow, Kafka, PG, Grafana) |
| #21 | Grafana Dashboards | Pipeline health, API metrics, data freshness |
| #22 | CI/CD — GitHub Actions | Lint + type-check + test pipeline |
| #23 | Final Documentation & ADRs | Architecture Decision Records, data dictionary |

---

## Notes

- All code, commits, docstrings and documentation are written exclusively in **English**.
- Business logic code starts at **Issue #1** (M1 branch: `feature/issue-1-coingecko-extractor`).
- Each issue branch is created from `develop` and merged back via PR (squash merge).
- `develop` is merged into `main` only when a full milestone is complete and green.
