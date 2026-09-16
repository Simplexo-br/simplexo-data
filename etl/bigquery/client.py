"""
Simplexo Data - Google BigQuery & Cloud Storage Integration Engine
Manages analytical data lake tables, streaming inserts, and data lake synchronization with resilient fallback.
"""

import os
import json
from typing import Optional, Dict, Any, List

DEFAULT_PROJECT_ID = os.getenv("GCP_PROJECT_ID", "odoo-server-vm2")
DEFAULT_DATASET_ID = os.getenv("BQ_DATASET_ID", "simplexo_data_lake")
DEFAULT_LOCATION = os.getenv("GCP_LOCATION", "southamerica-east1")

class BigQueryDataLake:
    def __init__(self, project_id: Optional[str] = None, dataset_id: Optional[str] = None):
        self.project_id = project_id or DEFAULT_PROJECT_ID
        self.dataset_id = dataset_id or DEFAULT_DATASET_ID
        self.client = None
        self._init_client()

    def _init_client(self):
        try:
            from google.cloud import bigquery
            self.client = bigquery.Client(project=self.project_id)
            print(f"[BigQuery] Connected successfully to project: {self.project_id}")
        except Exception as e:
            print(f"[BigQuery] Notice: BigQuery client running in resilient mode ({e})")
            self.client = None

    def is_available(self) -> bool:
        return self.client is not None

    def ensure_dataset(self, location: str = DEFAULT_LOCATION) -> bool:
        """Ensures that the simplexo_data_lake dataset exists in BigQuery."""
        if not self.client:
            return False
        try:
            from google.cloud import bigquery
            dataset_ref = bigquery.DatasetReference(self.project_id, self.dataset_id)
            try:
                self.client.get_dataset(dataset_ref)
                print(f"[BigQuery] Dataset {self.dataset_id} exists.")
                return True
            except Exception:
                dataset = bigquery.Dataset(dataset_ref)
                dataset.location = location
                dataset.description = "Simplexo Data Sovereign B2B Intelligence & Analytics Data Lake"
                self.client.create_dataset(dataset, timeout=30)
                print(f"[BigQuery] Created dataset {self.dataset_id} at {location}.")
                return True
        except Exception as e:
            print(f"[BigQuery] Error creating dataset {self.dataset_id}: {e}")
            return False

    def query_analytics(self, query: str) -> List[Dict[str, Any]]:
        """Executes analytical SQL query on BigQuery data lake."""
        if not self.client:
            return []
        try:
            query_job = self.client.query(query)
            results = query_job.result()
            return [dict(row) for row in results]
        except Exception as e:
            print(f"[BigQuery] Query execution error: {e}")
            return []

    def stream_records(self, table_name: str, rows: List[Dict[str, Any]]) -> bool:
        """Streams records into specified BigQuery table."""
        if not self.client or not rows:
            return False
        table_ref = f"{self.project_id}.{self.dataset_id}.{table_name}"
        try:
            errors = self.client.insert_rows_json(table_ref, rows)
            if errors:
                print(f"[BigQuery] Insert errors on {table_name}: {errors}")
                return False
            return True
        except Exception as e:
            print(f"[BigQuery] Error streaming to {table_name}: {e}")
            return False

# Global Singleton instance
bq_lake = BigQueryDataLake()
