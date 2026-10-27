
-- Vérifier qu'aucun article source ne manque dans fact_sales

SELECT
    order_id,
    order_item_id
FROM {{ source('raw', 'olist_order_items') }}

EXCEPT

SELECT
    order_id,
    order_item_id
FROM {{ ref('fact_sales') }}
