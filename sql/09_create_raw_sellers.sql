
-- Création de la table brute des vendeurs

CREATE TABLE IF NOT EXISTS raw.olist_sellers (
    seller_id VARCHAR(32) PRIMARY KEY,
    seller_zip_code_prefix VARCHAR(5),
    seller_city TEXT,
    seller_state VARCHAR(2)
);
