# Issue #23 — Final Documentation & ADRs

**Branch**: `feature/issue-23-final-documentation`
**Milestone**: M5 — Infra & Observability
**Depends on**: Issue #22 ✅
**Status**: 🟡 Not Started

---

## Objective

Finalize the project documentation to ensure the Market Intelligence Hub is easily maintainable and understandable for future developers. This includes writing Architecture Decision Records (ADRs) for key technical choices, creating a comprehensive Data Dictionary for the Data Warehouse, and polishing the root `README.md`.

---

## Architecture

- **`docs/adrs/`**: Directory containing Architecture Decision Records.
  - `0001-use-dbt-for-transformations.md`
  - `0002-use-kafka-for-event-streaming.md`
  - `0003-use-fastapi-for-serving-layer.md`
- **`docs/data_dictionary.md`**: Comprehensive description of the `market_intel` schemas, tables, and columns.
- **`README.md`**: The entry point of the repository.

---

## Checklist

### 🌿 Step 1 — Branch & Setup
- [x] Ensure `develop` is up-to-date: `git checkout develop && git pull`.
- [x] Create the issue branch: `git checkout -b feature/issue-23-final-documentation`.

### 📚 Step 2 — Architecture Decision Records (ADRs)
- [x] Create `docs/adrs/` directory.
- [x] Write `0001-use-dbt-for-transformations.md` detailing why dbt was chosen over pure SQL scripts or Pandas.
- [x] Write `0002-use-kafka-for-event-streaming.md` explaining the event-driven decoupling between extraction and loading.
- [x] Write `0003-use-fastapi-for-serving-layer.md` justifying the use of FastAPI for synchronous data serving.

### 📖 Step 3 — Data Dictionary
- [x] Create `docs/data_dictionary.md`.
- [x] Document the `raw` layer (e.g., `market_quotes_raw`, `news_articles_raw`).
- [x] Document the `staging` layer schemas.
- [x] Document the `marts` layer (dimension and fact tables).

### 📝 Step 4 — Polish README
- [x] Update `README.md` to reflect the final state of the project.
- [x] Add instructions for running the local stack via Docker Compose.
- [x] Add instructions for running tests and linters.
- [x] Link to the ADRs and Data Dictionary.

### 🔀 Step 5 — Commit, Merge & Close
- [ ] `git add docs/ README.md`
- [ ] `git commit -m "docs: add ADRs, data dictionary and update README (#23)"`
- [ ] `git push origin feature/issue-23-final-documentation`
- [ ] `git checkout develop`
- [ ] `git merge --squash feature/issue-23-final-documentation`
- [ ] `git commit -m "docs: finalize project documentation (#23)"`
- [ ] `git push origin develop`
- [ ] `git branch -d feature/issue-23-final-documentation`
- [ ] Close Issue #23 on GitHub.

---

## Design Notes
- ADRs should follow a standard format: Title, Status, Context, Decision, and Consequences.
- The Data Dictionary should be treated as a living document; as the schema evolves, the dictionary must be updated.
