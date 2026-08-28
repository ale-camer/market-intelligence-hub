# Issue #10 — Integration Tests (Pipeline)

**Branch**: `feature/issue-10-integration-tests`
**Milestone**: M2 — Transformation & Quality
**Depends on**: Issue #9 ✅
**Status**: 🟡 Not Started

---

## Objective

Desarrollar pruebas de integración End-to-End (E2E) que validen el correcto funcionamiento en conjunto de los componentes desarrollados en este Milestone y el anterior. Esto incluye la extracción de datos (Issue 1-3), validación de calidad con Great Expectations (Issue 8), y la correcta ejecución de los DAGs de Airflow (Issue 9).

Al ser este el **último issue del Milestone 2 (M2)**, su finalización incluirá el proceso de release: fusionar los cambios hacia `develop` y posteriormente levantar el Pull Request de `develop` hacia `main`.

---

## Architecture

- **`tests/integration/`**: Directorio principal para pruebas que involucren múltiples componentes interactuando entre sí (a diferencia de `tests/unit/`).
- **Pipeline de Pruebas**: Simulará un flujo completo:
  1. Llamada a extractores (usando mocks o sandboxes si es necesario para evitar límites de API).
  2. Validación de los esquemas y restricciones mediante los checkpoints de GX.
  3. Verificación de que la tarea de Airflow podría correr exitosamente.

---

## Checklist

### 🌿 Step 1 — Branch & Setup
- [ ] Asegurar estar en `develop` actualizado: `git checkout develop && git pull`.
- [ ] Crear la rama del issue: `git checkout -b feature/issue-10-integration-tests`.
- [ ] Verificar entorno activo y dependencias: `pip install -e ".[dev]"`.

### 🧪 Step 2 — Integration Tests Setup
- [ ] Crear/verificar el directorio `tests/integration/`.
- [ ] Crear un archivo `tests/integration/test_pipeline_e2e.py`.

### 🛠️ Step 3 — E2E Test Cases Definition
Desarrollar pruebas integradas en `test_pipeline_e2e.py` que comprueben:
- [ ] **Market Data Flow**: Extraer precios ficticios simulando `coingecko`/`yahoo_finance`, construir el DataFrame y pasarlo por el checkpoint `market_quotes_checkpoint` validando que se aprueba (`success == True`).
- [ ] **News Flow**: Extraer noticias ficticias, y validarlas contra `news_articles_checkpoint`.
- [ ] **Airflow + GX**: Probar el comportamiento integrado llamando a la lógica subyacente de las tareas de Airflow (`extract_market_data` y `validate_market_data`) para asegurar que el pipeline retorna los estados correctos sin fallar por excepciones no controladas.

### ⚙️ Step 4 — Quality & Coverage
- [ ] Ejecutar el set completo de validación estática y pruebas (unitarias + integración): `make format && make lint && make typecheck && make coverage`.
- [ ] Garantizar que la cobertura global (`--cov=src`) se mantiene por encima del **80%** tras incorporar las nuevas pruebas de integración.

### 🔀 Step 5 — Commit, Merge & Close
- [ ] `git add -A`
- [ ] `git commit -m "test(integration): add e2e pipeline tests (#10)"`
- [ ] `git push origin feature/issue-10-integration-tests`
- [ ] `git checkout develop`
- [ ] `git merge --squash feature/issue-10-integration-tests`
- [ ] `git commit -m "test(integration): pipeline end-to-end tests (#10)"`
- [ ] `git push origin develop`
- [ ] `git branch -d feature/issue-10-integration-tests`
- [ ] Issue #10 closed on GitHub

### 🚀 Step 6 — Milestone M2 Release (Merge to `main`)
Dado que el **Milestone M2** está completo y en verde:
- [ ] Levantar un Pull Request (PR) en GitHub desde `develop` hacia `main` (Título sugerido: `Release: Milestone M2 - Transformation & Quality`).
- [ ] Aprobar y mergear el PR en GitHub (usando merge commit estandar, o rebase).
- [ ] `git checkout main && git pull origin main`.
- [ ] Milestone M2 marcado como completado en el tracker.

---

## Design Notes
- Las pruebas de integración en este punto no escribirán en bases de datos reales ni enviarán Kafka messages, ya que eso corresponde al M3 (Storage & Warehouse). El objetivo es asegurar que la lógica de "Extracción -> Validación de Calidad" fluye correctamente.
- Recuerda utilizar `pytest.fixture` para modularizar configuraciones, inicialización de contextos de Great Expectations y simulaciones de datos (mocks) para acelerar las corridas E2E locales.
