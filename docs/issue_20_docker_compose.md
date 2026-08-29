# Issue #20 — Docker Compose (Local Stack)

**Branch**: `feature/issue-20-docker-compose`
**Milestone**: M5 — Infra & Observability
**Depends on**: Issue #19 ✅
**Status**: 🟡 Not Started

---

## Objective

Set up a complete local development environment using `docker-compose`. This stack will include all necessary infrastructure components to run the entire data pipeline locally: Apache Airflow (orchestration), Kafka & Zookeeper (messaging), PostgreSQL (relational storage/warehouse), and Grafana (observability).

---

## Architecture

- **`docker-compose.yml`**: The root configuration file for the local stack.
- **Services**:
  - `postgres`: PostgreSQL database (used for both Airflow metadata and as the local data warehouse).
  - `zookeeper`: Required for Kafka cluster management.
  - `kafka`: Message broker for the event-driven architecture.
  - `airflow-webserver`: Airflow UI.
  - `airflow-scheduler`: Airflow DAG scheduler.
  - `airflow-init`: Initialization container for Airflow DB migrations and user setup.
  - `grafana`: Dashboarding and visualization tool.

---

## Checklist

### 🌿 Step 1 — Branch & Setup
- [ ] Ensure `develop` is up-to-date: `git checkout develop && git pull`.
- [ ] Create the issue branch: `git checkout -b feature/issue-20-docker-compose`.

### 🐳 Step 2 — Base Infrastructure (Postgres & Kafka)
- [x] Create `docker-compose.yml` in the project root.
- [x] Add the `postgres` service with an initialized database for Airflow (`airflow`) and the data warehouse (`market_intel`). Set up environment variables (user, password, db).
- [x] Add the `zookeeper` service using the Confluent image (`confluentinc/cp-zookeeper`).
- [x] Add the `kafka` service using the Confluent image (`confluentinc/cp-kafka`), depending on `zookeeper`, and configuring the plaintext listener on port 9092.

### 💨 Step 3 — Orchestration (Apache Airflow)
- [x] Add the `airflow-init` service to run database migrations and create the default admin user.
- [x] Add the `airflow-scheduler` service, mounting the `./dags` and `./logs` directories, and connecting it to the `postgres` database.
- [x] Add the `airflow-webserver` service, exposing port 8080, mounting the necessary directories, and configuring dependencies.

### 📊 Step 4 — Observability (Grafana)
- [x] Add the `grafana` service using the official image (`grafana/grafana`).
- [x] Expose port 3000 for the Grafana UI.
- [x] (Optional) Create a default provisioning setup for data sources linking Grafana to the local `postgres` database.

### 🧪 Step 5 — Validation & Testing
- [x] Run `docker-compose up -d` to start the entire stack.
- [x] Verify Kafka is running and accessible on `localhost:9092`.
- [x] Verify PostgreSQL is accepting connections on `localhost:5432`.
- [x] Access the Airflow UI at `http://localhost:8080` and log in successfully.
- [x] Access the Grafana UI at `http://localhost:3000`.
- [x] Run `docker-compose down -v` to cleanly shut down and remove volumes.

### 🔀 Step 6 — Commit, Merge & Close
- [ ] `git add docker-compose.yml`
- [ ] `git commit -m "feat(infra): add docker-compose for local stack (#20)"`
- [ ] `git push origin feature/issue-20-docker-compose`
- [ ] `git checkout develop`
- [ ] `git merge --squash feature/issue-20-docker-compose`
- [ ] `git commit -m "feat(infra): add docker-compose for local stack (#20)"`
- [ ] `git push origin develop`
- [ ] `git branch -d feature/issue-20-docker-compose`
- [ ] Close Issue #20 on GitHub.

---

## Design Notes
- Store sensitive configuration or passwords in an `.env` file (ensure it's ignored by Git) and reference them in `docker-compose.yml`.
- Make sure to mount local directories (e.g., `./dags`, `./src`) as volumes in the Airflow containers so that code changes are reflected immediately without rebuilding the image.
- Configure resource limits (CPU/Memory) in `docker-compose.yml` to prevent the stack from overwhelming the host machine during local development.
