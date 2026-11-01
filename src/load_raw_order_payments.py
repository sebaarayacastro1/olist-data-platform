
from pathlib import Path
import csv
import os

import psycopg
from dotenv import load_dotenv


# Définir les chemins du projet
PROJECT_ROOT = Path(__file__).resolve().parent.parent
CSV_PATH = PROJECT_ROOT / "data" / "raw" / "olist_order_payments_dataset.csv"
ENV_PATH = PROJECT_ROOT / ".env"

# Définir les colonnes attendues
EXPECTED_COLUMNS = [
    "order_id",
    "payment_sequential",
    "payment_type",
    "payment_installments",
    "payment_value",
]


def main():
    # Vérifier la présence du fichier CSV
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

    # Vérifier l'unicité de la clé primaire composée
    payment_keys = [
        (row["order_id"], row["payment_sequential"])
        for row in rows
    ]

    if any(not order_id or not payment_seq
           for order_id, payment_seq in payment_keys):
        raise ValueError("Certaines clés primaires sont vides")

    if len(payment_keys) != len(set(payment_keys)):
        raise ValueError("Des clés primaires sont dupliquées")

    print(f"Lignes source : {len(rows)}")

    # Ouvrir une transaction PostgreSQL
    with psycopg.connect(database_url) as conn:
        with conn.cursor() as cur:

            # Empêcher les chargements simultanés
            cur.execute(
                "LOCK TABLE raw.olist_order_payments IN EXCLUSIVE MODE"
            )

            # Éviter de recharger une table non vide
            cur.execute(
                "SELECT COUNT(*) FROM raw.olist_order_payments"
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
                COPY raw.olist_order_payments (
                    order_id,
                    payment_sequential,
                    payment_type,
                    payment_installments,
                    payment_value
                )
                FROM STDIN
            """

            with cur.copy(copy_sql) as copy:
                for row in rows:
                    values = [
                        row[column] or None
                        for column in EXPECTED_COLUMNS
                    ]
                    copy.write_row(values)

            # Vérifier le nombre de lignes chargées
            cur.execute(
                "SELECT COUNT(*) FROM raw.olist_order_payments"
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
