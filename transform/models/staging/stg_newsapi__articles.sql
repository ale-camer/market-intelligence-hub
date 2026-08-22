with source as (
    select * from {{ source('raw_market_data', 'raw_newsapi_articles') }}
),

renamed as (
    select
        cast(url as string) as article_url,
        cast(title as string) as title,
        cast(description as string) as description,
        cast(image_url as string) as image_url,
        cast(author as string) as author,
        cast(published_at as timestamp) as published_at,
        cast(content as string) as content,
        cast(source_name as string) as source_name,
        cast(source_id as string) as source_id,
        cast(category as string) as category,
        'newsapi' as extractor_source,
        cast(ingested_at as timestamp) as ingested_at
    from source
)

select * from renamed
