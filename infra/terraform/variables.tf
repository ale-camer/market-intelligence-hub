variable "project_id" {
  description = "The GCP project ID"
  type        = string
  default     = "market-intelligence-hub-dev"
}

variable "region" {
  description = "The GCP region for resources"
  type        = string
  default     = "us-central1"
}

variable "env" {
  description = "Environment name (e.g. dev, staging, prod)"
  type        = string
  default     = "dev"
}
