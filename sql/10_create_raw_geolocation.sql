
-- Création de la table brute de géolocalisation
-- Conservation de toutes les lignes, y compris les doublons

CREATE TABLE IF NOT EXISTS raw.olist_geolocation (
    geolocation_row_id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    geolocation_zip_code_prefix VARCHAR(5),
    geolocation_lat DOUBLE PRECISION,
    geolocation_lng DOUBLE PRECISION,
    geolocation_city TEXT,
    geolocation_state VARCHAR(2)
);
