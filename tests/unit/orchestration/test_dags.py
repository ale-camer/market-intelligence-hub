from pathlib import Path

from airflow.models import DagBag


def test_dags_import_and_integrity() -> None:
    """Verify that all DAGs in dags/ load without import errors and have correct tasks."""
    dags_dir = Path(__file__).parents[3] / "dags"
    dagbag = DagBag(dag_folder=str(dags_dir))

    # 1. Verify no import errors occurred
    assert len(dagbag.import_errors) == 0, f"DAG import errors found: {dagbag.import_errors}"

    # 2. Verify DAG count
    assert len(dagbag.dags) >= 2

    # 3. Check expected DAG IDs
    expected_dag_ids = ["daily_market_data_pipeline", "hourly_news_pipeline"]
    for dag_id in expected_dag_ids:
        assert dag_id in dagbag.dags, f"DAG {dag_id} not found in DagBag"

    # 4. Check market_data_dag tasks
    market_dag = dagbag.dags["daily_market_data_pipeline"]
    assert len(market_dag.tasks) == 3
    assert set(market_dag.task_ids) == {
        "extract_market_data",
        "validate_market_data",
        "transform_dbt_models",
    }

    # 5. Check news_pipeline_dag tasks
    news_dag = dagbag.dags["hourly_news_pipeline"]
    assert len(news_dag.tasks) == 3
    assert set(news_dag.task_ids) == {
        "extract_news_articles",
        "validate_news_articles",
        "transform_news_dbt",
    }
