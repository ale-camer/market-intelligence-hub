# Issue #14 — Unit Tests — Storage Layer

**Branch**: `feature/issue-14-storage-tests`
**Milestone**: M3 — Storage & Warehouse
**Depends on**: Issue #13 ✅
**Status**: 🟡 Not Started

---

## Objective

Finalizar el hito **M3 (Storage & Warehouse)** asegurando que la calidad del código de toda la capa de persistencia (PostgreSQL, BigQuery y Kafka) cumpla con los estándares del proyecto (≥ 80% de cobertura, cero errores estáticos). Al ser el último issue del milestone, este proceso culmina con un Pull Request que fusiona el código estabilizado en `develop` hacia la rama productiva `main`.

---

## Architecture Context

La capa de almacenamiento desarrollada en este hito se compone de:
- **`src/loaders/postgres/`**: Persistencia transaccional vía SQLAlchemy.
- **`src/loaders/bigquery/`**: Almacenamiento analítico columnar.
- **`src/messaging/kafka/`**: Bus de eventos asíncronos con esquemas Avro.

*Nota: Las pruebas unitarias aisladas (`tests/unit/loaders/` y `tests/unit/messaging/`) fueron implementadas iterativamente durante los Issues #11, #12 y #13 para mantener la cobertura continua.*

---

## Checklist

### 🌿 Step 1 — Branch & Setup
- [ ] `git checkout develop && git pull`.
- [ ] Crear rama de feature: `git checkout -b feature/issue-14-storage-tests`.

### 🧪 Step 2 — Verify Coverage & Code Quality
- [ ] Ejecutar el pipeline completo de validación local: `make check`.
- [ ] Confirmar que **Ruff format/lint** aprueban sin advertencias.
- [ ] Confirmar que **MyPy** aprueba estrictamente.
- [ ] Confirmar que **Pytest** ejecuta exitosamente las suites de Postgres, BigQuery y Kafka (`tests/unit/loaders/` y `tests/unit/messaging/`).
- [ ] Validar que la cobertura (`make coverage`) supera el umbral estricto del **80%**.

### 🔀 Step 3 — M3 Milestone Release (Merge to Main)
- [ ] `git add -A`
- [ ] `git commit -m "chore(tests): verify storage layer tests and prepare m3 release (#14)"`
- [ ] `git push origin feature/issue-14-storage-tests`
- [ ] **Acción GitHub 1:** Levantar y mergear PR de `feature/issue-14-storage-tests` hacia `develop`.
- [ ] **Acción GitHub 2:** Crear el **Release PR** desde `develop` hacia `main` con el título "Release: Milestone 3 (Storage & Warehouse)".
- [ ] Mergear el PR en `main` creando un commit de consolidación de release.
- [ ] Cerrar Issue #14 y marcar el Milestone M3 como completado.

---

## Design Notes
- El proceso de Release hacia `main` consolida todas las integraciones de Postgres, BigQuery y Kafka. La rama `main` debe ser siempre la representación de un hito estable e implementado en su totalidad.
