"""BigQuery client setup and configuration wrapper for GCP interaction."""

import os

from google.cloud import bigquery


class BigQueryClient:
    """Wrapper class around google.cloud.bigquery.Client."""

    def __init__(
        self,
        project_id: str | None = None,
        dataset_id: str | None = None,
        client: bigquery.Client | None = None,
    ) -> None:
        """Initialize BigQuery client with project and dataset configurations."""
        self.project_id: str = (
            project_id or os.getenv("GCP_PROJECT_ID") or "market-intelligence-hub"
        )
        self.dataset_id: str = dataset_id or os.getenv("GCP_DATASET_ID") or "raw_market_data"
        self._client = client

    @property
    def client(self) -> bigquery.Client:
        """Lazy load or return initialized BigQuery client."""
        if self._client is None:
            self._client = bigquery.Client(project=self.project_id)
        return self._client

    @property
    def dataset_ref(self) -> bigquery.DatasetReference:
        """Get dataset reference for the current project and dataset ID."""
        return self.client.dataset(self.dataset_id)

    def get_table_ref(self, table_name: str) -> bigquery.TableReference:
        """Get full table reference for a given table name."""
        return self.dataset_ref.table(table_name)
