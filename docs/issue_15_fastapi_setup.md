# Issue #15 — FastAPI Application Setup

**Branch**: `feature/issue-15-fastapi-setup`
**Milestone**: M4 — API & Serving
**Depends on**: Issue #14 ✅ (M3 Cerrado)
**Status**: 🟡 Not Started

---

## Objective

Inicializar y configurar el esqueleto base de la aplicación web utilizando **FastAPI**. El objetivo es establecer una arquitectura robusta mediante el patrón **Application Factory**, configurar los middlewares esenciales (CORS), preparar el manejo global de excepciones y dejar listo el enrutador de monitoreo de estado (`health check`). Todo esto sentará las bases para los endpoints de negocio de los siguientes issues.

---

## Architecture

- **`src/api/`**: Directorio raíz de la capa web.
  - `main.py`: Contiene el patrón App Factory (`create_app()`).
  - `config.py`: Configuraciones específicas de la API (títulos, versiones, prefijos).
  - `dependencies.py`: Inyector de dependencias (repositorios, clientes de DB).
  - `middlewares.py`: Middlewares globales (e.g., tiempos de respuesta, CORS).
  - `exceptions.py`: Manejadores globales de errores HTTP.
  - `routers/`:
    - `health.py`: Endpoint simple (`/health`) para probar que el servidor funciona.

---

## Checklist

### 🌿 Step 1 — Branch & Dependencies
- [ ] Asegurar rama actualizada: `git checkout develop && git pull`.
- [ ] Crear rama de feature: `git checkout -b feature/issue-15-fastapi-setup`.
- [ ] Validar o agregar dependencias: `fastapi` y `uvicorn` en `pyproject.toml`.

### ⚙️ Step 2 — Configuration & Application Factory
- [ ] Crear `src/api/config.py` definiendo clase `APIConfig` (APP_NAME, VERSION, API_PREFIX).
- [ ] Crear `src/api/main.py` implementando la función `create_app() -> FastAPI`.
- [ ] Configurar metadatos en la instancia de `FastAPI(title=..., version=...)`.

### 🛡️ Step 3 — Middlewares & Exception Handlers
- [ ] Agregar el middleware `CORSMiddleware` en `create_app()` habilitando orígenes seguros (o `*` para local).
- [ ] Crear `src/api/exceptions.py` con handlers custom (opcionalmente capturar errores comunes y pasarlos a formato JSON HTTP estandarizado).

### 🚦 Step 4 — Health Check Router
- [ ] Crear `src/api/routers/health.py`.
- [ ] Implementar un endpoint `GET /health` que devuelva `{"status": "ok", "version": "1.0.0"}`.
- [ ] Registrar este router dentro de `create_app()` en `main.py`.

### 🚀 Step 5 — API Entrypoint (Uvicorn)
- [ ] Asegurar un punto de entrada para levantar la app. (Crear un script `run_api.py` o agregar un comando en el `Makefile` como `make run-api` que ejecute `uvicorn src.api.main:app --reload`).

### 🔀 Step 6 — Commit, Merge & Close
- [ ] `make check` (format, lint, typecheck, coverage).
- [ ] `git add -A`
- [ ] `git commit -m "feat(api): setup fastapi application factory and core routing (#15)"`
- [ ] `git push origin feature/issue-15-fastapi-setup`
- [ ] Levantar PR hacia `develop`, aprobar y mergear.
- [ ] Issue #15 closed.

---

## Design Notes
- **App Factory Pattern**: Encapsular la creación de la app de FastAPI en `create_app()` facilita enormemente las pruebas (Testing), permitiendo instanciar versiones "en limpio" para Pytest o sobreescribir dependencias con facilidad.
- La lógica de negocio NO debe residir en los routers, estos deben delegar en repositorios/servicios (capa de abstracción que se integrará en el Issue #16).
