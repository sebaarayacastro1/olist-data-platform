# Définition des indicateurs métier — Olist Data Platform

## 1. Périmètre analytique

Les indicateurs sont calculés à partir de `dbt_dev_marts.fact_sales` et des dimensions associées.

La table de faits contient une ligne par article de commande. Elle conserve les articles indépendamment du statut de livraison.

Les frais de livraison ne sont pas inclus dans le montant principal des ventes.

## 2. Indicateurs principaux

| Indicateur | Définition | Calcul SQL |
|---|---|---|
| Montant brut des articles | Somme des prix des articles | `SUM(price)` |
| Nombre d'articles | Nombre de lignes de vente | `COUNT(*)` |
| Nombre de commandes | Nombre de commandes distinctes ayant au moins un article | `COUNT(DISTINCT order_id)` |
| Prix moyen par article | Prix moyen d'une ligne de commande | `AVG(price)` |
| Panier moyen par commande | Montant brut des articles divisé par le nombre de commandes distinctes | `SUM(price) / COUNT(DISTINCT order_id)` |

## 3. Dimensions d'analyse

Les indicateurs peuvent être analysés selon :

- La date d'achat : jour, mois, trimestre et année.
- La catégorie de produit en français.
- Le produit.
- Le vendeur et sa localisation.
- Le client réel et sa localisation représentative.

## 4. Précautions d'interprétation

**Montant brut des articles :** il ne correspond pas nécessairement au chiffre d'affaires comptable. Les commandes annulées ou non livrées peuvent être incluses.

**Nombre de commandes :** il représente les commandes présentes dans `fact_sales`, et pas obligatoirement toutes les lignes de `raw.olist_orders`.

**Nombre d'articles :** il correspond au nombre de lignes de commande, et non à une quantité physique indépendante.

**Panier moyen :** il est calculé sur les commandes ayant des articles dans la table de faits.

**Localisation des clients :** elle correspond à la dernière localisation observée dans le dataset, et non nécessairement à leur adresse actuelle.

## 5. Contrôles effectués

- Réconciliation des identifiants d'articles entre RAW et MARTS.
- Concordance des prix au niveau de chaque article.
- Concordance du montant global.
- Cohérence entre les montants mensuels et le montant global.
- Vérification des relations avec les dimensions.

## 6. Utilisation dans Tableau

Le tableau de bord utilisera des libellés français et affichera clairement le périmètre des indicateurs afin d'éviter toute ambiguïté sur la notion de ventes.