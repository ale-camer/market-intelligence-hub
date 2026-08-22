# Issue #7 — dbt Models: staging → mart

**Branch**: `feature/issue-7-dbt-marts`
**Milestone**: M2 — Transformation & Quality
**Depends on**: Issue #6 ✅ (Staging models)
**Status**: 🟡 Not Started

---

## Objective

Desarrollar los modelos analíticos (marts) en dbt. Estos modelos tomarán los datos normalizados de la capa de `staging` y los transformarán en tablas de dimensiones (`dim_`) y hechos (`fct_`) listas para ser consumidas por dashboards, reportes o algoritmos de machine learning. 

---

## Architecture

Adoptaremos el patrón de diseño Kimball (Star Schema) estructurado en dos dominios:
- **`core`**: Dimensiones compartidas a lo largo de toda la organización (ej. `dim_assets`).
- **`finance` & `news`**: Tablas de hechos de cotizaciones, precios históricos y noticias (ej. `fct_market_quotes`, `fct_price_history`, `fct_news_articles`).

---

## Checklist

### 🌿 Step 1 — Branch & Setup
- [ ] `git checkout develop`
- [ ] `git checkout -b feature/issue-7-dbt-marts`
- [ ] Crear los directorios `transform/models/marts/core`, `transform/models/marts/finance` y `transform/models/marts/news`.
- [ ] Actualizar `transform/dbt_project.yml` para materializar los modelos bajo `marts` como `table` en lugar de `view` (para mayor rendimiento en consultas analíticas).

### 📐 Step 2 — Core Dimensions (`transform/models/marts/core/`)
- [ ] **`dim_assets.sql`**: Crear una dimensión única de activos unificando (con `UNION ALL`) los `ticker`, `name` y `asset_class` provenientes de `stg_coingecko__markets` y `stg_yahoo__quotes`. Usar `row_number()` para deduplicar tickers repetidos (ej. si BTC está en ambas fuentes).

### 📈 Step 3 — Finance Facts (`transform/models/marts/finance/`)
- [ ] **`fct_market_quotes.sql`**: Unificar las cotizaciones actuales de `stg_coingecko__markets` y `stg_yahoo__quotes`. Incluir `ticker`, `current_price`, `market_cap`, `volume_24h`, `price_change_pct_24h` y `currency`.
- [ ] **`fct_price_history.sql`**: Seleccionar los datos de `stg_yahoo__history` (precios OHLCV históricos) e incluir la clave del activo.

### 📰 Step 4 — News Facts (`transform/models/marts/news/`)
- [ ] **`fct_news_articles.sql`**: Seleccionar los datos de `stg_newsapi__articles`, asegurar que no haya duplicados usando `url` o un hash generado (surrogate key) como identificador principal.

### 📝 Step 5 — Documentation & Tests (`transform/models/marts/schema.yml`)
- [ ] Crear `transform/models/marts/schema.yml`.
- [ ] Documentar los modelos `dim_assets`, `fct_market_quotes`, `fct_price_history` y `fct_news_articles`.
- [ ] Agregar tests de `unique` y `not_null` a `ticker` en `dim_assets`.
- [ ] Agregar tests de integridad referencial (`relationships`) indicando que el `ticker` de las tablas `fct_` debe existir en `dim_assets`.

### ✅ Step 6 — Verification
- [ ] Ejecutar `dbt parse --project-dir transform --profiles-dir transform` para verificar que la sintaxis SQL y las referencias del DAG (`ref()`) sean correctas sin necesidad de conectar a la base de datos real.

### 🔀 Step 7 — Commit, Merge & Close
- [ ] `git add -A`
- [ ] `git commit -m "feat(dbt): analytical marts models (#7)"`
- [ ] `git push origin feature/issue-7-dbt-marts`
- [ ] `git checkout develop`
- [ ] `git merge --squash feature/issue-7-dbt-marts`
- [ ] `git commit -m "feat(dbt): staging to mart analytical models (#7)"`
- [ ] `git push origin develop`
- [ ] `git branch -d feature/issue-7-dbt-marts`
- [ ] Issue #7 closed on GitHub

---

## Design Notes
- **Materializaciones**: Se recomienda usar `table` (o incrementales a futuro) para los marts, ya que BigQuery optimiza mejor las consultas recurrentes sobre tablas particionadas/clusterizadas que sobre vistas anidadas.
- **Deduplicación**: Al unificar datos de múltiples proveedores (como CoinGecko y Yahoo para cripto), la capa mart (`dim_assets`) es el lugar correcto para establecer reglas de prioridad o consolidación de atributos.
