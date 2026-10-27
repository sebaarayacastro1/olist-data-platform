
-- Préparation des articles de commande pour le modèle analytique

WITH source AS (

    SELECT *
    FROM {{ source('raw', 'olist_order_items') }}

),

renamed AS (

    SELECT
        order_id,
        order_item_id,
        product_id,
        seller_id,

        -- Date limite d'expédition
        shipping_limit_date AS shipping_limit_at,

        -- Montants de l'article et de la livraison
        price,
        freight_value

    FROM source

)

SELECT *
FROM renamed
