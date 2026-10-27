# Data Dictionary

## Objectif

Ce document décrit la structure, le grain, les clés, les relations et les principales caractéristiques de qualité des données sources utilisées dans le projet Olist.

Il constitue la référence pour la conception du Data Warehouse et du modèle en étoile de l'étape 3.

> Les données sources restent dans `data/raw/` et ne sont pas versionnées dans Git.

---

## Sources

| Dataset | Lignes | Description | Rôle |
|---|---:|---|---|
| `olist_orders_dataset.csv` | 99 441 | Commandes | Transactionnel |
| `olist_order_items_dataset.csv` | 112 650 | Lignes de commande | Transactionnel |
| `olist_order_payments_dataset.csv` | 103 886 | Paiements | Transactionnel |
| `olist_order_reviews_dataset.csv` | 99 224 | Avis clients | Transactionnel |
| `olist_customers_dataset.csv` | 99 441 | Clients | Référentiel |
| `olist_products_dataset.csv` | 32 951 | Produits | Référentiel |
| `olist_sellers_dataset.csv` | 3 095 | Vendeurs | Référentiel |
| `olist_geolocation_dataset.csv` | 1 000 163 | Données géographiques | Référentiel |
| `product_category_name_translation.csv` | 71 | Traduction des catégories | Référentiel |

---

# 1. `olist_orders_dataset`

## Description

Table contenant les commandes et leur cycle de traitement.

## Grain

**1 ligne = 1 commande.**

## Clé primaire

`order_id`

## Clé étrangère

`customer_id` → `olist_customers_dataset.customer_id`

## Colonnes

| Colonne | Type | Description |
|---|---|---|
| `order_id` | string | Identifiant de la commande |
| `customer_id` | string | Identifiant du client associé à la commande |
| `order_status` | string | Statut de la commande |
| `order_purchase_timestamp` | datetime | Date et heure de création de la commande |
| `order_approved_at` | datetime | Date et heure d'approbation |
| `order_delivered_carrier_date` | datetime | Date de remise au transporteur |
| `order_delivered_customer_date` | datetime | Date de livraison au client |
| `order_estimated_delivery_date` | datetime | Date de livraison estimée |

## Qualité

Principales valeurs manquantes :

- `order_delivered_customer_date` : 2 965 valeurs manquantes (2,98 %)
- `order_delivered_carrier_date` : 1 783 valeurs manquantes (1,79 %)
- `order_approved_at` : 160 valeurs manquantes (0,16 %)

Ces valeurs ne doivent pas être remplacées automatiquement : elles peuvent correspondre à des commandes qui n'ont pas atteint certaines étapes du processus.

---

# 2. `olist_order_items_dataset`

## Description

Table détaillant les produits associés à chaque commande.

## Grain

**1 ligne = 1 article / ligne de commande.**

Une commande peut contenir plusieurs lignes de commande.

## Clé primaire

Le couple :

`order_id` + `order_item_id`

## Clés étrangères

- `order_id` → `olist_orders_dataset.order_id`
- `product_id` → `olist_products_dataset.product_id`
- `seller_id` → `olist_sellers_dataset.seller_id`

## Colonnes

| Colonne | Type | Description |
|---|---|---|
| `order_id` | string | Identifiant de la commande |
| `order_item_id` | integer | Numéro de la ligne dans la commande |
| `product_id` | string | Identifiant du produit |
| `seller_id` | string | Identifiant du vendeur |
| `shipping_limit_date` | datetime | Date limite d'expédition |
| `price` | numeric | Prix de l'article |
| `freight_value` | numeric | Frais de livraison |

## Cardinalité

- 112 650 lignes
- 98 666 commandes distinctes
- 32 951 produits distincts
- 3 095 vendeurs distincts

Certaines commandes contiennent plusieurs lignes de commande.

## Rôle dans le futur Data Warehouse

Cette table est une candidate naturelle pour constituer le grain principal de la future **fact table des ventes**.

---

# 3. `olist_order_payments_dataset`

## Description

Table contenant les informations relatives aux paiements des commandes.

## Grain

**1 ligne = 1 paiement associé à une commande.**

Une commande peut avoir plusieurs lignes de paiement.

## Clé étrangère

`order_id` → `olist_orders_dataset.order_id`

## Colonnes

| Colonne | Type | Description |
|---|---|---|
| `order_id` | string | Identifiant de la commande |
| `payment_sequential` | integer | Numéro séquentiel du paiement |
| `payment_type` | string | Type de paiement |
| `payment_installments` | integer | Nombre d'échéances |
| `payment_value` | numeric | Montant du paiement |

## Cardinalité

Une commande peut avoir plusieurs paiements, avec jusqu'à 29 enregistrements observés pour une même commande.

## Point d'attention

Cette table ne doit pas être jointe naïvement à `order_items` au niveau détaillé : une telle jointure pourrait multiplier les lignes et gonfler artificiellement les montants.

---

# 4. `olist_order_reviews_dataset`

## Description

Table contenant les avis associés aux commandes.

## Grain

**1 ligne = 1 avis.**

## Clé

`review_id` est l'identifiant de l'avis.

## Clé étrangère

`order_id` → `olist_orders_dataset.order_id`

## Colonnes principales

| Colonne | Type | Description |
|---|---|---|
| `review_id` | string | Identifiant de l'avis |
| `order_id` | string | Identifiant de la commande |
| `review_score` | integer | Score donné par le client |
| `review_comment_title` | string | Titre du commentaire |
| `review_comment_message` | string | Message du commentaire |
| `review_creation_date` | datetime | Date de création de l'avis |
| `review_answer_timestamp` | datetime | Date de réponse |

## Qualité

- `review_comment_title` : 87 656 valeurs manquantes (88,34 %)
- `review_comment_message` : 58 247 valeurs manquantes (58,70 %)

Ces valeurs manquantes sont cohérentes avec le caractère optionnel des commentaires.

## Point d'attention

Une commande peut être associée à plusieurs reviews dans les données. Le grain de cette table doit donc rester distinct du grain de `orders`.

---

# 5. `olist_customers_dataset`

## Description

Table contenant les informations géographiques associées aux clients.

## Grain

**1 ligne = 1 `customer_id`.**

## Clé primaire

`customer_id`

## Colonnes

| Colonne | Type | Description |
|---|---|---|
| `customer_id` | string | Identifiant d'un enregistrement client associé à une commande |
| `customer_unique_id` | string | Identifiant permettant d'identifier le client de manière plus persistante |
| `customer_zip_code_prefix` | integer | Préfixe du code postal |
| `customer_city` | string | Ville du client |
| `customer_state` | string | État du client |

## Cardinalité

- 99 441 `customer_id`
- 96 096 `customer_unique_id`
- 2 997 `customer_unique_id` sont associés à plusieurs `customer_id`

## Point d'attention

`customer_id` et `customer_unique_id` représentent deux niveaux d'identification différents.

Le choix de l'identifiant à utiliser dans la future dimension client devra être défini lors de l'étape de modélisation.

---

# 6. `olist_products_dataset`

## Description

Table contenant les caractéristiques des produits.

## Grain

**1 ligne = 1 produit.**

## Clé primaire

`product_id`

## Colonnes principales

| Colonne | Type | Description |
|---|---|---|
| `product_id` | string | Identifiant du produit |
| `product_category_name` | string | Catégorie du produit |
| `product_name_lenght` | numeric | Longueur du nom |
| `product_description_lenght` | numeric | Longueur de la description |
| `product_photos_qty` | numeric | Nombre de photos |
| `product_weight_g` | numeric | Poids en grammes |
| `product_length_cm` | numeric | Longueur |
| `product_height_cm` | numeric | Hauteur |
| `product_width_cm` | numeric | Largeur |

## Qualité

610 produits ne possèdent pas de catégorie.

Plusieurs attributs descriptifs et physiques présentent également des valeurs manquantes.

## Rôle

Candidate naturelle pour une future `dim_product`.

---

# 7. `olist_sellers_dataset`

## Description

Table contenant les informations relatives aux vendeurs.

## Grain

**1 ligne = 1 vendeur.**

## Clé primaire

`seller_id`

## Colonnes

| Colonne | Type | Description |
|---|---|---|
| `seller_id` | string | Identifiant du vendeur |
| `seller_zip_code_prefix` | integer | Préfixe du code postal |
| `seller_city` | string | Ville du vendeur |
| `seller_state` | string | État du vendeur |

## Cardinalité

- 3 095 vendeurs distincts

## Rôle

Candidate naturelle pour une future `dim_seller`.

---

# 8. `olist_geolocation_dataset`

## Description

Table contenant les informations géographiques associées aux préfixes de codes postaux.

## Grain

Le grain exact doit être précisé avant intégration au Data Warehouse : plusieurs lignes peuvent correspondre au même préfixe de code postal.

## Clé primaire

Aucune clé primaire simple n'a été retenue à ce stade.

## Colonnes

| Colonne | Type | Description |
|---|---|---|
| `geolocation_zip_code_prefix` | integer | Préfixe du code postal |
| `geolocation_lat` | numeric | Latitude |
| `geolocation_lng` | numeric | Longitude |
| `geolocation_city` | string | Ville |
| `geolocation_state` | string | État |

## Qualité

- 1 000 163 lignes
- 19 015 codes postaux distincts
- 261 831 doublons exacts

Cette table nécessitera une transformation avant intégration au modèle dimensionnel.

---

# 9. `product_category_name_translation`

## Description

Table de correspondance entre les noms de catégories en portugais et leur traduction en anglais.

## Grain

**1 ligne = 1 catégorie traduite.**

## Clé candidate

`product_category_name`

## Colonnes

| Colonne | Type | Description |
|---|---|---|
| `product_category_name` | string | Nom de la catégorie dans la langue source |
| `product_category_name_english` | string | Nom traduit en anglais |

## Cardinalité

71 catégories traduites.

## Rôle

Table de référence permettant d'enrichir les informations de catégorie des produits.

---

# Relations principales

Les relations vérifiées lors de l'exploration ne présentent pas d'enregistrements orphelins pour les clés testées.

```text
customers
    │
    │ customer_id
    ▼
orders
    │
    ├───────────────┐
    │               │
    ▼               ▼
order_items    order_payments
    │
    ├── product_id ──► products
    │
    └── seller_id ───► sellers

orders
    │
    └── order_id ───► order_reviews
```

## Cardinalités principales

| Relation | Cardinalité |
|---|---|
| Customer → Orders | 1:N |
| Order → Order Items | 1:N |
| Order → Payments | 1:N |
| Order → Reviews | 1:N dans les données |
| Product → Order Items | 1:N |
| Seller → Order Items | 1:N |

---

# Principaux points de qualité identifiés

| Problème | Impact potentiel | Traitement à définir |
|---|---|---|
| Dates de livraison manquantes | Certaines commandes ne sont pas livrées ou ne possèdent pas l'information | Ne pas imputer automatiquement |
| Commentaires de reviews manquants | Forte proportion de NULL | Conserver les NULL / traiter comme attribut optionnel |
| Produits sans catégorie | 610 produits | Catégorie `Unknown` ou traitement spécifique |
| Doublons géographiques | 261 831 doublons exacts | Déduplication / agrégation |
| `customer_id` vs `customer_unique_id` | Deux niveaux d'identification client | Décision de modélisation |
| Plusieurs paiements par commande | Risque de duplication des mesures | Fact table séparée ou agrégation |
| Plusieurs reviews par commande | Risque de duplication des mesures | Fact table séparée ou agrégation |
| Livraison après date estimée | 7 827 commandes | KPI potentiel de retard |
| Dates temporellement incohérentes | 166 cas détectés pour la livraison transporteur avant achat | Investigation / règle de qualité |

---

# Décisions à prendre à l'étape 3

Les éléments suivants restent volontairement ouverts et seront définis lors de la conception du Star Schema :

1. Grain exact de chaque future fact table.
2. Utilisation de `customer_id` ou `customer_unique_id` dans `dim_customer`.
3. Traitement de la géolocalisation.
4. Stratégie de gestion des produits sans catégorie.
5. Modélisation des paiements.
6. Modélisation des reviews.
7. Dimensions partagées entre les différentes fact tables.
8. Mesures et KPI destinés à Tableau.

---

# Prochaine étape

**Étape 3 — Data Modeling & Star Schema**

À partir de ce dictionnaire, le modèle dimensionnel sera conçu en fonction des besoins BI et des KPI à produire.
