# Issue #8 — Great Expectations Suites

**Branch**: `feature/issue-8-great-expectations`
**Milestone**: M2 — Transformation & Quality
**Depends on**: Issue #7 ✅
**Status**: 🟡 Not Started

---

## Objective

Configurar **Great Expectations (GX)** como nuestra herramienta principal para validación estricta de la calidad de los datos (Data Quality). A diferencia de los schemas de Pydantic (que validan tipos y formas durante la extracción), GX nos permite definir reglas de negocio y restricciones semánticas (ej. los precios deben ser positivos, el máximo mayor al mínimo, etc.) directamente sobre colecciones de datos (DataFrames o Tablas).

Estas validaciones servirán como barreras de calidad (Checkpoints) dentro del flujo de Airflow (Issue 9) antes de poblar los modelos analíticos.

---

## Architecture

- **`gx/`**: Directorio base inicializado por Great Expectations (Data Context).
- **Expectation Suites**: Reglas declarativas JSON enfocadas en negocio.
- **Checkpoints**: Entidades que combinan los datos en vuelo (Pandas DataFrames desde los extractores) con las suites correspondientes para dictaminar si el lote pasa (Pass) o falla (Fail).

---

## Checklist

### 🌿 Step 1 — Branch & Setup
- [ ] `git checkout develop`
- [ ] `git checkout -b feature/issue-8-great-expectations`
- [ ] Agregar `"great-expectations>=0.18.0"` a `dependencies` en `pyproject.toml`.
- [ ] Ejecutar `pip install -e ".[dev]"`.
- [ ] Ejecutar `great_expectations init` en la raíz del proyecto para crear la estructura base. (Aceptar configuración por defecto).

### ⚙️ Step 2 — Configuration (`gx/great_expectations.yml`)
- [ ] Revisar el archivo `.gitignore` en la raíz del proyecto y asegurarse de que el directorio `gx/uncommitted/` esté ignorado (para no subir credenciales ni logs locales).
- [ ] Limpiar los archivos generados de ejemplo (si los hay) bajo `gx/expectations/`.

### 📊 Step 3 — Expectation Suites definition
Crear (vía Python script descartable en `/scratch` o usando la CLI) 3 suites principales en `gx/expectations/`:

- [ ] **Suite `market_quotes_suite`**:
  - `expect_column_values_to_not_be_null` en `ticker`, `current_price`.
  - `expect_column_values_to_be_between` en `current_price` (min_value: 0).
  - `expect_column_values_to_be_in_set` en `asset_class` (`['crypto', 'equity']`).

- [ ] **Suite `price_history_suite`**:
  - `expect_column_values_to_not_be_null` en `ticker`, `bar_timestamp`, `close_price`.
  - `expect_column_pair_values_A_to_be_greater_than_or_equal_to_B` verificando que `high_price` >= `low_price`.
  - `expect_column_values_to_be_between` en `volume` (min_value: 0).

- [ ] **Suite `news_articles_suite`**:
  - `expect_column_values_to_not_be_null` en `article_url`, `title`, `published_at`.
  - `expect_column_value_lengths_to_be_between` en `title` (min_value: 5).

### 🛠️ Step 4 — Checkpoints (`gx/checkpoints/`)
- [ ] Crear programáticamente o manualmente los esqueletos de Checkpoints asociados (`market_quotes_checkpoint`, `price_history_checkpoint`, `news_articles_checkpoint`). En el futuro, Airflow instanciará estos checkpoints pasándoles el DataFrame extraído.

### 🧪 Step 5 — Unit Tests & Verification
- [ ] Crear el archivo `tests/unit/quality/test_gx_context.py`.
- [ ] Añadir un test que instancie el contexto local (`import great_expectations as gx; context = gx.get_context()`) y verifique que las 3 suites (`market_quotes_suite`, `price_history_suite`, `news_articles_suite`) existan en el `context.list_expectation_suite_names()`.
- [ ] Ejecutar `make format && make lint && make typecheck && make coverage`.

### 🔀 Step 6 — Commit, Merge & Close
- [ ] `git add -A`
- [ ] `git commit -m "feat(quality): configure great expectations and suites (#8)"`
- [ ] `git push origin feature/issue-8-great-expectations`
- [ ] `git checkout develop`
- [ ] `git merge --squash feature/issue-8-great-expectations`
- [ ] `git commit -m "feat(quality): great expectations pipelines (#8)"`
- [ ] `git push origin develop`
- [ ] `git branch -d feature/issue-8-great-expectations`
- [ ] Issue #8 closed on GitHub

---

## Design Notes
- Usaremos la validación en memoria (Pandas) ya que nuestro pipeline de ingestión planea levantar la data de las APIs, transformarla a un DataFrame unificado de Pydantic y luego lanzar el Checkpoint de Great Expectations antes de enviarla a BigQuery o Kafka.
