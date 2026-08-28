# Issue #16 — Market Data Endpoints

**Branch**: `feature/issue-16-market-endpoints`
**Milestone**: M4 — API & Serving
**Depends on**: Issue #15 ✅
**Status**: 🟡 Not Started

---

## Objective

Desarrollar los endpoints core de la aplicación para exponer la lectura de datos del sistema (precios de mercado, histórico de barras y noticias financieras). Estos endpoints utilizarán **Dependency Injection (DI)** para interactuar con la capa de persistencia (`PostgresRepository`) desarrollada en el Milestone 3, promoviendo un diseño desacoplado y altamente testeable.

---

## Architecture

- **`src/api/dependencies.py`**: Proveedores de dependencias inyectables (ej. `get_db_session`, `get_postgres_repository`).
- **`src/api/routers/market.py`**: Endpoints relacionados a cotizaciones y datos históricos (OHLCV).
- **`src/api/routers/news.py`**: Endpoints para consumo de artículos financieros.
- **`src/api/main.py`**: Registro de los nuevos routers.

---

## Checklist

### 🌿 Step 1 — Branch & Setup
- [ ] Asegurar rama actualizada: `git checkout develop && git pull`.
- [ ] Crear rama de feature: `git checkout -b feature/issue-16-market-endpoints`.

### 💉 Step 2 — Dependency Injection
- [ ] Desarrollar `src/api/dependencies.py`.
- [ ] Implementar un generador asíncrono/síncrono `get_db_session()` que instancie la conexión a la base de datos a través de SQLAlchemy y haga el cierre seguro (yield).
- [ ] Implementar `get_postgres_repository(session=Depends(get_db_session))` que retorne una instancia configurada de `PostgresRepository`.

### 📈 Step 3 — Market Data Router
- [ ] Crear `src/api/routers/market.py`.
- [ ] Implementar endpoint `GET /market/quotes/{ticker}` para obtener la cotización más reciente de un activo.
- [ ] Implementar endpoint `GET /market/bars/{ticker}` para obtener el histórico de precios, aceptando query params de paginación (`limit`, `offset`) o rangos de fechas.
- [ ] Manejar respuestas HTTP 404 de manera limpia si el ticker no existe en la base de datos utilizando `HTTPException`.

### 📰 Step 4 — News Router
- [ ] Crear `src/api/routers/news.py`.
- [ ] Implementar endpoint `GET /news` para obtener las últimas noticias.
- [ ] Añadir soporte para parámetros de consulta opcionales: `?category=crypto` o `?source=newsapi`.
- [ ] Implementar paginación básica (`limit`, `offset`).

### 🔌 Step 5 — Router Registration
- [ ] Importar y registrar `market.router` y `news.router` dentro de `create_app()` en `src/api/main.py` bajo el prefijo `APIConfig.API_PREFIX`.

### 🧪 Step 6 — API Unit Tests (Mocks)
- [ ] Crear `tests/unit/api/test_market.py` y `tests/unit/api/test_news.py`.
- [ ] Utilizar `app.dependency_overrides[get_postgres_repository]` para inyectar un repositorio mockeado (evitando llamadas reales a la DB en las pruebas unitarias).
- [ ] Validar los status codes (200 OK, 404 Not Found) y las estructuras de los JSON de respuesta.

### 🔀 Step 7 — Commit, Merge & Close
- [ ] `make check` (format, lint, typecheck, coverage).
- [ ] `git add -A`
- [ ] `git commit -m "feat(api): implement market and news data endpoints with di (#16)"`
- [ ] `git push origin feature/issue-16-market-endpoints`
- [ ] Levantar PR hacia `develop`, aprobar y mergear.
- [ ] Issue #16 closed.

---

## Design Notes
- **Separation of Concerns:** Los routers de FastAPI solo deben validar las peticiones HTTP y formatear respuestas. Toda la lógica de obtención de datos y consultas SQL debe seguir encapsulada en el `PostgresRepository` que es inyectado por FastAPI (`Depends`).
- **Dependency Overrides:** Esta arquitectura permite que en la fase de test (Paso 6) inyectemos un mock del repositorio sin necesidad de modificar el código productivo.
