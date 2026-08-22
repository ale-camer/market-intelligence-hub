with source as (
    select * from {{ source('raw_market_data', 'raw_yahoo_history') }}
),

renamed as (
    select
        upper(cast(ticker as string)) as ticker,
        cast(asset_class as string) as asset_class,
        cast(dt as timestamp) as bar_timestamp,
        cast(open as numeric) as open_price,
        cast(high as numeric) as high_price,
        cast(low as numeric) as low_price,
        cast(close as numeric) as close_price,
        cast(volume as numeric) as volume,
        cast(interval as string) as bar_interval,
        'yahoo_finance' as source_name,
        cast(ingested_at as timestamp) as ingested_at
    from source
)

select * from renamed
