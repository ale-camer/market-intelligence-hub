# Issue #21 — Grafana Dashboards

**Branch**: `feature/issue-21-grafana-dashboards`
**Milestone**: M5 — Infra & Observability
**Depends on**: Issue #20 ✅
**Status**: 🟡 Not Started

---

## Objective

Configure Grafana to monitor the overall health of the Market Intelligence Hub. We will provision default data sources and create dashboards to track pipeline execution (via Airflow metrics), data freshness (querying PostgreSQL/BigQuery), and API health/usage (FastAPI metrics via Prometheus).

---

## Architecture

- **`infra/grafana/provisioning/`**: Directory for Grafana provisioning configurations.
  - `datasources/`: YAML files defining data sources (Postgres, Prometheus).
  - `dashboards/`: YAML files linking to JSON dashboard definitions.
- **Dashboards**:
  - `pipeline_health.json`: Tracks Airflow DAG success/failure rates and execution times.
  - `data_freshness.json`: Monitors the most recent timestamps of ingested data in the warehouse.
  - `api_metrics.json`: Visualizes FastAPI request rates, error rates, and response latency.

---

## Checklist

### 🌿 Step 1 — Branch & Setup
- [ ] Ensure `develop` is up-to-date: `git checkout develop && git pull`.
- [ ] Create the issue branch: `git checkout -b feature/issue-21-grafana-dashboards`.

### 🔌 Step 2 — Data Source Provisioning
- [x] Create `infra/grafana/provisioning/datasources/datasources.yaml`.
- [x] Add **PostgreSQL** as a default data source pointing to the local `postgres:5432` container (database: `market_intelligence`).
- [x] (Optional) Add **Prometheus** as a data source if we integrate Prometheus for the FastAPI app.

### 📊 Step 3 — Dashboard Provisioning Configuration
- [x] Create `infra/grafana/provisioning/dashboards/dashboards.yaml`.
- [x] Configure the dashboards provider to load JSON files from `/etc/grafana/provisioning/dashboards/`.

### 📈 Step 4 — Dashboard Creation (JSONs)
- [x] Create `infra/grafana/provisioning/dashboards/pipeline_health.json`.
- [x] Create `infra/grafana/provisioning/dashboards/data_freshness.json`.
- [x] Create `infra/grafana/provisioning/dashboards/api_metrics.json`.
- [x] Update `docker-compose.yml` (from Issue #20) to mount the `infra/grafana/provisioning` directory into the Grafana container at `/etc/grafana/provisioning`.

### 🧪 Step 5 — Validation & Testing
- [ ] Run `docker compose up -d grafana postgres` to start the required services.
- [ ] Access Grafana at `http://localhost:3000`.
- [ ] Verify that the data sources are automatically provisioned.
- [ ] Verify that the three dashboards appear in the UI and load without layout errors.
- [ ] Shut down the containers: `docker compose down`.

### 🔀 Step 6 — Commit, Merge & Close
- [ ] `git add infra/grafana/ docker-compose.yml`
- [ ] `git commit -m "feat(observability): add grafana dashboards provisioning (#21)"`
- [ ] `git push origin feature/issue-21-grafana-dashboards`
- [ ] `git checkout develop`
- [ ] `git merge --squash feature/issue-21-grafana-dashboards`
- [ ] `git commit -m "feat(observability): add grafana dashboards provisioning (#21)"`
- [ ] `git push origin develop`
- [ ] `git branch -d feature/issue-21-grafana-dashboards`
- [ ] Close Issue #21 on GitHub.

---

## Design Notes
- Grafana dashboard JSONs can be very large and unreadable. The best approach is to create them manually in the Grafana UI, export the JSON model, and save that into the `dashboards/` directory.
- Use Grafana variables for environments (`dev`, `prod`) to make the dashboards reusable across different deployments.
