# GCS Bucket for Data Lake
resource "google_storage_bucket" "data_lake_bucket" {
  name                        = "${var.project_id}-${var.env}-data-lake"
  location                    = var.region
  force_destroy               = true
  uniform_bucket_level_access = true

  versioning {
    enabled = true
  }

  lifecycle_rule {
    action {
      type = "Delete"
    }
    condition {
      age = 90
    }
  }
}

# BigQuery Datasets: raw, staging, marts
resource "google_bigquery_dataset" "raw" {
  dataset_id                 = "raw_${var.env}"
  friendly_name              = "Raw Data Lake Layer"
  description                = "Raw ingested data from external APIs"
  location                   = var.region
  delete_contents_on_destroy = true
}

resource "google_bigquery_dataset" "staging" {
  dataset_id                 = "staging_${var.env}"
  friendly_name              = "Staging Data Layer"
  description                = "Cleaned and standardized staging models"
  location                   = var.region
  delete_contents_on_destroy = true
}

resource "google_bigquery_dataset" "marts" {
  dataset_id                 = "marts_${var.env}"
  friendly_name              = "Analytical Marts Layer"
  description                = "Dimension and Fact tables for analytics"
  location                   = var.region
  delete_contents_on_destroy = true
}

# Service Account for Data Pipeline
resource "google_service_account" "pipeline_sa" {
  account_id   = "market-intel-pipeline-${var.env}"
  display_name = "Market Intelligence Data Pipeline SA"
  description  = "Service Account used by Airflow/extractors to write to GCS and BigQuery"
}

# IAM Role Bindings for Service Account
resource "google_project_iam_member" "sa_storage_admin" {
  project = var.project_id
  role    = "roles/storage.objectAdmin"
  member  = "serviceAccount:${google_service_account.pipeline_sa.email}"
}

resource "google_project_iam_member" "sa_bq_editor" {
  project = var.project_id
  role    = "roles/bigquery.dataEditor"
  member  = "serviceAccount:${google_service_account.pipeline_sa.email}"
}

resource "google_project_iam_member" "sa_bq_job_user" {
  project = var.project_id
  role    = "roles/bigquery.jobUser"
  member  = "serviceAccount:${google_service_account.pipeline_sa.email}"
}
