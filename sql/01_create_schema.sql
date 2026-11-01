-- ============================================================
-- Olist Data Warehouse
-- Physical schema
-- ============================================================

-- ============================================================
-- 1. DIM_DATE
-- ============================================================

CREATE TABLE dim_date (
    date_id INTEGER PRIMARY KEY,
    date DATE NOT NULL UNIQUE,
    month SMALLINT NOT NULL,
    quarter SMALLINT NOT NULL,
    year SMALLINT NOT NULL,

    CONSTRAINT chk_dim_date_month
        CHECK (month BETWEEN 1 AND 12),

    CONSTRAINT chk_dim_date_quarter
        CHECK (quarter BETWEEN 1 AND 4)
);


-- ============================================================
-- 2. DIM_PRODUCT
-- ============================================================

CREATE TABLE dim_product (
    product_id VARCHAR(32) PRIMARY KEY,
    category TEXT,
    category_english TEXT,
    name_length INTEGER,
    description_length INTEGER,
    photos_qty INTEGER,
    weight_g NUMERIC,
    length_cm NUMERIC,
    height_cm NUMERIC,
    width_cm NUMERIC
);


-- ============================================================
-- 3. DIM_SELLER
-- ============================================================

CREATE TABLE dim_seller (
    seller_id VARCHAR(32) PRIMARY KEY,
    zip_code_prefix INTEGER,
    city TEXT,
    state VARCHAR(2)
);


-- ============================================================
-- 4. DIM_CUSTOMER
-- ============================================================

CREATE TABLE dim_customer (
    customer_key BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    customer_unique_id VARCHAR(32) NOT NULL UNIQUE,
    customer_id VARCHAR(32),
    zip_code_prefix INTEGER,
    city TEXT,
    state VARCHAR(2)
);


-- ============================================================
-- 5. FACT_SALES
-- ============================================================

CREATE TABLE fact_sales (
    order_id VARCHAR(32) NOT NULL,
    order_item_id INTEGER NOT NULL,
    product_id VARCHAR(32) NOT NULL,
    seller_id VARCHAR(32) NOT NULL,
    customer_key BIGINT NOT NULL,
    date_id INTEGER NOT NULL,
    price NUMERIC(12, 2) NOT NULL,

    PRIMARY KEY (order_id, order_item_id),

    CONSTRAINT fk_fact_sales_product
        FOREIGN KEY (product_id)
        REFERENCES dim_product(product_id),

    CONSTRAINT fk_fact_sales_seller
        FOREIGN KEY (seller_id)
        REFERENCES dim_seller(seller_id),

    CONSTRAINT fk_fact_sales_customer
        FOREIGN KEY (customer_key)
        REFERENCES dim_customer(customer_key),

    CONSTRAINT fk_fact_sales_date
        FOREIGN KEY (date_id)
        REFERENCES dim_date(date_id)
);