
from pathlib import Path
import csv

# Chemin du fichier seed
PROJECT_ROOT = Path(__file__).resolve().parent.parent
CSV_PATH = (
    PROJECT_ROOT
    / "dbt"
    / "olist_analytics"
    / "seeds"
    / "product_categories_fr.csv"
)

# Traductions françaises des catégories Olist
TRANSLATIONS = {
    "agro_industria_e_comercio": "Agro-industrie et commerce",
    "alimentos": "Alimentation",
    "alimentos_bebidas": "Alimentation et boissons",
    "artes": "Arts",
    "artes_e_artesanato": "Arts et artisanat",
    "artigos_de_festas": "Articles de fête",
    "artigos_de_natal": "Articles de Noël",
    "audio": "Audio",
    "automotivo": "Automobile",
    "bebes": "Bébés",
    "bebidas": "Boissons",
    "beleza_saude": "Beauté et santé",
    "brinquedos": "Jouets",
    "cama_mesa_banho": "Linge de maison",
    "casa_conforto": "Confort de la maison",
    "casa_conforto_2": "Confort de la maison 2",
    "casa_construcao": "Maison et construction",
    "cds_dvds_musicais": "CD et DVD musicaux",
    "cine_foto": "Cinéma et photographie",
    "climatizacao": "Climatisation",
    "consoles_games": "Consoles et jeux vidéo",
    "construcao_ferramentas_construcao": "Outils de construction",
    "construcao_ferramentas_ferramentas": "Outillage",
    "construcao_ferramentas_iluminacao": "Éclairage de construction",
    "construcao_ferramentas_jardim": "Outils de jardinage",
    "construcao_ferramentas_seguranca": "Équipements de sécurité",
    "cool_stuff": "Gadgets et objets originaux",
    "dvds_blu_ray": "DVD et Blu-ray",
    "eletrodomesticos": "Électroménager",
    "eletrodomesticos_2": "Électroménager 2",
    "eletronicos": "Électronique",
    "eletroportateis": "Petit électroménager",
    "esporte_lazer": "Sport et loisirs",
    "fashion_bolsas_e_acessorios": "Mode : sacs et accessoires",
    "fashion_calcados": "Mode : chaussures",
    "fashion_esporte": "Mode : sport",
    "fashion_roupa_feminina": "Mode : vêtements femme",
    "fashion_roupa_infanto_juvenil": "Mode : vêtements enfant",
    "fashion_roupa_masculina": "Mode : vêtements homme",
    "fashion_underwear_e_moda_praia": "Mode : sous-vêtements et plage",
    "ferramentas_jardim": "Outils de jardinage",
    "flores": "Fleurs",
    "fraldas_higiene": "Couches et hygiène",
    "industria_comercio_e_negocios": "Industrie, commerce et affaires",
    "informatica_acessorios": "Informatique et accessoires",
    "instrumentos_musicais": "Instruments de musique",
    "la_cuisine": "Cuisine",
    "livros_importados": "Livres importés",
    "livros_interesse_geral": "Livres généralistes",
    "livros_tecnicos": "Livres techniques",
    "malas_acessorios": "Bagages et accessoires",
    "market_place": "Marketplace",
    "moveis_colchao_e_estofado": "Matelas et meubles rembourrés",
    "moveis_cozinha_area_de_servico_jantar_e_jardim": "Meubles de cuisine, salle à manger et jardin",
    "moveis_decoracao": "Meubles et décoration",
    "moveis_escritorio": "Mobilier de bureau",
    "moveis_quarto": "Mobilier de chambre",
    "moveis_sala": "Mobilier de salon",
    "musica": "Musique",
    "papelaria": "Papeterie",
    "pc_gamer": "PC gamer",
    "pcs": "Ordinateurs",
    "perfumaria": "Parfumerie",
    "pet_shop": "Animalerie",
    "portateis_casa_forno_e_cafe": "Appareils domestiques : fours et café",
    "portateis_cozinha_e_preparadores_de_alimentos": "Appareils de cuisine portables et préparateurs alimentaires",
    "relogios_presentes": "Montres et cadeaux",
    "seguros_e_servicos": "Assurances et services",
    "sinalizacao_e_seguranca": "Signalisation et sécurité",
    "tablets_impressao_imagem": "Tablettes, impression et image",
    "telefonia": "Téléphonie",
    "telefonia_fixa": "Téléphonie fixe",
    "utilidades_domesticas": "Articles ménagers",
}


def main():
    # Lire les catégories du fichier seed
    with CSV_PATH.open(
        "r", encoding="utf-8-sig", newline=""
    ) as file:
        reader = csv.DictReader(file)
        rows = list(reader)

    # Vérifier que toutes les catégories possèdent une traduction
    categories = {
        row["category_name_pt"]
        for row in rows
    }

    missing = categories - TRANSLATIONS.keys()
    extra = TRANSLATIONS.keys() - categories

    if missing or extra:
        raise ValueError(
            f"Traductions manquantes : {sorted(missing)}\n"
            f"Traductions supplémentaires : {sorted(extra)}"
        )

    # Ajouter les traductions françaises
    for row in rows:
        row["category_name_fr"] = TRANSLATIONS[
            row["category_name_pt"]
        ]

    # Réécrire le fichier seed
    with CSV_PATH.open(
        "w", encoding="utf-8", newline=""
    ) as file:
        writer = csv.DictWriter(
            file,
            fieldnames=[
                "category_name_pt",
                "category_name_fr",
            ],
        )
        writer.writeheader()
        writer.writerows(rows)

    print(f"Catégories traduites : {len(rows)}")
    print("Toutes les traductions sont complètes.")


if __name__ == "__main__":
    main()
