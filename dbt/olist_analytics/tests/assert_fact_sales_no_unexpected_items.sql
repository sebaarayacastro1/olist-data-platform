
-- Vérifier qu'aucun article supplémentaire n'existe dans fact_sales

SELECT
    order_id,
    order_item_id
FROM {{ ref('fact_sales') }}

EXCEPT

SELECT
    order_id,
    order_item_id
FROM {{ source('raw', 'olist_order_items') }}
