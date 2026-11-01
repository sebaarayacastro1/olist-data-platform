# Star Schema

## 1. Objectif

Ce document définit le modèle dimensionnel initial du projet Olist.

L'objectif est de structurer les données de manière à faciliter l'analyse des ventes dans un outil de Business Intelligence tel que Tableau.

Le modèle est construit autour d'une **fact table principale des ventes** et de plusieurs dimensions permettant d'analyser ces ventes selon différents axes.

---

## 2. Fact table principale : `fact_sales`

### Grain

**1 ligne = 1 article vendu dans une commande.**

L'identification d'une ligne de vente repose sur le couple :

- `order_id`
- `order_item_id`

Ce choix correspond au grain observé dans `olist_order_items_dataset`.

### Mesure principale

`price`

Dans le cadre de ce projet, le chiffre d'affaires est défini à partir de `price` uniquement.

`freight_value` n'est pas inclus dans le chiffre d'affaires, car les frais de livraison peuvent correspondre à un coût ou à un service tiers et ne représentent pas nécessairement un revenu pour l'entreprise.

### Attributs et clés

| Colonne | Rôle | Source |
|---|---|---|
| `order_id` | Identifiant de la commande source | `orders.order_id` |
| `order_item_id` | Identifiant de la ligne de commande | `order_items.order_item_id` |
| `product_id` | Clé étrangère vers le produit | `order_items.product_id` |
| `seller_id` | Clé étrangère vers le vendeur | `order_items.seller_id` |
| `customer_key` | Clé étrangère vers le client du Data Warehouse | dérivée de `customer_unique_id` |
| `date_id` | Clé étrangère vers la date | dérivée de `orders.order_purchase_timestamp` |
| `price` | Montant de la vente | `order_items.price` |

---

## 3. Dimension `dim_date`

### Objectif

Permettre l'analyse des ventes dans le temps.

### Clé primaire

`date_id`

`date_id` est une clé numérique construite à partir de la date au format `YYYYMMDD`.

Exemple :

```text
20240115 → 15 janvier 2024
```

### Attributs

| Colonne | Description |
|---|---|
| `date_id` | Clé primaire numérique |
| `date` | Date complète |
| `month` | Mois |
| `quarter` | Trimestre |
| `year` | Année |

### Source

La date de vente est basée sur :

`orders.order_purchase_timestamp`

---

## 4. Dimension `dim_product`

### Objectif

Décrire les produits afin de permettre l'analyse des ventes par produit et par catégorie.

### Clé primaire

`product_id`

Dans cette dimension, l'identifiant source `product_id` est conservé comme clé primaire afin de garder une modélisation simple.

### Attributs

| Colonne | Source |
|---|---|
| `product_id` | `products.product_id` |
| `category` | `products.product_category_name` |
| `category_english` | `product_category_name_translation.product_category_name_english` |
| `name_length` | `products.product_name_lenght` |
| `description_length` | `products.product_description_lenght` |
| `photos_qty` | `products.product_photos_qty` |
| `weight_g` | `products.product_weight_g` |
| `length_cm` | `products.product_length_cm` |
| `height_cm` | `products.product_height_cm` |
| `width_cm` | `products.product_width_cm` |

Le prix n'est pas stocké dans cette dimension : il correspond à une mesure au niveau de la vente.

---

## 5. Dimension `dim_seller`

### Objectif

Permettre l'analyse de la performance des vendeurs.

### Clé primaire

`seller_id`

L'identifiant source `seller_id` est conservé comme clé primaire afin de garder une modélisation simple.

### Attributs

| Colonne | Source |
|---|---|
| `seller_id` | `sellers.seller_id` |
| `zip_code_prefix` | `sellers.seller_zip_code_prefix` |
| `city` | `sellers.seller_city` |
| `state` | `sellers.seller_state` |

---

## 6. Dimension `dim_customer`

### Objectif

Permettre l'analyse des ventes selon les clients.

### Clé primaire

`customer_key`

`customer_key` est une **surrogate key** créée par notre Data Warehouse. Elle est indépendante des identifiants techniques provenant de la source Olist.

### Business key

`customer_unique_id`

`customer_unique_id` est utilisé comme **business key** pour représenter le client de manière unique dans le modèle analytique.

### Attributs

| Colonne | Rôle | Source |
|---|---|---|
| `customer_key` | Clé primaire surrogate | générée par le Data Warehouse |
| `customer_unique_id` | Business key du client | `customers.customer_unique_id` |
| `customer_id` | Identifiant technique source | `customers.customer_id` |
| `zip_code_prefix` | Préfixe du code postal | `customers.customer_zip_code_prefix` |
| `city` | Ville du client | `customers.customer_city` |
| `state` | État du client | `customers.customer_state` |

### Relation avec `fact_sales`

La fact table ne référence pas directement `customer_id`.

Le chargement suivra conceptuellement le chemin :

```text
orders.customer_id
        │
        ▼
customers.customer_unique_id
        │
        ▼
dim_customer.customer_key
        │
        ▼
fact_sales.customer_key
```

Cette approche permet de séparer les identifiants de la source des clés utilisées dans notre Data Warehouse.

---

## 7. Relations

La fact table est reliée aux dimensions selon les clés suivantes :

| Fact | Dimension | Clé |
|---|---|---|
| `fact_sales.product_id` | `dim_product.product_id` | FK |
| `fact_sales.seller_id` | `dim_seller.seller_id` | FK |
| `fact_sales.customer_key` | `dim_customer.customer_key` | FK |
| `fact_sales.date_id` | `dim_date.date_id` | FK |

Le schéma conceptuel est le suivant :

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

## 8. Dimensions non intégrées à ce stade

### Géographie

Une dimension `dim_geography` n'est pas retenue dans la première version du modèle.

Les informations géographiques sont actuellement conservées dans `dim_customer` et `dim_seller`.

La table `geolocation` présente par ailleurs un grain nécessitant une transformation préalable et contient un nombre important de doublons exacts.

Son intégration pourra être réévaluée ultérieurement si elle apporte une valeur analytique suffisante.

### Paiements

`order_payments` n'est pas intégré à `fact_sales`.

La table possède un grain différent : une commande peut être associée à plusieurs paiements.

L'intégration des paiements fera l'objet d'une décision spécifique afin d'éviter la duplication des mesures de vente.

### Reviews

`order_reviews` n'est pas intégrée à `fact_sales`.

Les reviews possèdent également un grain différent de celui des lignes de commande.

Une éventuelle fact table dédiée pourra être envisagée si l'analyse de satisfaction est retenue dans le périmètre BI.

---

## 9. Questions métier couvertes

Le modèle doit permettre notamment d'analyser :

- l'évolution des ventes dans le temps ;
- la performance des produits ;
- la performance des catégories ;
- la performance des vendeurs ;
- la performance géographique via les informations client et vendeur ;
- les ventes par client.

---

## 10. Décisions de modélisation

Les décisions suivantes ont été prises à ce stade :

1. Le grain de `fact_sales` est une ligne de produit vendue dans une commande.
2. `order_id + order_item_id` identifie une ligne de vente.
3. `price` constitue la mesure principale du chiffre d'affaires.
4. `freight_value` n'est pas inclus dans le chiffre d'affaires.
5. `order_purchase_timestamp` définit la date de vente.
6. `dim_date` utilise une clé numérique `date_id` au format `YYYYMMDD`.
7. Le prix est conservé dans la fact table et non dans `dim_product`.
8. `dim_customer` utilise une surrogate key `customer_key` créée par le Data Warehouse.
9. `customer_unique_id` constitue la business key de `dim_customer`.
10. `customer_id` est conservé comme identifiant technique provenant de la source Olist.
11. `dim_product` utilise `product_id` comme clé primaire.
12. `dim_seller` utilise `seller_id` comme clé primaire.
13. `fact_sales` référence `dim_customer` via `customer_key`.
14. Les paiements et les reviews ne sont pas intégrés directement à `fact_sales`.
15. La géolocalisation détaillée n'est pas intégrée dans la première version du modèle.

---

## 11. Prochaine étape

Le modèle conceptuel est désormais défini.

La prochaine étape consiste à traduire ce modèle en un **modèle physique**, en précisant notamment les types de données, les contraintes et les règles de transformation nécessaires avant le chargement dans le Data Warehouse.
