
from pathlib import Path
import csv
import os

import psycopg
from dotenv import load_dotenv


# Définir les chemins du projet
PROJECT_ROOT = Path(__file__).resolve().parent.parent
CSV_PATH = PROJECT_ROOT / "data" / "raw" / "olist_orders_dataset.csv"
ENV_PATH = PROJECT_ROOT / ".env"

# Colonnes attendues dans le fichier CSV
EXPECTED_COLUMNS = [
    "order_id",
    "customer_id",
    "order_status",
    "order_purchase_timestamp",
    "order_approved_at",
    "order_delivered_carrier_date",
    "order_delivered_customer_date",
    "order_estimated_delivery_date",
]


def main():
    # Vérifier la présence du fichier CSV
    if not CSV_PATH.is_file():
        raise FileNotFoundError(f"Fichier introuvable : {CSV_PATH}")

    # Charger la configuration de connexion
    load_dotenv(ENV_PATH)
    database_url = os.getenv("DATABASE_URL")

    if not database_url:
        raise ValueError("DATABASE_URL est manquante dans .env")

    # Lire et valider le fichier source
    with CSV_PATH.open("r", encoding="utf-8-sig", newline="") as file:
        reader = csv.DictReader(file)

        if reader.fieldnames != EXPECTED_COLUMNS:
            raise ValueError(
                f"Colonnes inattendues : {reader.fieldnames}"
            )

        rows = list(reader)

    # Vérifier les identifiants de commande
    order_ids = [row["order_id"] for row in rows]

    if any(not order_id for order_id in order_ids):
        raise ValueError("Certains order_id sont vides")

    if len(order_ids) != len(set(order_ids)):
        raise ValueError("Des order_id sont dupliqués")

    print(f"Lignes source : {len(rows)}")

    # Ouvrir une transaction PostgreSQL
    with psycopg.connect(database_url) as conn:
        with conn.cursor() as cur:

            # Empêcher deux chargements simultanés
            cur.execute("LOCK TABLE raw.olist_orders IN EXCLUSIVE MODE")

            # Vérifier si la table contient déjà des données
            cur.execute("SELECT COUNT(*) FROM raw.olist_orders")
            existing_count = cur.fetchone()[0]

            if existing_count > 0:
                print(
                    f"Chargement annulé : "
                    f"{existing_count} lignes déjà présentes."
                )
                return

            # Charger les données avec PostgreSQL COPY
            copy_sql = """
                COPY raw.olist_orders (
                    order_id,
                    customer_id,
                    order_status,
                    order_purchase_timestamp,
                    order_approved_at,
                    order_delivered_carrier_date,
                    order_delivered_customer_date,
                    order_estimated_delivery_date
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
            cur.execute("SELECT COUNT(*) FROM raw.olist_orders")
            loaded_count = cur.fetchone()[0]

            if loaded_count != len(rows):
                raise ValueError(
                    f"Nombre de lignes incorrect : {loaded_count}"
                )

            print(f"Lignes chargées : {loaded_count}")
            print("Chargement terminé avec succès.")

    # La transaction est validée automatiquement ici


if __name__ == "__main__":
    main()
