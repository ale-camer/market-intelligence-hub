# Issue #19 — Terraform — GCP Infrastructure

**Branch**: `feature/issue-19-terraform-gcp`
**Milestone**: M5 — Infra & Observability
**Depends on**: Issue #18 ✅
**Status**: 🟡 Not Started

---

## Objective

Provision the necessary cloud infrastructure on Google Cloud Platform (GCP) using Terraform (Infrastructure as Code). This includes creating BigQuery datasets for our data warehouse, Google Cloud Storage (GCS) buckets for data lakes and Terraform state, and configuring Identity and Access Management (IAM) service accounts with the principle of least privilege.

---

## Architecture

- **`infra/terraform/`**: The root directory for all Terraform configurations.
- **Provider**: Google Cloud Platform (`hashicorp/google`).
- **Resources**:
  - `google_bigquery_dataset`: Datasets for raw, staging, and mart layers.
  - `google_storage_bucket`: Buckets for raw data lake and Terraform remote state.
  - `google_service_account`: Dedicated service accounts for data extraction and loading processes.
  - `google_project_iam_member`: IAM role bindings for the service accounts.

---

## Checklist

### 🌿 Step 1 — Branch & Setup
- [x] Ensure `develop` is up-to-date: `git checkout develop && git pull`.
- [x] Create the issue branch: `git checkout -b feature/issue-19-terraform-gcp`.
- [x] Ensure Terraform CLI is installed on the local machine (`terraform version`).

### 🛠️ Step 2 — Terraform Configuration
- [x] Navigate to `infra/terraform/` (create if it doesn't exist).
- [x] Create `providers.tf` to configure the Google Cloud provider.
- [x] Create `variables.tf` to define project variables (e.g., `project_id`, `region`, `env`).
- [x] Create `main.tf` and define:
    - **BigQuery Datasets**: `raw`, `staging`, `marts`.
    - **GCS Buckets**: Data lake bucket and Terraform state bucket.
    - **IAM & Service Accounts**: Create a service account (e.g., `data-pipeline-sa`) and assign necessary roles (BigQuery Data Editor, Storage Object Admin).
- [x] Create `outputs.tf` to output the created resource IDs and service account emails.

### 🧪 Step 3 — Validation & Plan
- [ ] Run `terraform init` to initialize the provider and backend.
- [ ] Run `terraform fmt` to format the code according to HashiCorp conventions.
- [ ] Run `terraform validate` to check syntax and validity of configuration files.
- [ ] Run `terraform plan` to verify the execution plan. Ensure it matches the expected infrastructure (Optional: actually apply to a sandbox project if GCP credentials are set).

### 🔀 Step 4 — Commit, Merge & Close
- [ ] `git add infra/terraform/`
- [ ] `git commit -m "feat(infra): setup gcp infrastructure with terraform (#19)"`
- [ ] `git push origin feature/issue-19-terraform-gcp`
- [ ] `git checkout develop`
- [ ] `git merge --squash feature/issue-19-terraform-gcp`
- [ ] `git commit -m "feat(infra): setup gcp infrastructure with terraform (#19)"`
- [ ] `git push origin develop`
- [ ] `git branch -d feature/issue-19-terraform-gcp`
- [ ] Close Issue #19 on GitHub.

---

## Design Notes
- Store the Terraform remote state in a GCS bucket to allow team collaboration and avoid state conflicts.
- Do not commit any service account key files (`*.json`) to the repository. Ensure they are added to `.gitignore`.
- Use variables for project IDs and regions to allow for multiple environments (e.g., `dev`, `prod`) in the future.
