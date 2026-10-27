# Qualité des données — Olist Data Platform

## 1. Validation de la couche RAW

Les neuf fichiers CSV du dataset Olist ont été chargés dans le schéma `raw` de PostgreSQL (Supabase).

Les contrôles effectués comprennent :

- La vérification du nombre de lignes chargées.
- La vérification de l'unicité des clés primaires définies.
- La vérification des relations entre les principales tables.
- La protection contre les rechargements accidentels.
- La conservation des données sources, y compris les doublons de géolocalisation.

## 2. Catégories sans traduction anglaise

Lors du rapprochement entre `raw.olist_products` et `raw.product_category_name_translation`, deux catégories utilisées par les produits n'ont pas trouvé de correspondance :

| Catégorie originale | Traduction française proposée |
|---|---|
| `pc_gamer` | PC gamer |
| `portateis_cozinha_e_preparadores_de_alimentos` | Appareils de cuisine portables et préparateurs alimentaires |

Ces catégories sont conservées sans modification dans la couche `raw`.

## 3. Traitement prévu avec dbt

Les transformations permettront de :

- Préserver les catégories originales en portugais.
- Conserver les traductions anglaises disponibles.
- Ajouter des traductions françaises via un fichier de référence géré par dbt seed.
- Définir une valeur de remplacement lorsque la traduction anglaise est absente.
- Vérifier la couverture des traductions par des tests de qualité.

## 4. Règles de conservation

La couche `raw` conserve les données sources sans déduplication ni enrichissement métier.

Les opérations de nettoyage, de normalisation et d'enrichissement seront réalisées dans les modèles dbt.