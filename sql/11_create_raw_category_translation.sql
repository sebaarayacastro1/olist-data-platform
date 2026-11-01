
-- Création de la table brute des traductions
-- Conservation des catégories originales en portugais
-- et de leurs traductions en anglais

CREATE TABLE IF NOT EXISTS raw.product_category_name_translation (
    product_category_name TEXT PRIMARY KEY,
    product_category_name_english TEXT
);
