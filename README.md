# Market Intelligence Hub

[![CI](https://github.com/ale-camer/market-intelligence-hub/actions/workflows/ci.yml/badge.svg)](https://github.com/ale-camer/market-intelligence-hub/actions)
[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Code style: ruff](https://img.shields.io/badge/code%20style-ruff-000000.svg)](https://github.com/astral-sh/ruff)

> **P-05 — Portfolio Project** | A unified data platform that consolidates multi-source financial market data (prices, news sentiment, on-chain metrics) with full orchestration, warehousing, and API serving capabilities.

---

## 🏗️ Architecture Overview

```
┌──────────────────────────────────────────────────────────────────────┐
│                        Data Sources                                  │
│   CoinGecko  │  Yahoo Finance  │  NewsAPI  │  Glassnode (on-chain)  │
└──────┬───────┴────────┬────────┴────┬──────┴────────────┬───────────┘
       │                │             │                   │
       ▼                ▼             ▼                   ▼
┌──────────────────────────────────────────────────────────────────────┐
│                  M1 — Extraction Layer (src/extractors/)             │
│           Pydantic-validated Python extractors + Airflow DAGs        │
└─────────────────────────────┬────────────────────────────────────────┘
                              │
               ┌──────────────┴──────────────┐
               ▼                             ▼
┌──────────────────────┐       ┌─────────────────────────────────────┐
│  Apache Kafka        │       │  PostgreSQL (OLTP)                  │
│  (market-events,     │       │  Raw ingestion store                │
│   news-events topics)│       └──────────────┬──────────────────────┘
└──────────────────────┘                      │
                                              ▼
                              ┌─────────────────────────────────────┐
                              │  M2 — Transformation Layer          │
                              │  dbt models + Great Expectations    │
                              │  (raw → staging → mart)             │
                              └──────────────┬──────────────────────┘
                                             │
                                             ▼
                              ┌─────────────────────────────────────┐
                              │  M3 — BigQuery Data Warehouse       │
                              │  (mart layer, analytical queries)   │
                              └──────────────┬──────────────────────┘
                                             │
                              ┌──────────────┴──────────────┐
                              ▼                             ▼
               ┌──────────────────────┐       ┌────────────────────────┐
               │  M4 — FastAPI        │       │  M5 — Observability    │
               │  REST API serving    │       │  Grafana + Prometheus  │
               │  market intelligence │       │  Terraform (GCP IaC)   │
               └──────────────────────┘       └────────────────────────┘
```

---

## 📚 Documentation & ADRs

- **[Data Dictionary](docs/data_dictionary.md)**: Explore the data schemas for the raw, staging, and marts layers.
- **[ADR 0001: dbt for Transformations](docs/adrs/0001-use-dbt-for-transformations.md)**
- **[ADR 0002: Kafka for Event Streaming](docs/adrs/0002-use-kafka-for-event-streaming.md)**
- **[ADR 0003: FastAPI for Serving Layer](docs/adrs/0003-use-fastapi-for-serving-layer.md)**

---

## 📦 Tech Stack

| Layer | Technology |
|:------|:-----------|
| Orchestration | Apache Airflow 2.9+ |
| Extraction | Python + httpx + Pydantic v2 |
| Messaging | Apache Kafka + Avro |
| OLTP Storage | PostgreSQL 16 + SQLAlchemy |
| OLAP Warehouse | Google BigQuery |
| Transformation | dbt-bigquery |
| Data Quality | Great Expectations |
| API Serving | FastAPI + Uvicorn |
| Auth | JWT (python-jose) |
| Observability | Grafana + Prometheus |
| IaC | Terraform (GCP) |
| CI/CD | GitHub Actions |
| Containerization | Docker + Docker Compose |

---

## 🗂️ Repository Structure

```text
market-intelligence-hub/
├── src/
│   ├── extractors/     # Data source extractors (CoinGecko, YFinance, NewsAPI, Glassnode)
│   ├── transformers/   # dbt models and transformation utilities
│   ├── loaders/        # PostgreSQL and BigQuery loaders
│   └── api/            # FastAPI application (routes, schemas, auth)
├── dags/               # Apache Airflow DAGs
├── tests/
│   ├── unit/           # Unit tests with mocks
│   └── integration/    # Integration tests
├── infra/
│   ├── terraform/      # GCP infrastructure as code
│   └── docker/         # Dockerfiles and compose files
├── docs/               # Architecture docs, ADRs, issue tracking
└── .github/
    └── workflows/      # CI/CD GitHub Actions pipelines
```

---

## 🚀 Quick Start (Development)

### 1. Local Environment Setup
```bash
# Clone the repository
git clone https://github.com/ale-camer/market-intelligence-hub.git
cd market-intelligence-hub

# Create and activate virtual environment
python3 -m venv .venv
source .venv/bin/activate

# Install development dependencies
pip install -e ".[dev]"

# Copy and configure environment variables
cp .env.example .env
# Edit .env with your API keys and credentials
```

### 2. Running the Infrastructure (Docker Compose)
The project includes a complete local stack containing PostgreSQL, Kafka, Zookeeper, Airflow, and Grafana.

```bash
# Spin up the infrastructure in detached mode
docker compose up -d

# Check the status of the containers
docker compose ps
```
Services exposed locally:
- **Airflow Web UI**: `http://localhost:8080` (admin/admin)
- **Grafana Dashboards**: `http://localhost:3000` (admin/adminpassword)
- **PostgreSQL**: `localhost:5432`

### 3. Testing and Linting
```bash
# Run unit and integration tests with coverage
pytest --cov=src tests/

# Run code linters (Ruff)
ruff check src/ tests/
ruff format --check src/ tests/

# Run static type checking (MyPy)
mypy src/
```

---

## 📋 Project Milestones

| Milestone | Description | Status |
|:----------|:------------|:------:|
| M1 — Data Extraction | Extractors, Pydantic schemas, unit tests | ✅ Done |
| M2 — Transformation & Quality | dbt models, Great Expectations, Airflow DAGs | ✅ Done |
| M3 — Storage & Warehouse | PostgreSQL loader, BigQuery loader, Kafka | ✅ Done |
| M4 — API & Serving | FastAPI endpoints, auth, rate limiting | ✅ Done |
| M5 — Infra & Observability | Terraform, Grafana, CI/CD, final docs | ✅ Done |

---

## 📄 License

MIT License — see [LICENSE](LICENSE) for details.

---

*Part of the [DE → AI Engineer Portfolio](https://github.com/ale-camer) roadmap.*
