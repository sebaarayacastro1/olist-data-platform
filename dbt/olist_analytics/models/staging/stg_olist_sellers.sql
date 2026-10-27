
-- Préparation des vendeurs pour le modèle dimensionnel

WITH source AS (

    SELECT *
    FROM {{ source('raw', 'olist_sellers') }}

),

renamed AS (

    SELECT
        seller_id,

        -- Informations géographiques du vendeur
        seller_zip_code_prefix AS zip_code_prefix,
        seller_city AS city,
        seller_state AS state

    FROM source

)

SELECT *
FROM renamed
