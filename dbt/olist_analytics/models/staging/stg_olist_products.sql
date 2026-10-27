
-- Préparation du catalogue des produits pour le modèle dimensionnel

WITH source AS (

    SELECT *
    FROM {{ source('raw', 'olist_products') }}

),

renamed AS (

    SELECT
        product_id,

        -- Catégorie originale en portugais
        product_category_name,

        -- Correction des noms de colonnes
        product_name_lenght AS product_name_length,
        product_description_lenght AS product_description_length,

        -- Caractéristiques du produit
        product_photos_qty,
        product_weight_g,
        product_length_cm,
        product_height_cm,
        product_width_cm

    FROM source

)

SELECT *
FROM renamed
