# Issue #11 — PostgreSQL Loader

**Branch**: `feature/issue-11-postgresql-loader`
**Milestone**: M3 — Storage & Warehouse
**Depends on**: Issue #10 ✅
**Status**: 🟡 Not Started

---

## Objective

Implementar el componente de carga (Loader) hacia **PostgreSQL** utilizando **SQLAlchemy ORM** para el modelado de datos y **Alembic** para el manejo de migraciones de la base de datos. Este componente será el responsable de persistir las entidades extraídas (precios y noticias) de forma estructurada en un esquema relacional.

Con este issue iniciamos formalmente el Milestone 3 (Storage & Warehouse).

---

## Architecture

- **`src/loaders/postgres/`**: Directorio de la lógica de persistencia relacional.
  - `models.py`: Clases mapeadas con SQLAlchemy Declarative Base.
  - `repository.py`: Clase encargada de manejar la sesión y las operaciones CRUD (insert/upsert) extrayendo la lógica transaccional.
- **`alembic/`**: Directorio de configuración para migraciones que controlará el historial del esquema de la base de datos de manera incremental.

---

## Checklist

### 🌿 Step 1 — Branch & Setup
- [ ] Asegurarse de tener la rama actualizada: `git checkout develop && git pull`.
- [ ] Crear rama de feature: `git checkout -b feature/issue-11-postgresql-loader`.
- [ ] Validar que dependencias clave (`sqlalchemy`, `alembic`, `psycopg2-binary`) estén presentes en `pyproject.toml`.
- [ ] Ejecutar `pip install -e ".[dev]"`.

### ⚙️ Step 2 — Alembic Initialization
- [ ] Ejecutar `alembic init alembic` en el root del proyecto.
- [ ] Ajustar el archivo `alembic.ini` y `alembic/env.py` para que la conexión a la base de datos se lea dinámicamente desde variables de entorno.
- [ ] Importar la clase base de los modelos (`Base`) dentro de `env.py` y asignarla a `target_metadata` para que Alembic pueda autogenerar migraciones comprobando contra los modelos en Python.

### 🛠️ Step 3 — SQLAlchemy ORM Models
Desarrollar el archivo `src/loaders/postgres/models.py` conteniendo:
- [ ] Clase `MarketQuoteORM`: Tabla `market_quotes` (campos: ticker, asset_class, price, market_cap, volume, timestamp de ingesta).
- [ ] Clase `FinancialArticleORM`: Tabla `financial_news` (campos: url, title, source_name, published_at, timestamp de ingesta).
- [ ] Clase `PriceHistoryORM`: Tabla `price_bars` (campos: ticker, interval, dt, open, high, low, close, volume).

### 🗄️ Step 4 — Initial Migration
- [ ] Generar la migración inicial: `alembic revision --autogenerate -m "Initial schema"`.
- [ ] Revisar cuidadosamente el script generado en `alembic/versions/` para verificar tipos, llaves foráneas e índices (ej. creación de índices por `ticker` o `published_at`).

### 💾 Step 5 — Repository Logic
Desarrollar `src/loaders/postgres/repository.py`:
- [ ] Implementar un manejador de contexto (`contextmanager`) para la sesión a partir de un Engine.
- [ ] Método `upsert_market_quote()`: Usar lógica de "Upsert" (e.g. `postgresql.insert().on_conflict_do_update()`) para evitar duplicados.
- [ ] Método `bulk_insert_news()`: Inserción en lote utilizando SQLAlchemy 2.0.

### 🧪 Step 6 — Local Tests (SQLite)
- [ ] Crear el archivo `tests/unit/loaders/test_postgres.py`.
- [ ] Usar un Engine in-memory de SQLite (`sqlite:///:memory:`) para inicializar las tablas de SQLAlchemy directamente (`Base.metadata.create_all`).
- [ ] Validar que los métodos del repositorio insertan y retornan datos correctamente mapeados sin necesidad de levantar un contenedor Postgres completo.

### 🔀 Step 7 — Commit, Merge & Close
- [ ] `make format && make lint && make typecheck && make coverage`
- [ ] `git add -A`
- [ ] `git commit -m "feat(storage): implement postgres loader with sqlalchemy and alembic (#11)"`
- [ ] `git push origin feature/issue-11-postgresql-loader`
- [ ] Levantar PR hacia `develop`, hacer merge squash.
- [ ] Issue #11 closed on GitHub.

---

## Design Notes
- Las operaciones de persistencia (Upsert) son vitales. Los datos financieros suelen solaparse cuando se consumen por ventanas de tiempo (Airflow DAGs diarios o por hora). Se debe evitar violar restricciones de unicidad.
- El repositorio (Repository Pattern) aislará al resto del código de la lógica específica de SQLAlchemy. Las funciones superiores solo deberán pasarle los objetos Pydantic validados que se crearon en el issue 4.
