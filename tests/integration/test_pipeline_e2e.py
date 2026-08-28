"""End-to-end integration tests for extraction, data quality (Great Expectations), and DAGs."""

from datetime import UTC, datetime

import pandas as pd

import great_expectations as gx
from dags.market_data_dag import daily_market_data_pipeline
from dags.news_pipeline_dag import hourly_news_pipeline
from src.schemas.enums import AssetClass, DataSource
from src.schemas.market import MarketQuote
from src.schemas.news import FinancialArticle


def test_market_data_flow_integration() -> None:
    """Test end-to-end flow for market quotes: extraction schema -> DataFrame -> GX validation."""
    # 1. Simulate data extraction & Pydantic normalization
    quote = MarketQuote(
        source=DataSource.COINGECKO,
        ticker="BTC",
        asset_class=AssetClass.CRYPTO,
        name="Bitcoin",
        current_price=50000.0,
        volume_24h=1000000.0,
        currency="USD",
    )

    # Convert enum to string value for GX compatibility
    data = quote.model_dump()
    data["asset_class"] = quote.asset_class.value
    df = pd.DataFrame([data])

    # 2. Run Great Expectations validation against market_quotes_suite
    context = gx.get_context()  # type: ignore[attr-defined]
    suite = context.get_expectation_suite("market_quotes_suite")
    validator = gx.from_pandas(df, expectation_suite=suite)  # type: ignore[attr-defined]
    validation_result = validator.validate()

    assert validation_result.success is True, (
        f"Market quotes GX validation failed: {validation_result}"
    )


def test_news_flow_integration() -> None:
    """Test end-to-end flow for news articles: extraction schema -> DataFrame -> GX validation."""
    article = FinancialArticle(
        source=DataSource.NEWSAPI,
        title="Bitcoin Reaches New All-Time High Today",
        description="Crypto markets surge as demand increases.",
        url="https://example.com/news/1",
        published_at=datetime.now(UTC),
        source_name="Financial Times",
    )

    data = article.model_dump()
    data["article_url"] = data["url"]
    df = pd.DataFrame([data])

    context = gx.get_context()  # type: ignore[attr-defined]
    suite = context.get_expectation_suite("news_articles_suite")
    validator = gx.from_pandas(df, expectation_suite=suite)  # type: ignore[attr-defined]
    validation_result = validator.validate()

    assert validation_result.success is True, (
        f"News articles GX validation failed: {validation_result}"
    )


def test_airflow_dags_e2e_structure() -> None:
    """Test integration structure and task availability of Airflow DAGs."""
    market_dag = daily_market_data_pipeline()
    assert market_dag.dag_id == "daily_market_data_pipeline"
    assert len(market_dag.tasks) == 3

    news_dag = hourly_news_pipeline()
    assert news_dag.dag_id == "hourly_news_pipeline"
    assert len(news_dag.tasks) == 3
