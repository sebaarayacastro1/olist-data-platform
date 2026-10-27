
-- Dimension des vendeurs Olist
-- Une ligne par vendeur

WITH sellers AS (

    SELECT
        seller_id,
        zip_code_prefix,
        city,
        state

    FROM {{ ref('stg_olist_sellers') }}

)

SELECT
    seller_id,
    zip_code_prefix,
    city,
    state
FROM sellers
