# Issue #22 — CI/CD — GitHub Actions

**Branch**: `feature/issue-22-github-actions`
**Milestone**: M5 — Infra & Observability
**Depends on**: Issue #21 ✅
**Status**: 🟡 Not Started

---

## Objective

Set up Continuous Integration (CI) and Continuous Deployment (CD) pipelines using GitHub Actions. This will enforce code quality standards on every Pull Request to `develop` and `main` branches by automatically running linting, type-checking, and the full test suite (unit and integration tests). 

---

## Architecture

- **`.github/workflows/`**: Directory for all GitHub Actions workflow definitions.
  - `ci.yml`: The primary CI workflow triggered on Pull Requests and pushes to `main`/`develop`.

---

## Checklist

### 🌿 Step 1 — Branch & Setup
- [x] Ensure `develop` is up-to-date: `git checkout develop && git pull`.
- [x] Create the issue branch: `git checkout -b feature/issue-22-github-actions`.

### ⚙️ Step 2 — CI Workflow Configuration
- [x] Create `.github/workflows/ci.yml`.
- [x] Define the trigger events: `push` on `main` and `develop`, and `pull_request` targeting `develop` and `main`.
- [x] Add the `lint-and-typecheck` job:
  - Check out the repository (`actions/checkout@v4`).
  - Set up Python 3.10 (`actions/setup-python@v5`).
  - Install dependencies (`pip install -e ".[dev]"`).
  - Run Ruff for linting (`ruff check .`).
  - Run Ruff for formatting checks (`ruff format --check .`).
  - Run MyPy for static type checking (`mypy src/`).
- [x] Add the `test` job (depends on `lint-and-typecheck`):
  - Check out the repository.
  - Set up Python 3.10.
  - Install dependencies.
  - Run Pytest with coverage (`pytest --cov=src tests/`).
  - (Optional) Upload coverage report as an artifact or integrate with a tool like Codecov.

### 🧪 Step 3 — Validation & Testing
- [ ] Commit the workflow file: `git add .github/workflows/ci.yml && git commit -m "ci: add github actions workflow for linting and testing"`.
- [ ] Push the branch to the remote repository.
- [ ] Navigate to the GitHub repository online and create a Draft PR to `develop`.
- [ ] Verify that the GitHub Actions run automatically and pass successfully (since no logic code exists yet, the checks should pass instantly).

### 🔀 Step 4 — Commit, Merge & Close
- [ ] `git push origin feature/issue-22-github-actions`
- [ ] `git checkout develop`
- [ ] `git merge --squash feature/issue-22-github-actions`
- [ ] `git commit -m "ci: configure github actions pipeline (#22)"`
- [ ] `git push origin develop`
- [ ] `git branch -d feature/issue-22-github-actions`
- [ ] Close Issue #22 on GitHub.

---

## Design Notes
- Running tests in GitHub Actions guarantees that no broken code is merged into `develop`.
- The repository settings on GitHub should be updated to require status checks to pass before merging PRs.
