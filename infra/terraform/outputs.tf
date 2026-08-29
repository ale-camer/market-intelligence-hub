output "data_lake_bucket_name" {
  description = "The name of the GCS bucket for raw data storage"
  value       = google_storage_bucket.data_lake_bucket.name
}

output "raw_dataset_id" {
  description = "The ID of the raw BigQuery dataset"
  value       = google_bigquery_dataset.raw.dataset_id
}

output "staging_dataset_id" {
  description = "The ID of the staging BigQuery dataset"
  value       = google_bigquery_dataset.staging.dataset_id
}

output "marts_dataset_id" {
  description = "The ID of the marts BigQuery dataset"
  value       = google_bigquery_dataset.marts.dataset_id
}

output "service_account_email" {
  description = "The email address of the pipeline service account"
  value       = google_service_account.pipeline_sa.email
}
