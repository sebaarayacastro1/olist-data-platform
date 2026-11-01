
from pathlib import Path
import csv
import os

import psycopg
from psycopg import sql
from dotenv import load_dotenv


# Définir les chemins du projet
PROJECT_ROOT = Path(__file__).resolve().parent.parent
ENV_PATH = PROJECT_ROOT / ".env"
OUTPUT_DIR = PROJECT_ROOT / "data" / "tableau"

SCHEMA_NAME = "dbt_dev_marts"

# Tables analytiques à exporter
TABLES = {
    "fact_sales": 112_650,
    "dim_product": 32_951,
    "dim_seller": 3_095,
    "dim_customer": 96_096,
    "dim_date": None,
}


def export_table(conn, table_name, expected_rows):
    output_path = OUTPUT_DIR / f"{table_name}.csv"

    # Préparer la requête SQL en toute sécurité
    query = sql.SQL("SELECT * FROM {}.{}").format(
        sql.Identifier(SCHEMA_NAME),
        sql.Identifier(table_name),
    )

    # Lire les données sans charger toute la table en mémoire
    with conn.cursor(name=f"export_{table_name}") as cur:
        cur.execute(query)

        columns = [column.name for column in cur.description]

        row_count = 0

        with output_path.open(
            "w", encoding="utf-8-sig", newline=""
        ) as file:
            writer = csv.writer(file)
            writer.writerow(columns)

            for row in cur:
                writer.writerow(row)
                row_count += 1

    # Vérifier le volume exporté
    if expected_rows is not None and row_count != expected_rows:
        output_path.unlink(missing_ok=True)
        raise ValueError(
            f"Volume incorrect pour {table_name} : {row_count}"
        )

    print(f"{table_name}: {row_count} lignes exportées")

    return row_count


def main():
    # Charger la configuration PostgreSQL
    load_dotenv(ENV_PATH)
    database_url = os.getenv("DATABASE_URL")

    if not database_url:
        raise ValueError("DATABASE_URL manquante dans .env")

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    # Connexion en lecture seule
    with psycopg.connect(database_url) as conn:
        conn.execute("SET TRANSACTION READ ONLY")

        for table_name, expected_rows in TABLES.items():
            export_table(conn, table_name, expected_rows)

    print("Export Tableau terminé avec succès.")


if __name__ == "__main__":
    main()
