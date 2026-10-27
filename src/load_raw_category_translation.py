
from pathlib import Path
import csv
import os

import psycopg
from dotenv import load_dotenv


# Définir les chemins du projet
PROJECT_ROOT = Path(__file__).resolve().parent.parent
CSV_PATH = (
    PROJECT_ROOT
    / "data"
    / "raw"
    / "product_category_name_translation.csv"
)
ENV_PATH = PROJECT_ROOT / ".env"

# Définir les colonnes attendues
EXPECTED_COLUMNS = [
    "product_category_name",
    "product_category_name_english",
]

EXPECTED_ROW_COUNT = 71


def main():
    # Vérifier la présence du fichier CSV
    if not CSV_PATH.is_file():
        raise FileNotFoundError(
            f"Fichier introuvable : {CSV_PATH}"
        )

    # Charger les variables d'environnement
    load_dotenv(ENV_PATH)
    database_url = os.getenv("DATABASE_URL")

    if not database_url:
        raise ValueError(
            "DATABASE_URL est manquante dans .env"
        )

    # Lire et valider le fichier CSV
    with CSV_PATH.open(
        "r", encoding="utf-8-sig", newline=""
    ) as file:
        reader = csv.DictReader(file)

        if reader.fieldnames != EXPECTED_COLUMNS:
            raise ValueError(
                f"Colonnes inattendues : {reader.fieldnames}"
            )

        rows = list(reader)

    # Vérifier les catégories obligatoires
    category_names = [
        row["product_category_name"]
        for row in rows
    ]

    if any(not name for name in category_names):
        raise ValueError(
            "Certaines catégories sont vides"
        )

    # Vérifier l'unicité des catégories
    if len(category_names) != len(set(category_names)):
        raise ValueError(
            "Des catégories sont dupliquées"
        )

    # Vérifier le nombre de lignes attendu
    if len(rows) != EXPECTED_ROW_COUNT:
        raise ValueError(
            f"Nombre de lignes inattendu : {len(rows)}"
        )

    print(f"Lignes source : {len(rows)}")

    # Ouvrir une transaction PostgreSQL
    with psycopg.connect(database_url) as conn:
        with conn.cursor() as cur:

            # Empêcher deux chargements simultanés
            cur.execute(
                "LOCK TABLE "
                "raw.product_category_name_translation "
                "IN EXCLUSIVE MODE"
            )

            # Empêcher une nouvelle insertion
            cur.execute(
                "SELECT COUNT(*) FROM "
                "raw.product_category_name_translation"
            )
            existing_count = cur.fetchone()[0]

            if existing_count > 0:
                print(
                    f"Chargement annulé : "
                    f"{existing_count} lignes déjà présentes."
                )
                return

            # Charger les traductions avec COPY
            copy_sql = """
                COPY raw.product_category_name_translation (
                    product_category_name,
                    product_category_name_english
                )
                FROM STDIN
            """

            with cur.copy(copy_sql) as copy:
                for row in rows:
                    values = [
                        row[column] if row[column] != "" else None
                        for column in EXPECTED_COLUMNS
                    ]
                    copy.write_row(values)

            # Vérifier les lignes chargées
            cur.execute(
                "SELECT COUNT(*) FROM "
                "raw.product_category_name_translation"
            )
            loaded_count = cur.fetchone()[0]

            if loaded_count != len(rows):
                raise ValueError(
                    f"Nombre de lignes incorrect : {loaded_count}"
                )

            print(f"Lignes chargées : {loaded_count}")
            print("Chargement terminé avec succès.")


if __name__ == "__main__":
    main()
