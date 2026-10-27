
-- Table de faits des ventes Olist
-- Grain : une ligne par article de commande

WITH order_items AS (

    SELECT
        order_id,
        order_item_id,
        product_id,
        seller_id,
        price

    FROM {{ ref('stg_olist_order_items') }}

),

orders AS (

    SELECT
        order_id,
        customer_id,
        purchased_at

    FROM {{ ref('stg_olist_orders') }}

),

customers AS (

    SELECT
        customer_id,
        customer_unique_id

    FROM {{ ref('stg_olist_customers') }}

),

customer_dimension AS (

    SELECT
        customer_key,
        customer_unique_id

    FROM {{ ref('dim_customer') }}

),

dates AS (

    SELECT
        date_id,
        date

    FROM {{ ref('dim_date') }}

),

final AS (

    SELECT
        i.order_id,
        i.order_item_id,
        i.product_id,
        i.seller_id,
        dc.customer_key,
        d.date_id,
        i.price

    FROM order_items AS i

    INNER JOIN orders AS o
        ON i.order_id = o.order_id

    INNER JOIN customers AS c
        ON o.customer_id = c.customer_id

    INNER JOIN customer_dimension AS dc
        ON c.customer_unique_id = dc.customer_unique_id

    INNER JOIN dates AS d
        ON o.purchased_at::DATE = d.date

)

SELECT *
FROM final
