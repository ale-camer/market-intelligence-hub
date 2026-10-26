CREATE OR REPLACE VIEW `gen-lang-client-0887473308.staging_prod.vw_p05_hub_data_health` AS
SELECT 
    source_name,
    COUNT(DISTINCT ticker) AS total_assets,
    SUM(CASE WHEN current_price IS NULL OR current_price <= 0 THEN 1 ELSE 0 END) AS invalid_price_count,
    MIN(ingested_at) AS earliest_ingestion,
    MAX(ingested_at) AS latest_ingestion,
    DATE_DIFF(CURRENT_DATE(), DATE(MAX(ingested_at)), DAY) AS days_since_last_sync,
    CASE 
        WHEN DATE_DIFF(CURRENT_DATE(), DATE(MAX(ingested_at)), DAY) <= 1
         AND SUM(CASE WHEN current_price IS NULL OR current_price <= 0 THEN 1 ELSE 0 END) = 0
        THEN 1
        ELSE 0
    END AS is_healthy
FROM `gen-lang-client-0887473308.staging_prod.fct_market_quotes`
GROUP BY source_name;
