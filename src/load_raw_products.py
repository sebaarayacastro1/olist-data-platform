
from pathlib import Path
import csv
import os

import psycopg
from dotenv import load_dotenv


# Définir les chemins du projet
PROJECT_ROOT = Path(__file__).resolve().parent.parent
CSV_PATH = PROJECT_ROOT / "data" / "raw" / "olist_products_dataset.csv"
ENV_PATH = PROJECT_ROOT / ".env"

# Colonnes attendues dans le fichier CSV
EXPECTED_COLUMNS = [
    "product_id",
    "product_category_name",
    "product_name_lenght",
    "product_description_lenght",
    "product_photos_qty",
    "product_weight_g",
    "product_length_cm",
    "product_height_cm",
    "product_width_cm",
]


def main():
    # Vérifier que le fichier CSV existe
    if not CSV_PATH.is_file():
        raise FileNotFoundError(f"Fichier introuvable : {CSV_PATH}")

    # Charger les variables d'environnement
    load_dotenv(ENV_PATH)
    database_url = os.getenv("DATABASE_URL")

    if not database_url:
        raise ValueError("DATABASE_URL est manquante dans .env")

    # Lire et valider le fichier CSV
    with CSV_PATH.open("r", encoding="utf-8-sig", newline="") as file:
        reader = csv.DictReader(file)

        if reader.fieldnames != EXPECTED_COLUMNS:
            raise ValueError(
                f"Colonnes inattendues : {reader.fieldnames}"
            )

        rows = list(reader)

    # Vérifier l'unicité des identifiants de produits
    product_ids = [row["product_id"] for row in rows]

    if any(not product_id for product_id in product_ids):
        raise ValueError("Certains product_id sont vides")

    if len(product_ids) != len(set(product_ids)):
        raise ValueError("Des product_id sont dupliqués")

    print(f"Lignes source : {len(rows)}")

    # Ouvrir une transaction PostgreSQL
    with psycopg.connect(database_url) as conn:
        with conn.cursor() as cur:

            # Empêcher deux chargements simultanés
            cur.execute(
                "LOCK TABLE raw.olist_products IN EXCLUSIVE MODE"
            )

            # Empêcher une nouvelle insertion si la table contient des données
            cur.execute(
                "SELECT COUNT(*) FROM raw.olist_products"
            )
            existing_count = cur.fetchone()[0]

            if existing_count > 0:
                print(
                    f"Chargement annulé : "
                    f"{existing_count} lignes déjà présentes."
                )
                return

            # Charger les données avec PostgreSQL COPY
            copy_sql = """
                COPY raw.olist_products (
                    product_id,
                    product_category_name,
                    product_name_lenght,
                    product_description_lenght,
                    product_photos_qty,
                    product_weight_g,
                    product_length_cm,
                    product_height_cm,
                    product_width_cm
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

            # Vérifier le nombre de lignes chargées
            cur.execute(
                "SELECT COUNT(*) FROM raw.olist_products"
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
