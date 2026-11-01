
-- Vérifier la concordance des montants totaux

WITH raw_total AS (

    SELECT SUM(price) AS total_amount
    FROM {{ source('raw', 'olist_order_items') }}

),

fact_total AS (

    SELECT SUM(price) AS total_amount
    FROM {{ ref('fact_sales') }}

)

SELECT
    r.total_amount AS raw_amount,
    f.total_amount AS fact_amount

FROM raw_total AS r
CROSS JOIN fact_total AS f

WHERE r.total_amount IS DISTINCT FROM f.total_amount
