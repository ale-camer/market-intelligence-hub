# ADR 0001: Use dbt for Transformations

## Status
Accepted

## Context
The Market Intelligence Hub ingests financial data from various sources (CoinGecko, Yahoo Finance, NewsAPI) into a Data Lake/Data Warehouse. This raw data requires cleaning, standardizing, and aggregating before it can be served via the API or analyzed in dashboards. We needed a tool to handle these transformations efficiently within the warehouse.

## Decision
We decided to use **dbt (data build tool)** for all data transformations within the warehouse, adopting an ELT (Extract, Load, Transform) paradigm. 

## Consequences
- **Positive:**
  - Standardizes transformations using modular, version-controlled SQL.
  - Automatically handles dependencies between staging and mart layers using DAGs.
  - Integrates seamlessly with our CI/CD pipelines and testing frameworks.
  - Keeps transformation logic inside the warehouse, leveraging BigQuery's computational power instead of relying on Python/Pandas in Airflow.
- **Negative:**
  - Requires developers to learn dbt syntax (Jinja + SQL).
  - Shifts the debugging process from Python to SQL.
