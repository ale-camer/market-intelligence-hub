with history as (
    select
        ticker,
        asset_class,
        bar_timestamp,
        open_price,
        high_price,
        low_price,
        close_price,
        volume,
        bar_interval,
        source_name,
        ingested_at
    from {{ ref('stg_yahoo__history') }}
)

select
    ticker,
    asset_class,
    bar_timestamp,
    open_price,
    high_price,
    low_price,
    close_price,
    volume,
    bar_interval,
    source_name,
    ingested_at
from history
