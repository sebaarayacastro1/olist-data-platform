
-- Vérifier que les prix des articles sont identiques à la source

SELECT
    r.order_id,
    r.order_item_id,
    r.price AS raw_price,
    f.price AS fact_price

FROM {{ source('raw', 'olist_order_items') }} AS r

INNER JOIN {{ ref('fact_sales') }} AS f
    ON r.order_id = f.order_id
   AND r.order_item_id = f.order_item_id

WHERE r.price IS DISTINCT FROM f.price
