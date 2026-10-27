import os

import psycopg
from dotenv import load_dotenv

# Charger les variables d'environnement
load_dotenv()

database_url = os.getenv("DATABASE_URL")

if not database_url:
    raise ValueError("DATABASE_URL est absente du fichier .env")

# Tester la connexion à Supabase
try:
    with psycopg.connect(
        database_url,
        sslmode="require",
        connect_timeout=10
    ) as conn:
        print("Connexion à Supabase réussie !")

        # Vérifier les tables du Data Warehouse
        with conn.cursor() as cur:
            cur.execute("""
                SELECT table_name
                FROM information_schema.tables
                WHERE table_schema = 'public'
                  AND table_name IN (
                      'dim_date',
                      'dim_product',
                      'dim_seller',
                      'dim_customer',
                      'fact_sales'
                  )
                ORDER BY table_name;
            """)

            tables = cur.fetchall()

            print("\nTables trouvées :")
            for table in tables:
                print(f"- {table[0]}")

            if len(tables) != 5:
                print("\nAttention : certaines tables sont manquantes.")

except psycopg.Error as error:
    print(f"Erreur de connexion : {error}")