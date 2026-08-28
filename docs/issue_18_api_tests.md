# Issue #18 — API Tests & Milestone 4 Closure

**Branch**: `feature/issue-18-api-tests`
**Milestone**: M4 — API & Serving
**Depends on**: Issue #17 ✅
**Status**: 🟡 Not Started

---

## Objective

Desarrollar pruebas de integración End-to-End (E2E) para la API y culminar el **Milestone 4 (API & Serving)**. Dado que las pruebas unitarias exhaustivas con *mocks* ya se implementaron en los issues 15, 16 y 17, este issue se centrará en validar el flujo completo (autenticación + consumo de datos) y en ejecutar el Release hacia `main` para dar por cerrado el Milestone 4.

---

## Architecture

- **`tests/integration/test_api_e2e.py`**: Nuevo archivo para simular un ciclo de vida real del cliente de la API (obtener token JWT válido -> inyectar cabecera `Authorization: Bearer <token>` -> consultar endpoints protegidos).

---

## Checklist

### 🌿 Step 1 — Branch & Setup
- [ ] Asegurar rama base: `git checkout develop && git pull`.
- [ ] Crear rama de feature: `git checkout -b feature/issue-18-api-tests`.

### 🧪 Step 2 — E2E API Integration Tests
- [ ] Crear `tests/integration/test_api_e2e.py`.
- [ ] Implementar un test integrador que levante la `FastAPI` app configurada.
- [ ] Realizar una petición a `POST /api/v1/auth/token` para obtener un `access_token` válido.
- [ ] Usar el token para consultar `GET /api/v1/market/quotes/BTC` y `GET /api/v1/news`.
- [ ] Validar que todas las respuestas sean HTTP 200 OK y que los datos sean coherentes.

### 🧹 Step 3 — Quality Gates
- [ ] Ejecutar `make format` y `make lint`.
- [ ] Ejecutar `make typecheck` para asegurar que `mypy` no arroje errores.
- [ ] Ejecutar `make coverage` y asegurar que la cobertura agregada se mantenga sobre el 80% (actualmente ~90%).

### 🔀 Step 4 — Commit & Merge to Develop
- [ ] `git add -A`
- [ ] `git commit -m "test(api): implement e2e api integration flow (#18)"`
- [ ] `git push origin feature/issue-18-api-tests`
- [ ] Levantar PR hacia `develop`, aprobar y mergear.

### 🚀 Step 5 — Milestone 4 Closure (Merge to Main)
- [ ] Cambiar a `main`: `git checkout main && git pull`
- [ ] Levantar y mergear **PR desde `develop` hacia `main`**.
- [ ] Crear tag del release: `git tag -a v0.4.0 -m "Release M4: API & Serving"`
- [ ] Subir tags: `git push origin v0.4.0`
- [ ] Issue #18 closed. Milestone M4 Completado.

---

## Design Notes
- El objetivo del test E2E no es re-testear la lógica de base de datos (que ya está cubierta por `test_postgres.py` y los test unitarios con *mocks*), sino **verificar la correcta integración de todos los middlewares, dependencias y enrutadores de FastAPI operando en conjunto**.
