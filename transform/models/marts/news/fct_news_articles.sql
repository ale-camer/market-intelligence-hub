with articles as (
    select
        article_url,
        title,
        description,
        image_url,
        author,
        published_at,
        content,
        source_name,
        source_id,
        category,
        extractor_source,
        ingested_at
    from {{ ref('stg_newsapi__articles') }}
),

deduplicated as (
    select
        *,
        row_number() over (partition by article_url order by published_at desc) as rn
    from articles
)

select
    article_url,
    title,
    description,
    image_url,
    author,
    published_at,
    content,
    source_name,
    source_id,
    category,
    extractor_source,
    ingested_at
from deduplicated
where rn = 1
