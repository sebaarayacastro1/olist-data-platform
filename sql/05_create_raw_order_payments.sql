
-- Création de la table brute des paiements des commandes

CREATE TABLE IF NOT EXISTS raw.olist_order_payments (
    order_id VARCHAR(32) NOT NULL,
    payment_sequential INTEGER NOT NULL,
    payment_type TEXT,
    payment_installments INTEGER,
    payment_value NUMERIC(10, 2),

    CONSTRAINT pk_olist_order_payments
        PRIMARY KEY (order_id, payment_sequential)
);
