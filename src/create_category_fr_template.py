
from pathlib import Path
import csv

# Définir les chemins du projet
PROJECT_ROOT = Path(__file__).resolve().parent.parent

SOURCE_PATH = (
    PROJECT_ROOT
    / "data"
    / "raw"
    / "product_category_name_translation.csv"
)

OUTPUT_PATH = (
    PROJECT_ROOT
    / "dbt"
    / "olist_analytics"
    / "seeds"
    / "product_categories_fr.csv"
)

# Ajouter les catégories absentes des traductions anglaises
MISSING_CATEGORIES = [
    "pc_gamer",
    "portateis_cozinha_e_preparadores_de_alimentos",
]


def main():
    # Lire les catégories originales
    with SOURCE_PATH.open(
        "r", encoding="utf-8-sig", newline=""
    ) as file:
        reader = csv.DictReader(file)

        categories = {
            row["product_category_name"]
            for row in reader
            if row["product_category_name"]
        }

    # Compléter avec les catégories manquantes
    categories.update(MISSING_CATEGORIES)

    # Préparer le répertoire des seeds
    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)

    # Ne pas écraser un fichier déjà préparé
    if OUTPUT_PATH.exists():
        raise FileExistsError(
            f"Le fichier existe déjà : {OUTPUT_PATH}"
        )

    # Générer le modèle de traduction
    with OUTPUT_PATH.open(
        "w", encoding="utf-8", newline=""
    ) as file:
        writer = csv.writer(file)

        writer.writerow([
            "category_name_pt",
            "category_name_fr",
        ])

        for category in sorted(categories):
            writer.writerow([category, ""])

    print(f"Catégories préparées : {len(categories)}")
    print(f"Fichier créé : {OUTPUT_PATH}")


if __name__ == "__main__":
    main()
