
-- Préparation des avis clients pour les analyses

WITH source AS (

    SELECT *
    FROM {{ source('raw', 'olist_order_reviews') }}

),

renamed AS (

    SELECT
        review_row_id,
        review_id,
        order_id,
        review_score,

        -- Contenu de l'avis
        review_comment_title,
        review_comment_message,

        -- Horodatages de l'avis
        review_creation_date AS review_created_at,
        review_answer_timestamp AS review_answered_at

    FROM source

)

SELECT *
FROM renamed
