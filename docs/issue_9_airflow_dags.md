# Issue #9 — Airflow DAGs

**Branch**: `feature/issue-9-airflow-dags`
**Milestone**: M2 — Transformation & Quality
**Depends on**: Issue #8 ✅
**Status**: 🟡 Not Started

---

## Objective

Configurar **Apache Airflow** para la orquestación del flujo de datos. El objetivo de este issue es crear los Directed Acyclic Graphs (DAGs) que integren las fases de extracción de datos (Issue 1-3), validación de calidad con Great Expectations (Issue 8) y preparativos de transformación. 

---

## Architecture

- **`dags/`**: Directorio principal de Airflow donde residen las definiciones de los DAGs. La lógica pesada no debe residir aquí, sino ser importada desde `src/`.
- **DAGs Principales**:
  - `daily_market_data_pipeline`: DAG que corre diariamente para orquestar la extracción de precios y métricas de Yahoo Finance/CoinGecko, validarlos y dar pie a dbt.
  - `hourly_news_sentiment_pipeline`: DAG que corre periódicamente (ej. cada hora) para extraer noticias, validarlas y procesarlas.
- **TaskFlow API**: Usaremos los decoradores modernos de Airflow (`@dag`, `@task`) para estructurar los grafos de manera limpia.

---

## Checklist

### 🌿 Step 1 — Branch & Setup
- [ ] `git checkout develop`
- [ ] `git checkout -b feature/issue-9-airflow-dags`
- [ ] Agregar `"apache-airflow>=2.8.0"` (y cualquier provider necesario como dbt, si aplica) a `dependencies` en `pyproject.toml`.
- [ ] Ejecutar `pip install -e ".[dev]"`.

### ⚙️ Step 2 — Configuration & Scaffolding
- [ ] Asegurarse de que existe el directorio `dags/` en la raíz (creado en el issue #0).
- [ ] Verificar que `dags/__pycache__/` y cualquier base local `airflow.db` estén listados en el `.gitignore`.
- [ ] (Opcional) Configurar la variable de entorno `AIRFLOW_HOME` apuntando al directorio raíz del proyecto localmente para inicializar la BD de pruebas con `airflow db migrate`.

### 🛠️ Step 3 — DAG Definitions
Crear los siguientes scripts dentro del directorio `dags/`:

- [ ] **`dags/market_data_dag.py`**:
  - Definir el DAG `daily_market_data_pipeline` con schedule_interval `@daily`.
  - Crear tareas orquestadas para:
    1. **Extract**: Llamar a las funciones de `src/extractors/` para Yahoo Finance y CoinGecko.
    2. **Validate**: Llamar a la validación de Great Expectations usando `market_quotes_checkpoint` / `price_history_checkpoint`.
    3. **Transform**: Agregar un dummy operator o BashOperator (placeholder temporal) que representará la corrida de los modelos de dbt (Issue 6 y 7).

- [ ] **`dags/news_pipeline_dag.py`**:
  - Definir el DAG `hourly_news_pipeline` con schedule_interval `@hourly`.
  - Crear tareas orquestadas para:
    1. **Extract**: Obtener noticias recientes desde el extractor de NewsAPI.
    2. **Validate**: Correr la validación con `news_articles_checkpoint`.
    3. **Transform**: Placeholder para procesamiento de texto/sentimiento o dbt.

### 🧪 Step 4 — Unit Tests & Validation
- [ ] Crear archivo `tests/unit/orchestration/test_dags.py`.
- [ ] Añadir una suite de pruebas usando el objeto `DagBag` de Airflow que verifique lo siguiente:
  - Los archivos `.py` en `dags/` no contienen errores de sintaxis o importación.
  - La cuenta de DAGs cargados exitosamente es al menos 2.
  - Los DAGs tienen los IDs y tareas esperadas sin ciclos en el grafo (DAG integrity check).
- [ ] Ejecutar `make format && make lint && make typecheck && make coverage`.

### 🔀 Step 5 — Commit, Merge & Close
- [ ] `git add -A`
- [ ] `git commit -m "feat(orchestration): add airflow dags definitions (#9)"`
- [ ] `git push origin feature/issue-9-airflow-dags`
- [ ] `git checkout develop`
- [ ] `git merge --squash feature/issue-9-airflow-dags`
- [ ] `git commit -m "feat(orchestration): airflow dags and pipelines (#9)"`
- [ ] `git push origin develop`
- [ ] `git branch -d feature/issue-9-airflow-dags`
- [ ] Issue #9 closed on GitHub

---

## Design Notes
- **Lógica separada**: Es una buena práctica mantener el código de extracción/validación en `src/` e importar esas funciones hacia los operators (ej. `PythonOperator` o `@task`) dentro de `dags/`. Esto permite probar la lógica de negocio usando pytest de forma nativa sin tener un entorno Airflow levantado.
- Para el envío de DataFrames entre tareas (XComs), ten cuidado con el límite de tamaño. Si la cantidad de datos es alta, se deben persistir localmente (o en GCS/S3) y pasar sólo las rutas de los archivos entre las tareas.
