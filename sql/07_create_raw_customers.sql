
-- Création de la table brute des clients

CREATE TABLE IF NOT EXISTS raw.olist_customers (
    customer_id VARCHAR(32) PRIMARY KEY,
    customer_unique_id VARCHAR(32),
    customer_zip_code_prefix VARCHAR(5),
    customer_city TEXT,
    customer_state VARCHAR(2)
);
