# installer l'environnement virtuel Poetry
poetry install

# créer la bdd sur Azure
cd scripts_azure/
. script_azure_bdd.sh 

cd .. #remonter dans le dossier parent 

cd formation_simplon/formation_simplon/mon_compte_formation
poetry run python requete_api.py #exécution de la requête api pour récupérer les données de mon compte formation dans un csv
cd .. #remonter dans le dossier parent cad formation_simplon/formation_simplon
poetry run python create_db.py # créer les tables dans Azure
poetry run python import_bdd.py #import des données csv de la requête api dans la BDD Azure


######## instructions dev pour la suite :
# - noter l'adresse de BDD affichée dans la console (normalement elle se charge dans le .env du dossier scripts_azure)
# - adresse BDD : récupérable dans le .env une fois le script azure exécuté
# - l'adresse est à renseigner dans create_db.py, ainsi que dans pipelines.py (class Database) et dans models.py
# lignes à ajouter dans ces fichiers : 
# import os
# from dotenv import load_dotenv
# ########################### automatisation avec le script_automatise et le .env
# # Spécifiez le chemin vers votre fichier .env
# env_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'scripts_azure', '.env')
# # Chargez les variables d'environnement depuis le fichier .env
# load_dotenv(dotenv_path=env_path)
# # Maintenant, vous pouvez accéder aux variables d'environnement comme d'habitude
# DATABASE_URL = os.getenv('DATABASE_URL') #si demandé dans ledit fichier
# engine = create_engine(DATABASE_URL) #si demandé dans ledit fichier
# ########################### fin automatisation


# exécuter le scraper et remplir la BDD en ligne grâce au scraper
poetry run scrapy crawl simplon_spider 


# lancer l'API pour consulter les données
poetry run uvicorn api_main:app --reload