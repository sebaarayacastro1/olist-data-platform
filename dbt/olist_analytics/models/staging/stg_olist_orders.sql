
-- Préparation des commandes pour les modèles analytiques

WITH source AS (

    SELECT *
    FROM {{ source('raw', 'olist_orders') }}

),

renamed AS (

    SELECT
        order_id,
        customer_id,
        order_status,

        -- Dates et horodatages des commandes
        order_purchase_timestamp AS purchased_at,
        order_approved_at AS approved_at,
        order_delivered_carrier_date AS delivered_to_carrier_at,
        order_delivered_customer_date AS delivered_to_customer_at,
        order_estimated_delivery_date AS estimated_delivery_at

    FROM source

)

SELECT *
FROM renamed
