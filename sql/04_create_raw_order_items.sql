
-- Création de la table brute des articles de commande

CREATE TABLE IF NOT EXISTS raw.olist_order_items (
    order_id VARCHAR(32) NOT NULL,
    order_item_id INTEGER NOT NULL,
    product_id VARCHAR(32),
    seller_id VARCHAR(32),
    shipping_limit_date TIMESTAMP,
    price NUMERIC(10, 2),
    freight_value NUMERIC(10, 2),

    CONSTRAINT pk_olist_order_items
        PRIMARY KEY (order_id, order_item_id)
);
