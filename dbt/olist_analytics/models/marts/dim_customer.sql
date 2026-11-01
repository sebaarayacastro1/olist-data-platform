
-- Dimension des clients Olist
-- Une ligne par client réel
-- Localisation de la commande la plus récente

WITH customers AS (

    SELECT
        customer_id,
        customer_unique_id,
        zip_code_prefix,
        city,
        state

    FROM {{ ref('stg_olist_customers') }}

),

orders AS (

    SELECT
        order_id,
        customer_id,
        purchased_at

    FROM {{ ref('stg_olist_orders') }}

),

customer_history AS (

    SELECT
        c.customer_id,
        c.customer_unique_id,
        c.zip_code_prefix,
        c.city,
        c.state,
        o.order_id,
        o.purchased_at

    FROM customers AS c

    LEFT JOIN orders AS o
        ON c.customer_id = o.customer_id

),

ranked_customers AS (

    SELECT
        *,
        ROW_NUMBER() OVER (
            PARTITION BY customer_unique_id
            ORDER BY
                purchased_at DESC NULLS LAST,
                order_id DESC NULLS LAST,
                customer_id DESC
        ) AS location_rank

    FROM customer_history

),

latest_customers AS (

    SELECT
        customer_unique_id,
        zip_code_prefix,
        city,
        state

    FROM ranked_customers
    WHERE location_rank = 1

),

final AS (

    SELECT
        -- Clé technique déterministe pour ce jeu de données
        ROW_NUMBER() OVER (
            ORDER BY customer_unique_id
        )::BIGINT AS customer_key,

        customer_unique_id,
        zip_code_prefix,
        city,
        state

    FROM latest_customers

)

SELECT *
FROM final
