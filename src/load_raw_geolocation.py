
from pathlib import Path
import csv
import os

import psycopg
from dotenv import load_dotenv


# Définir les chemins du projet
PROJECT_ROOT = Path(__file__).resolve().parent.parent
CSV_PATH = PROJECT_ROOT / "data" / "raw" / "olist_geolocation_dataset.csv"
ENV_PATH = PROJECT_ROOT / ".env"

# Définir les colonnes attendues
EXPECTED_COLUMNS = [
    "geolocation_zip_code_prefix",
    "geolocation_lat",
    "geolocation_lng",
    "geolocation_city",
    "geolocation_state",
]

EXPECTED_ROW_COUNT = 1_000_163


def main():
    # Vérifier la présence du fichier CSV
    if not CSV_PATH.is_file():
        raise FileNotFoundError(f"Fichier introuvable : {CSV_PATH}")

    # Charger les variables d'environnement
    load_dotenv(ENV_PATH)
    database_url = os.getenv("DATABASE_URL")

    if not database_url:
        raise ValueError("DATABASE_URL est manquante dans .env")

    # Ouvrir le fichier sans charger toutes les lignes en mémoire
    with CSV_PATH.open(
        "r", encoding="utf-8-sig", newline=""
    ) as file:
        reader = csv.DictReader(file)

        if reader.fieldnames != EXPECTED_COLUMNS:
            raise ValueError(
                f"Colonnes inattendues : {reader.fieldnames}"
            )

        # Ouvrir une transaction PostgreSQL
        with psycopg.connect(database_url) as conn:
            with conn.cursor() as cur:

                # Empêcher deux chargements simultanés
                cur.execute(
                    "LOCK TABLE raw.olist_geolocation "
                    "IN EXCLUSIVE MODE"
                )

                # Empêcher une nouvelle insertion si la table est remplie
                cur.execute(
                    "SELECT COUNT(*) FROM raw.olist_geolocation"
                )
                existing_count = cur.fetchone()[0]

                if existing_count > 0:
                    print(
                        f"Chargement annulé : "
                        f"{existing_count} lignes déjà présentes."
                    )
                    return

                # Charger les données progressivement avec COPY
                copy_sql = """
                    COPY raw.olist_geolocation (
                        geolocation_zip_code_prefix,
                        geolocation_lat,
                        geolocation_lng,
                        geolocation_city,
                        geolocation_state
                    )
                    FROM STDIN
                """

                row_count = 0

                with cur.copy(copy_sql) as copy:
                    for row in reader:
                        # Vérifier la structure de chaque ligne
                        if None in row or any(
                            row[column] is None
                            for column in EXPECTED_COLUMNS
                        ):
                            raise ValueError(
                                f"Ligne CSV invalide : {reader.line_num}"
                            )

                        values = [
                            row[column] if row[column] != "" else None
                            for column in EXPECTED_COLUMNS
                        ]

                        copy.write_row(values)
                        row_count += 1

                        if row_count % 100_000 == 0:
                            print(
                                f"Lignes traitées : {row_count}"
                            )

                print(f"Lignes source : {row_count}")

                # Vérifier le nombre attendu de lignes
                if row_count != EXPECTED_ROW_COUNT:
                    raise ValueError(
                        f"Nombre de lignes source inattendu : {row_count}"
                    )

                # Vérifier le nombre de lignes chargées
                cur.execute(
                    "SELECT COUNT(*) FROM raw.olist_geolocation"
                )
                loaded_count = cur.fetchone()[0]

                if loaded_count != row_count:
                    raise ValueError(
                        f"Nombre de lignes incorrect : {loaded_count}"
                    )

                print(f"Lignes chargées : {loaded_count}")
                print("Chargement terminé avec succès.")


if __name__ == "__main__":
    main()
