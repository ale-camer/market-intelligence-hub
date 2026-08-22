with source as (
    select * from {{ source('raw_market_data', 'raw_yahoo_quotes') }}
),

renamed as (
    select
        upper(cast(ticker as string)) as ticker,
        cast(asset_class as string) as asset_class,
        cast(name as string) as name,
        cast(current_price as numeric) as current_price,
        cast(market_cap as int64) as market_cap,
        cast(volume_24h as numeric) as volume_24h,
        coalesce(cast(currency as string), 'USD') as currency,
        cast(exchange as string) as exchange,
        cast(price_change_pct_24h as numeric) as price_change_pct_24h,
        'yahoo_finance' as source_name,
        cast(ingested_at as timestamp) as ingested_at
    from source
)

select * from renamed
