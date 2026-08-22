with coingecko_assets as (
    select
        ticker,
        name,
        asset_class,
        source_name
    from {{ ref('stg_coingecko__markets') }}
),

yahoo_assets as (
    select
        ticker,
        name,
        asset_class,
        source_name
    from {{ ref('stg_yahoo__quotes') }}
),

combined as (
    select * from coingecko_assets
    union all
    select * from yahoo_assets
),

deduplicated as (
    select
        ticker,
        name,
        asset_class,
        source_name,
        row_number() over (partition by ticker order by source_name asc) as rn
    from combined
)

select
    ticker,
    name,
    asset_class,
    source_name as primary_source
from deduplicated
where rn = 1
