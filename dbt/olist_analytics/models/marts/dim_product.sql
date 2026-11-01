
-- Dimension des produits avec catégories multilingues

WITH products AS (

    SELECT *
    FROM {{ ref('stg_olist_products') }}

),

translations_en AS (

    SELECT *
    FROM {{ ref('stg_product_category_translation') }}

),

translations_fr AS (

    SELECT *
    FROM {{ ref('product_categories_fr') }}

),

final AS (

    SELECT
        p.product_id,

        -- Catégories en portugais, anglais et français
        p.product_category_name AS category_name_pt,
        t_en.category_name_en,
        t_fr.category_name_fr,

        -- Caractéristiques du produit
        p.product_name_length AS name_length,
        p.product_description_length AS description_length,
        p.product_photos_qty AS photos_qty,
        p.product_weight_g AS weight_g,
        p.product_length_cm AS length_cm,
        p.product_height_cm AS height_cm,
        p.product_width_cm AS width_cm

    FROM products AS p

    LEFT JOIN translations_en AS t_en
        ON p.product_category_name = t_en.category_name_pt

    LEFT JOIN translations_fr AS t_fr
        ON p.product_category_name = t_fr.category_name_pt

)

SELECT *
FROM final
