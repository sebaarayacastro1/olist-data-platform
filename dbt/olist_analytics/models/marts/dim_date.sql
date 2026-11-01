
-- Dimension calendrier pour les analyses de ventes
-- Une ligne par jour entre la première et la dernière commande

WITH date_bounds AS (

    SELECT
        MIN(purchased_at)::DATE AS min_date,
        MAX(purchased_at)::DATE AS max_date

    FROM {{ ref('stg_olist_orders') }}

),

date_series AS (

    SELECT
        GENERATE_SERIES(
            min_date,
            max_date,
            INTERVAL '1 day'
        )::DATE AS date

    FROM date_bounds

),

final AS (

    SELECT
        TO_CHAR(date, 'YYYYMMDD')::INTEGER AS date_id,
        date,
        EXTRACT(MONTH FROM date)::INTEGER AS month,
        EXTRACT(QUARTER FROM date)::INTEGER AS quarter,
        EXTRACT(YEAR FROM date)::INTEGER AS year

    FROM date_series

)

SELECT *
FROM final
