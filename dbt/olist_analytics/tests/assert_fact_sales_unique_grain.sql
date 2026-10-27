
-- Vérifier l'unicité du grain de fact_sales

SELECT
    order_id,
    order_item_id,
    COUNT(*) AS row_count

FROM {{ ref('fact_sales') }}

GROUP BY
    order_id,
    order_item_id

HAVING COUNT(*) > 1
