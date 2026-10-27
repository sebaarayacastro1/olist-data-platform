# Physical Model

## 1. Objectif

Ce document traduit le modèle conceptuel défini dans `star_schema.md` en une première spécification physique destinée à une implémentation dans un Data Warehouse PostgreSQL / Supabase.

Le modèle physique précise :

- les tables à créer ;
- les colonnes ;
- les types de données ;
- les clés primaires ;
- les clés étrangères ;
- les contraintes principales.

L'objectif est de disposer d'une spécification suffisamment précise avant de commencer l'implémentation SQL et les transformations ETL.

---

## 2. Vue d'ensemble

Le modèle physique est composé de cinq tables principales :

```text
dim_date
dim_product
dim_seller
dim_customer
fact_sales
```

Le modèle conserve une structure en étoile avec `fact_sales` au centre.

```text
                         dim_date
                            │
                            │ date_id
                            ▼
dim_product ─────────► fact_sales ◄───────── dim_seller
 product_id             │   │                 seller_id
                        │   │
                  customer_key
                        │
                        ▼
                  dim_customer
```

---

# 3. Table `dim_date`

## 3.1 Grain

Une ligne représente **une date calendaire**.

## 3.2 Structure

| Colonne | Type PostgreSQL | Contraintes | Description |
|---|---|---|---|
| `date_id` | `INTEGER` | PK, NOT NULL | Clé numérique au format `YYYYMMDD` |
| `date` | `DATE` | NOT NULL, UNIQUE | Date complète |
| `month` | `SMALLINT` | NOT NULL | Numéro du mois, de 1 à 12 |
| `quarter` | `SMALLINT` | NOT NULL | Numéro du trimestre, de 1 à 4 |
| `year` | `SMALLINT` | NOT NULL | Année |

## 3.3 Contraintes

- `date_id` est la clé primaire.
- `date` doit être unique.
- `month` doit être compris entre 1 et 12.
- `quarter` doit être compris entre 1 et 4.
- `year` doit correspondre à l'année de `date`.

## 3.4 Source

La date de vente est dérivée de :

`orders.order_purchase_timestamp`

---

# 4. Table `dim_product`

## 4.1 Grain

Une ligne représente **un produit**.

## 4.2 Structure

| Colonne | Type PostgreSQL | Contraintes | Description |
|---|---|---|---|
| `product_id` | `VARCHAR(32)` | PK, NOT NULL | Identifiant du produit provenant de la source |
| `category` | `TEXT` | NULL | Catégorie du produit |
| `category_english` | `TEXT` | NULL | Catégorie en anglais |
| `name_length` | `INTEGER` | NULL | Longueur du nom du produit |
| `description_length` | `INTEGER` | NULL | Longueur de la description |
| `photos_qty` | `INTEGER` | NULL | Nombre de photos |
| `weight_g` | `NUMERIC` | NULL | Poids du produit en grammes |
| `length_cm` | `NUMERIC` | NULL | Longueur du produit en cm |
| `height_cm` | `NUMERIC` | NULL | Hauteur du produit en cm |
| `width_cm` | `NUMERIC` | NULL | Largeur du produit en cm |

## 4.3 Clé

`product_id` est utilisé directement comme clé primaire.

Cette dimension ne nécessite pas de surrogate key dans la première version du modèle.

## 4.4 Source

La majorité des attributs proviennent de `products`.

`category_english` provient de `product_category_name_translation`.

---

# 5. Table `dim_seller`

## 5.1 Grain

Une ligne représente **un vendeur**.

## 5.2 Structure

| Colonne | Type PostgreSQL | Contraintes | Description |
|---|---|---|---|
| `seller_id` | `VARCHAR(32)` | PK, NOT NULL | Identifiant du vendeur |
| `zip_code_prefix` | `INTEGER` | NULL | Préfixe du code postal |
| `city` | `TEXT` | NULL | Ville du vendeur |
| `state` | `VARCHAR(2)` | NULL | État du vendeur |

## 5.3 Clé

`seller_id` est utilisé directement comme clé primaire.

## 5.4 Source

Les attributs proviennent de `sellers`.

---

# 6. Table `dim_customer`

## 6.1 Grain

Une ligne représente **un client unique identifié par `customer_unique_id`**.

## 6.2 Structure

| Colonne | Type PostgreSQL | Contraintes | Description |
|---|---|---|---|
| `customer_key` | `BIGINT` | PK, NOT NULL | Surrogate key créée par le Data Warehouse |
| `customer_unique_id` | `VARCHAR(32)` | NOT NULL, UNIQUE | Business key du client |
| `customer_id` | `VARCHAR(32)` | NULL | Identifiant technique provenant de la source |
| `zip_code_prefix` | `INTEGER` | NULL | Préfixe du code postal |
| `city` | `TEXT` | NULL | Ville du client |
| `state` | `VARCHAR(2)` | NULL | État du client |

## 6.3 Clés

### Primary Key

`customer_key`

Cette clé est générée par le Data Warehouse et ne dépend pas directement de la source Olist.

### Business Key

`customer_unique_id`

Cette colonne doit être unique dans `dim_customer`.

### Source identifier

`customer_id` est conservé afin de maintenir la traçabilité avec les données sources.

## 6.4 Règle de transformation

La correspondance avec la fact table suit le chemin :

```text
orders.customer_id
        │
        ▼
customers.customer_unique_id
        │
        ▼
dim_customer.customer_unique_id
        │
        ▼
dim_customer.customer_key
        │
        ▼
fact_sales.customer_key
```

---

# 7. Table `fact_sales`

## 7.1 Grain

**Une ligne = un article vendu dans une commande.**

Le grain correspond à une ligne de `order_items`.

## 7.2 Structure

| Colonne | Type PostgreSQL | Contraintes | Description |
|---|---|---|---|
| `order_id` | `VARCHAR(32)` | PK, NOT NULL | Identifiant de la commande |
| `order_item_id` | `INTEGER` | PK, NOT NULL | Identifiant de la ligne dans la commande |
| `product_id` | `VARCHAR(32)` | FK, NOT NULL | Produit vendu |
| `seller_id` | `VARCHAR(32)` | FK, NOT NULL | Vendeur |
| `customer_key` | `BIGINT` | FK, NOT NULL | Client dans le Data Warehouse |
| `date_id` | `INTEGER` | FK, NOT NULL | Date de la vente |
| `price` | `NUMERIC(12,2)` | NOT NULL | Montant de la vente |

## 7.3 Primary Key

La clé primaire est composée de :

```text
(order_id, order_item_id)
```

Cette combinaison identifie une ligne de produit vendue dans une commande.

## 7.4 Foreign Keys

```text
fact_sales.product_id
    → dim_product.product_id

fact_sales.seller_id
    → dim_seller.seller_id

fact_sales.customer_key
    → dim_customer.customer_key

fact_sales.date_id
    → dim_date.date_id
```

## 7.5 Mesure

`price` représente le montant de la vente.

`freight_value` n'est pas intégré à cette première version de `fact_sales`.

---

# 8. Types de données et conventions

Les types proposés suivent les caractéristiques des données sources et les besoins analytiques du modèle.

### Identifiants

Les identifiants textuels provenant d'Olist sont conservés sous forme de `VARCHAR(32)`.

### Montants

Les montants monétaires sont stockés avec :

```text
NUMERIC(12,2)
```

afin d'éviter les problèmes de précision associés aux types flottants.

### Dates

Les dates calendaires sont stockées avec le type PostgreSQL :

```text
DATE
```

Les timestamps provenant de la source seront transformés en date lors de l'ETL.

### Valeurs numériques

Les mesures et attributs numériques utilisent `INTEGER`, `SMALLINT` ou `NUMERIC` selon leur nature.

---

# 9. Relations et intégrité référentielle

Le modèle doit respecter les relations suivantes :

```text
dim_date
    1
    │
    │
    N
fact_sales
    N
    │
    │
    1
dim_product
```

et de manière équivalente pour `dim_seller` et `dim_customer`.

Chaque ligne de `fact_sales` doit donc référencer :

- une date existante ;
- un produit existant ;
- un vendeur existant ;
- un client existant.

---

# 10. Règles de chargement

L'ordre logique de chargement sera :

```text
1. dim_date
2. dim_product
3. dim_seller
4. dim_customer
5. fact_sales
```

Les dimensions doivent être disponibles avant le chargement de `fact_sales`, car la fact table contient leurs clés étrangères.

Pour `dim_customer`, le chargement doit notamment permettre de résoudre `customer_unique_id` vers `customer_key` avant l'insertion dans `fact_sales`.

---

# 11. Points à vérifier avant implémentation

Avant de créer les tables dans Supabase, les points suivants devront être validés :

- les longueurs et types réels des identifiants ;
- les valeurs `NULL` présentes dans les colonnes ;
- l'unicité de `product_id` ;
- l'unicité de `seller_id` ;
- l'unicité de `customer_unique_id` après transformation ;
- la correspondance entre les clés étrangères de `fact_sales` et les dimensions ;
- la précision nécessaire pour `price` ;
- la couverture des dates nécessaires dans `dim_date`.

Ces vérifications seront réalisées pendant la phase d'implémentation et de chargement.

---

# 12. Prochaine étape

Le modèle physique est maintenant spécifié.

La prochaine étape consiste à préparer l'implémentation du Data Warehouse dans Supabase/PostgreSQL :

1. créer les tables ;
2. définir les contraintes ;
3. charger les dimensions ;
4. construire et charger `fact_sales` ;
5. effectuer les contrôles d'intégrité et de qualité.
