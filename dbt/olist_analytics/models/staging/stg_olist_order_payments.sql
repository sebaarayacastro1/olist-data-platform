
-- Préparation des paiements pour les analyses futures

WITH source AS (

    SELECT *
    FROM {{ source('raw', 'olist_order_payments') }}

),

renamed AS (

    SELECT
        order_id,
        payment_sequential,
        payment_type,
        payment_installments,
        payment_value

    FROM source

)

SELECT *
FROM renamed
