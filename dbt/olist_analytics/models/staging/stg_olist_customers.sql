
-- Préparation des clients pour le modèle dimensionnel

WITH source AS (

    SELECT *
    FROM {{ source('raw', 'olist_customers') }}

),

renamed AS (

    SELECT
        customer_id,
        customer_unique_id,

        -- Informations géographiques du client
        customer_zip_code_prefix AS zip_code_prefix,
        customer_city AS city,
        customer_state AS state

    FROM source

)

SELECT *
FROM renamed
