# Architecture dbt — Olist Data Platform

## 1. Objectif

Transformer les données brutes du dataset Olist en un modèle dimensionnel destiné à l'analyse des ventes et à la visualisation avec Tableau.

La plateforme repose sur PostgreSQL (Supabase), Python et dbt Core avec l'adaptateur PostgreSQL.

## 2. Architecture ELT

Le pipeline suit trois couches principales :

**RAW → STAGING → MARTS**

### Couche RAW

Neuf tables PostgreSQL contiennent les données provenant des fichiers CSV Olist.

Les données sont chargées via des scripts Python avec `psycopg` et PostgreSQL `COPY`.

Les données sources sont conservées, notamment les doublons de géolocalisation et les catégories sans traduction anglaise.

### Couche STAGING

Neuf modèles dbt, matérialisés sous forme de vues dans `dbt_dev_staging`, préparent les données pour les analyses.

Les transformations comprennent principalement :

- Le renommage et la normalisation des colonnes.
- La conservation des identifiants métier.
- La préservation du grain de chaque table.
- La conservation des valeurs manquantes lorsque leur remplacement n'est pas justifié.
- La documentation et les tests de qualité.

### Données de référence

Un seed dbt, `product_categories_fr`, contient 73 correspondances de catégories portugaises vers le français.

Il est chargé dans `dbt_dev_reference`.

Les traductions françaises sont des correspondances définies pour le projet et ne constituent pas une traduction officielle d'Olist.

### Couche MARTS

Cinq modèles dbt, matérialisés en tables dans `dbt_dev_marts`, constituent le modèle dimensionnel :

| Modèle | Grain |
|---|---|
| `dim_product` | Un produit par ligne |
| `dim_seller` | Un vendeur par ligne |
| `dim_customer` | Un client réel par ligne |
| `dim_date` | Une date calendaire par ligne |
| `fact_sales` | Un article de commande par ligne |

Les tables analytiques historiques du schéma `public` ne sont pas modifiées par les modèles de développement.

## 3. Règles de modélisation

### Dimension client

La dimension utilise `customer_unique_id` pour identifier le client réel.

Une localisation représentative est sélectionnée à partir de la commande la plus récente observée, avec des critères de départage déterministes.

La clé `customer_key` est produite par `ROW_NUMBER()`. Sa stabilité n'est pas garantie si de nouveaux identifiants clients sont ajoutés lors de reconstructions futures.

### Dimension produit

Les catégories sont disponibles en portugais, en anglais et en français.

Les traductions anglaises absentes restent nulles. Les catégories sans traduction française ne sont pas inventées.

### Dimension date

Le calendrier couvre l'intervalle entre la première et la dernière date d'achat observée.

La clé `date_id` suit le format numérique YYYYMMDD.

### Table de faits

Le grain de `fact_sales` correspond à la clé composée `(order_id, order_item_id)`.

La mesure principale `price` exclut les frais de livraison.

Le modèle conserve les articles indépendamment du statut des commandes. Il ne représente donc pas uniquement les ventes livrées ni le chiffre d'affaires net.

## 4. Qualité des données

Les tests dbt vérifient notamment :

- L'unicité des identifiants nécessaires.
- L'absence de valeurs nulles dans les champs obligatoires.
- L'intégrité des relations entre les modèles.
- Les valeurs autorisées pour les notes des avis.
- L'unicité du grain de la table de faits.
- La conservation des articles entre RAW et MARTS.
- La concordance des prix et du montant total.

Les contrôles de réconciliation ont été validés sans écarts observés.

## 5. Limites et évolutions

- La dimension client utilise une clé technique adaptée à ce dataset statique, mais pas encore à des chargements incrémentaux.
- Les tables MARTS sont actuellement créées dans un schéma de développement.
- Les catégories sans traduction anglaise sont conservées.
- Les métriques de ventes doivent être interprétées selon leur définition, sans les assimiler automatiquement au chiffre d'affaires comptable.
- La stratégie de publication des modèles analytiques vers un environnement de consommation reste à définir.

## 6. Prochaine phase

Connecter Tableau aux modèles dimensionnels validés et créer un tableau de bord analytique en français.