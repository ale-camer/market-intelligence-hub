with coingecko_quotes as (
    select
        ticker,
        current_price,
        market_cap,
        volume_24h,
        price_change_pct_24h,
        currency,
        source_name,
        ingested_at
    from {{ ref('stg_coingecko__markets') }}
),

yahoo_quotes as (
    select
        ticker,
        current_price,
        market_cap,
        volume_24h,
        price_change_pct_24h,
        currency,
        source_name,
        ingested_at
    from {{ ref('stg_yahoo__quotes') }}
),

combined as (
    select * from coingecko_quotes
    union all
    select * from yahoo_quotes
)

select
    ticker,
    current_price,
    market_cap,
    volume_24h,
    price_change_pct_24h,
    currency,
    source_name,
    ingested_at
from combined
