
from pathlib import Path
import os
import sys
import subprocess
from urllib.parse import urlparse, unquote

from dotenv import load_dotenv


# Charger les variables d'environnement du projet
PROJECT_ROOT = Path(__file__).resolve().parent.parent
load_dotenv(PROJECT_ROOT / ".env")

database_url = os.getenv("DATABASE_URL")

if not database_url:
    raise ValueError("DATABASE_URL est manquante dans .env")

# Extraire les paramètres de connexion PostgreSQL
parsed_url = urlparse(database_url)

if parsed_url.scheme not in ("postgresql", "postgres"):
    raise ValueError("URL PostgreSQL invalide")

env = os.environ.copy()

env["DBT_HOST"] = parsed_url.hostname or ""
env["DBT_USER"] = unquote(parsed_url.username or "")
env["DBT_PASSWORD"] = unquote(parsed_url.password or "")
env["DBT_DBNAME"] = unquote(
    parsed_url.path.lstrip("/")
)

# Conserver le port fourni dans DATABASE_URL
env["DBT_PORT"] = str(parsed_url.port or 5432)

# Vérifier les paramètres obligatoires
required_vars = [
    "DBT_HOST",
    "DBT_USER",
    "DBT_PASSWORD",
    "DBT_DBNAME",
]

if any(not env[var] for var in required_vars):
    raise ValueError("Configuration PostgreSQL incomplète")

# Exécuter dbt sans afficher les identifiants
dbt_project = PROJECT_ROOT / "dbt" / "olist_analytics"

print("Configuration dbt chargée.")
print("Exécution de dbt debug...")

# Exécuter la commande dbt demandée
dbt_args = sys.argv[1:] or ["debug"]

print(f"Commande dbt : {' '.join(dbt_args)}")

subprocess.run(
    ["dbt", *dbt_args, "--project-dir", str(dbt_project)],
    env=env,
    cwd=dbt_project,
    check=True,
)