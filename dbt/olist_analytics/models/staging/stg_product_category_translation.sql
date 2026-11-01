
-- Préparation des traductions des catégories de produits

WITH source AS (

    SELECT *
    FROM {{ source('raw', 'product_category_name_translation') }}

),

renamed AS (

    SELECT
        product_category_name AS category_name_pt,
        product_category_name_english AS category_name_en

    FROM source

)

SELECT *
FROM renamed
