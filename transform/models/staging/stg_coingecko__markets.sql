with source as (
    select * from {{ source('raw_market_data', 'raw_coingecko_markets') }}
),

renamed as (
    select
        cast(id as string) as id,
        upper(cast(symbol as string)) as ticker,
        'crypto' as asset_class,
        cast(name as string) as name,
        cast(current_price as numeric) as current_price,
        cast(market_cap as int64) as market_cap,
        cast(total_volume as numeric) as volume_24h,
        'USD' as currency,
        'coingecko' as source_name,
        cast(price_change_percentage_24h as numeric) as price_change_pct_24h,
        cast(last_updated as timestamp) as last_updated_at,
        cast(ingested_at as timestamp) as ingested_at
    from source
)

select * from renamed
