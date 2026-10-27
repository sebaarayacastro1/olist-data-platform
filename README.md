# E-commerce Data Platform — Étape 1 : Cadrage du projet

## 1. Contexte

Ce projet a pour objectif de construire une plateforme de données permettant d'analyser les performances commerciales et opérationnelles d'une marketplace e-commerce.

Le projet s'appuie sur le dataset **Brazilian E-Commerce Public Dataset by Olist**, qui contient des informations relatives aux commandes, clients, produits, vendeurs, paiements, avis clients et livraisons.

L'objectif n'est pas uniquement de réaliser une analyse exploratoire, mais de mettre en place un **pipeline de données de bout en bout**, depuis l'ingestion des données jusqu'à leur exploitation dans un outil de Business Intelligence.

L'architecture cible sera basée principalement sur :

- **Python** pour l'ingestion et les transformations ;
- **Supabase / PostgreSQL** pour le stockage et le Data Warehouse ;
- **SQL** pour la modélisation et les transformations ;
- **Tableau** pour la visualisation et l'analyse ;
- **Git / GitHub** pour le versionnement ;
- **GitHub Actions** pour l'automatisation du pipeline.

---

## 2. Objectifs du projet

Les principaux objectifs sont les suivants :

1. Explorer et comprendre les données disponibles.
2. Identifier les problèmes de qualité des données.
3. Concevoir un modèle de données adapté à l'analyse décisionnelle.
4. Mettre en place un processus d'ingestion automatisé avec Python.
5. Transformer les données brutes en données analytiques.
6. Construire un Data Warehouse basé sur un modèle en étoile.
7. Mettre en place des contrôles de qualité des données.
8. Créer des tableaux de bord permettant de suivre les performances de l'activité.
9. Automatiser l'exécution du pipeline.
10. Documenter l'ensemble de la solution afin de garantir sa reproductibilité.

---

## 3. Problématique métier

Une marketplace e-commerce génère des données provenant de nombreuses sources : commandes, produits, clients, vendeurs, paiements, livraisons et avis.

Lorsque ces données sont stockées dans différentes tables ou fichiers, il peut être difficile d'obtenir une vision globale de l'activité.

Le projet cherche donc à répondre à la problématique suivante :

> **Comment construire une plateforme de données permettant de centraliser, transformer et exploiter les données d'une marketplace e-commerce afin de faciliter le suivi de ses performances commerciales, logistiques et de la satisfaction client ?**

---

## 4. Questions métier

Le projet devra permettre de répondre à plusieurs questions.

### Performance commerciale

- Quel est le chiffre d'affaires généré au cours du temps ?
- Comment évoluent les ventes mensuelles ?
- Quel est le panier moyen ?
- Combien de commandes sont réalisées ?
- Quelles sont les catégories de produits les plus performantes ?
- Quels sont les produits générant le plus de chiffre d'affaires ?
- Quels sont les vendeurs les plus performants ?

### Analyse géographique

- Quelles régions génèrent le plus de chiffre d'affaires ?
- Où sont situés les principaux clients ?
- Où sont situés les principaux vendeurs ?
- Existe-t-il des différences de performance selon les régions ?

### Logistique

- Quel est le délai moyen de livraison ?
- Quelle est la différence entre la date de livraison estimée et la date de livraison réelle ?
- Quelles régions ou catégories présentent les délais les plus importants ?
- Existe-t-il une relation entre le délai de livraison et la satisfaction client ?

### Satisfaction client

- Quelle est la note moyenne attribuée par les clients ?
- Comment évolue la satisfaction au cours du temps ?
- Quelles catégories de produits obtiennent les meilleures notes ?
- Les commandes livrées en retard obtiennent-elles des notes plus faibles ?

---

## 5. Périmètre

### Inclus dans le projet

Le projet couvrira principalement :

- les commandes ;
- les lignes de commande ;
- les produits ;
- les clients ;
- les vendeurs ;
- les paiements ;
- les avis clients ;
- les informations géographiques ;
- les dates et informations de livraison.

### Hors périmètre

Dans un premier temps, le projet ne cherchera pas à :

- développer un modèle de Machine Learning ;
- mettre en place une architecture Big Data ;
- traiter des données temps réel ;
- développer une application web métier ;
- reproduire une infrastructure cloud de production.

Ces éléments pourront éventuellement faire l'objet de projets ou d'évolutions ultérieurs.

---

## 6. Architecture cible

L'architecture générale envisagée est la suivante :

```text
                 Olist Dataset
                       │
                       ▼
              ┌─────────────────┐
              │ Python Ingestion│
              └────────┬────────┘
                       │
                       ▼
              ┌─────────────────┐
              │ Staging Layer   │
              │   PostgreSQL    │
              └────────┬────────┘
                       │
                       ▼
              ┌─────────────────┐
              │ Transformation  │
              │     Python      │
              │       + SQL     │
              └────────┬────────┘
                       │
                       ▼
              ┌─────────────────┐
              │  Data Warehouse │
              │   Star Schema   │
              └────────┬────────┘
                       │
                       ▼
              ┌─────────────────┐
              │     Tableau     │
              │       BI        │
              └─────────────────┘
```

L'objectif est de séparer les différentes étapes du traitement afin de faciliter la maintenance, les contrôles de qualité et l'évolution du pipeline.

---

## 7. Livrables

Le projet devra aboutir aux livrables suivants :

### Data Engineering

- Pipeline d'ingestion Python.
- Pipeline de transformation.
- Base de données PostgreSQL sur Supabase.
- Modèle dimensionnel.
- Scripts SQL de création et de transformation.
- Contrôles de qualité des données.

### Business Intelligence

- Tableau de bord de suivi des performances commerciales.
- Tableau de bord d'analyse des ventes.
- Tableau de bord dédié à la logistique et à la satisfaction client.

### Documentation

- Documentation de l'architecture.
- Data dictionary.
- Documentation du modèle de données.
- Documentation du pipeline.
- README permettant de reproduire le projet.

---

## 8. Critères de réussite

Le projet sera considéré comme fonctionnel lorsque :

- les données sources peuvent être ingérées automatiquement ;
- les transformations peuvent être exécutées de manière reproductible ;
- les données finales sont disponibles dans le Data Warehouse ;
- les principales règles de qualité sont contrôlées automatiquement ;
- les indicateurs métier peuvent être calculés à partir du modèle final ;
- Tableau peut exploiter directement les données du Data Warehouse ;
- l'ensemble du pipeline peut être exécuté sans intervention manuelle importante ;
- une nouvelle personne peut comprendre et reproduire le projet à partir de la documentation.

---

## 9. Stack technique

| Technologie | Utilisation |
|---|---|
| Python | Ingestion, transformation et contrôles |
| Pandas | Manipulation des données |
| PostgreSQL | Stockage et Data Warehouse |
| Supabase | Hébergement PostgreSQL |
| SQL | Modélisation et transformations |
| Tableau | Business Intelligence |
| Git / GitHub | Versionnement |
| GitHub Actions | Automatisation |

---

## 10. Prochaine étape

La prochaine étape du projet consiste à réaliser une **exploration approfondie des données sources** afin de comprendre :

- la structure de chaque dataset ;
- les relations entre les différentes tables ;
- les types de données ;
- les valeurs manquantes ;
- les doublons ;
- les incohérences potentielles ;
- les clés primaires et étrangères ;
- les contraintes nécessaires à la construction du Data Warehouse.

Cette analyse servira de base à la conception du modèle de données.