
-- Préparation des données géographiques Olist
-- Conservation de toutes les lignes, y compris les doublons

WITH source AS (

    SELECT *
    FROM {{ source('raw', 'olist_geolocation') }}

),

renamed AS (

    SELECT
        geolocation_row_id,
        geolocation_zip_code_prefix AS zip_code_prefix,
        geolocation_lat AS latitude,
        geolocation_lng AS longitude,
        geolocation_city AS city,
        geolocation_state AS state

    FROM source

)

SELECT *
FROM renamed
