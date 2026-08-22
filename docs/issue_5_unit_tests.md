# Issue #5 — Unit Tests (Extractors & Schemas)

**Branch**: `feature/issue-5-unit-tests`
**Milestone**: M1 — Data Extraction
**Depends on**: Issues #1, #2, #3, #4
**Status**: 🟡 Not Started

---

## Objective

Consolidate and verify the unit test suite for all extractors (CoinGecko, Yahoo Finance, NewsAPI) and canonical schemas. Since we adopted a Test-Driven Development (TDD) approach and implemented tests inline during Issues #1-4, this issue focuses on orchestrating a unified test run, ensuring global ≥80% test coverage across the entire `src/` directory, and establishing a `Makefile` to standardize local quality checks.

---

## Checklist

### 🌿 Step 1 — Branch & Setup
- [ ] `git checkout develop`
- [ ] `git checkout -b feature/issue-5-unit-tests`

### 🛠️ Step 2 — Create Makefile
- [ ] Create a `Makefile` at the root of the project with the following targets:
  - `format`: `ruff format src/ tests/`
  - `lint`: `ruff check src/ tests/ --fix`
  - `typecheck`: `mypy src/ tests/`
  - `test`: `pytest tests/ -v`
  - `coverage`: `pytest tests/ -v --cov=src --cov-report=term-missing --cov-report=html`
  - `check`: runs `format`, `lint`, `typecheck`, and `coverage` sequentially.

### 🧪 Step 3 — Global Test Execution
- [ ] Verify formatting: `make format`
- [ ] Verify linting: `make lint`
- [ ] Verify typing: `make typecheck`
- [ ] Run unified coverage: `make coverage`
- [ ] Verify that total coverage across all of `src/` is ≥80%.

### 🔀 Step 4 — Commit, Merge to Develop & Main (Milestone Closure)
- [ ] `git add Makefile`
- [ ] `git commit -m "test: unified test suite execution and Makefile (#5)"`
- [ ] `git push origin feature/issue-5-unit-tests`
- [ ] `git checkout develop`
- [ ] `git merge --squash feature/issue-5-unit-tests`
- [ ] `git commit -m "test: Unit Tests Extractors (#5)"`
- [ ] `git push origin develop`
- [ ] `git branch -d feature/issue-5-unit-tests`
- [ ] `git checkout main`
- [ ] `git merge develop`
- [ ] `git tag -a v0.1.0-m1 -m "Milestone 1 - Data Extraction"`
- [ ] `git push origin main --tags`
- [ ] Issue #5 closed on GitHub

---

## Design Notes
- Thanks to the TDD approach used in Issues #1-4, all necessary unit tests are already implemented.
- The `Makefile` standardizes quality gate commands for all future issues, abstracting away the long `ruff`, `mypy`, and `pytest` commands.
