# Issue #12 — BigQuery Loader

**Branch**: `feature/issue-12-bigquery-loader`
**Milestone**: M3 — Storage & Warehouse
**Depends on**: Issue #11 ✅
**Status**: 🟡 Not Started

---

## Objective

Desarrollar el componente de carga (Loader) analítico hacia **GCP BigQuery** usando la librería `google-cloud-bigquery`. Este componente será el responsable de persistir las entidades extraídas en el Data Warehouse, garantizando la correcta gestión de esquemas (`SchemaField`), particionado de tablas y optimización en las cargas (Load Jobs).

---

## Architecture

- **`src/loaders/bigquery/`**: Directorio de la lógica de persistencia analítica (Data Warehouse).
  - `client.py`: Wrapper sobre el cliente nativo de BigQuery que inicializa y gestiona las credenciales de GCP.
  - `schemas.py`: Definición explícita de los esquemas de las tablas mediante la API de BigQuery.
  - `repository.py`: Repositorio especializado en ejecutar operaciones de inserción masiva (`Load Jobs` o inserciones basadas en DataFrames).

---

## Checklist

### 🌿 Step 1 — Branch & Setup
- [ ] Asegurarse de tener `develop` actualizado: `git checkout develop && git pull`.
- [ ] Crear rama de feature: `git checkout -b feature/issue-12-bigquery-loader`.
- [ ] Validar en `pyproject.toml` la existencia de dependencias como `google-cloud-bigquery` y `pandas`.

### ⚙️ Step 2 — BigQuery Client Setup
- [ ] Desarrollar `src/loaders/bigquery/client.py`.
- [ ] Implementar la clase `BigQueryClient` para instanciar el cliente nativo (`bigquery.Client()`).
- [ ] Configurar lecturas de variables de entorno para `GCP_PROJECT_ID` y `GCP_DATASET_ID`.

### 🛠️ Step 3 — BigQuery Schemas
- [ ] Desarrollar `src/loaders/bigquery/schemas.py`.
- [ ] Crear la estructura `market_quotes_schema` empleando objetos `bigquery.SchemaField` con sus tipos de datos nativos en BigQuery (e.g. `FLOAT64`, `TIMESTAMP`, `STRING`).
- [ ] Crear las estructuras análogas para `financial_news_schema` y `price_history_schema`.

### 💾 Step 4 — BigQuery Repository
- [ ] Desarrollar `src/loaders/bigquery/repository.py`.
- [ ] Función `create_tables_if_not_exist()` para instanciar las tablas en BigQuery asociándolas a los esquemas creados en el Step 3, y de ser posible, definiendo particionamiento por `TIMESTAMP`.
- [ ] Función `load_market_quotes_from_dataframe(df: pd.DataFrame)` para realizar un **Load Job** eficiente hacia BigQuery usando `client.load_table_from_dataframe()`.
- [ ] Implementar la lógica de carga para noticias (`load_news_articles`) y velas de precio (`load_price_bars`).

### 🧪 Step 5 — Local Tests (Mocks)
- [ ] Crear el archivo `tests/unit/loaders/test_bigquery.py`.
- [ ] Utilizar `unittest.mock` para aislar (mockear) la llamada a `bigquery.Client` y evitar pegarle a la API real de Google Cloud.
- [ ] Validar que los repositorios transforman la data correctamente al formato de DataFrame esperado y configuran el `LoadJobConfig` con el esquema respectivo.

### 🔀 Step 6 — Commit, Merge & Close
- [ ] `make format && make lint && make typecheck && make coverage`
- [ ] `git add -A`
- [ ] `git commit -m "feat(storage): implement bigquery loader with schema management (#12)"`
- [ ] `git push origin feature/issue-12-bigquery-loader`
- [ ] Levantar PR hacia `develop`, aprobar y mergear.
- [ ] Issue #12 closed on GitHub.

---

## Design Notes
- Las tablas en BigQuery se orientan al almacenamiento columnar analítico. A diferencia de Postgres (donde hicimos un upsert relacional), en BigQuery priorizaremos la adición de nuevas particiones temporales (modo "Append").
- Para BigQuery, es preferible el uso de **Load Jobs** mediante Pandas DataFrames ya que son operaciones asíncronas gratuitas, a diferencia de los *Streaming Inserts* tradicionales (insert_rows_json) que sí generan un costo por giga insertado.
