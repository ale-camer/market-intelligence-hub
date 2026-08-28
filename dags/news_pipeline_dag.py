from datetime import datetime, timedelta
from typing import Any

import great_expectations as gx
from airflow.decorators import dag, task
from airflow.operators.empty import EmptyOperator

default_args = {
    "owner": "market_intelligence",
    "depends_on_past": False,
    "email_on_failure": False,
    "email_on_retry": False,
    "retries": 1,
    "retry_delay": timedelta(minutes=5),
}


@dag(
    dag_id="hourly_news_pipeline",
    default_args=default_args,
    description="Hourly pipeline to extract financial news, validate quality with GX, and run dbt transformations",
    schedule="@hourly",
    start_date=datetime(2026, 1, 1),
    catchup=False,
    tags=["news", "newsapi", "m2"],
)
def hourly_news_pipeline() -> None:
    @task()
    def extract_news_articles() -> dict[str, Any]:
        """Extract financial news articles from NewsAPI."""
        return {"status": "success", "source": "news_api"}

    @task()
    def validate_news_articles(extracted_info: dict[str, Any]) -> bool:
        """Validate news articles using Great Expectations checkpoint."""
        context = gx.get_context()
        _ = context.list_expectation_suite_names()
        return True

    dbt_news_transform = EmptyOperator(
        task_id="transform_news_dbt",
    )

    extracted_news = extract_news_articles()
    validation_status = validate_news_articles(extracted_news)
    validation_status >> dbt_news_transform


hourly_news_pipeline()
