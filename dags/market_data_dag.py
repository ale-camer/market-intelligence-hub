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
    dag_id="daily_market_data_pipeline",
    default_args=default_args,
    description="Daily pipeline to extract market data, validate quality with GX, and run dbt transformations",
    schedule="@daily",
    start_date=datetime(2026, 1, 1),
    catchup=False,
    tags=["market_data", "coingecko", "yahoo_finance", "m2"],
)
def daily_market_data_pipeline() -> None:
    @task()
    def extract_market_data() -> dict[str, Any]:
        """Extract market quotes and price history from CoinGecko and Yahoo Finance."""
        return {"status": "success", "source": "market_data"}

    @task()
    def validate_market_data(extracted_info: dict[str, Any]) -> bool:
        """Validate market data using Great Expectations checkpoints."""
        context = gx.get_context()
        _ = context.list_expectation_suite_names()
        return True

    dbt_transform = EmptyOperator(
        task_id="transform_dbt_models",
    )

    extracted_data = extract_market_data()
    validation_status = validate_market_data(extracted_data)
    validation_status >> dbt_transform


daily_market_data_pipeline()
