# Issue #17 — Auth & Rate Limiting

**Branch**: `feature/issue-17-auth`
**Milestone**: M4 — API & Serving
**Depends on**: Issue #16 ✅
**Status**: 🟡 Not Started

---

## Objective

Proteger la API mediante la implementación de autenticación basada en **JSON Web Tokens (JWT)** y prevenir el abuso de la infraestructura mediante limitación de tasa de peticiones (**Rate Limiting**). Se desarrollará un flujo de autenticación estándar mediante OAuth2PasswordBearer y se asegurarán los endpoints de datos de mercado y noticias construidos en el issue anterior.

---

## Architecture

- **`src/api/security.py`**: Lógica core de seguridad (hasheo de contraseñas, generación y decodificación de JWT).
- **`src/api/routers/auth.py`**: Endpoint `/token` para el inicio de sesión y emisión de tokens.
- **`src/api/dependencies.py`**: Nuevo inyector `get_current_user` para validar el token en cada petición.
- **Rate Limiting**: Integración global o por endpoint (ej. mediante la librería `slowapi` o custom middleware).

---

## Checklist

### 🌿 Step 1 — Branch & Dependencies
- [ ] Asegurar rama actualizada: `git checkout develop && git pull`.
- [ ] Crear rama de feature: `git checkout -b feature/issue-17-auth`.
- [ ] Validar que `python-jose[cryptography]` y `passlib[bcrypt]` estén en `pyproject.toml`.
- [ ] Opcional: Agregar `slowapi` a `pyproject.toml` para el rate limiting estándar de FastAPI.

### 🔐 Step 2 — Security Core & Config
- [ ] Añadir configuraciones en `src/api/config.py`: `SECRET_KEY`, `ALGORITHM` (HS256), `ACCESS_TOKEN_EXPIRE_MINUTES`.
- [ ] Crear `src/api/security.py`.
- [ ] Implementar `create_access_token(data: dict)` usando `jose.jwt`.
- [ ] Implementar lógica (mockeada por ahora) de verificación de contraseñas con `passlib`.

### 🛡️ Step 3 — Auth Router & Dependency
- [ ] Crear `src/api/routers/auth.py` con el endpoint `POST /token` que reciba `OAuth2PasswordRequestForm` y devuelva un JWT válido.
- [ ] Registrar `auth.router` en `src/api/main.py`.
- [ ] En `src/api/dependencies.py`, implementar `get_current_user(token: str = Depends(oauth2_scheme))` para decodificar y validar el token entrante.

### 🛑 Step 4 — Rate Limiting
- [ ] Instanciar el `Limiter` (ej. de `slowapi`) en `src/api/main.py` pasándole la IP del cliente como llave.
- [ ] Registrar el middleware/exception handler necesario para devolver un HTTP 429 Too Many Requests cuando se exceda la cuota.
- [ ] Aplicar un límite razonable (ej. `@limiter.limit("60/minute")`) a los routers.

### 🔒 Step 5 — Secure the Endpoints
- [ ] Modificar `src/api/routers/market.py` y `src/api/routers/news.py`.
- [ ] Añadir `current_user = Depends(get_current_user)` en las firmas de los endpoints `GET /market/quotes`, `GET /market/bars` y `GET /news` para bloquear el acceso público.

### 🧪 Step 6 — API Unit Tests
- [ ] Crear `tests/unit/api/test_auth.py` para validar la correcta emisión del JWT.
- [ ] Actualizar `test_market.py` y `test_news.py` para incluir un token válido en las cabeceras `Authorization: Bearer <token>`, y verificar que sin el token devuelvan HTTP 401 Unauthorized.

### 🔀 Step 7 — Commit, Merge & Close
- [ ] `make check` (format, lint, typecheck, coverage).
- [ ] `git add -A`
- [ ] `git commit -m "feat(api): implement jwt auth and rate limiting (#17)"`
- [ ] `git push origin feature/issue-17-auth`
- [ ] Levantar PR hacia `develop`, aprobar y mergear.
- [ ] Issue #17 closed.

---

## Design Notes
- Dado que el sistema aún no cuenta con una tabla de `Users` en base de datos (y no es el foco principal del hub de datos), en el Paso 3 emplearemos un mecanismo *dummy/hardcoded* de validación de credenciales (ej. admin/admin) exclusivamente para emitir los JWT. El foco de la protección es el consumo de la API (M2M o Cliente-API), no un sistema complejo de gestión de identidades.
