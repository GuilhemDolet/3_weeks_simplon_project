#une fois la DB créée sur Azure, lancer ce fichier une seule fois pour créer les tables
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from models import Base
import os
from dotenv import load_dotenv

########################### automatisation avec le script_automatise et le .env

# Spécifiez le chemin vers votre fichier .env
env_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'scripts_azure', '.env')

# Chargez les variables d'environnement depuis le fichier .env
load_dotenv(dotenv_path=env_path)

# Maintenant, vous pouvez accéder aux variables d'environnement comme d'habitude
DATABASE_URL = os.getenv('DATABASE_URL')

########################### fin automatisation

# # Définir la connexion à la base de données
# DATABASE_URL="postgresql+psycopg2://iratevenison3:qkDvlq24qQ1PUwqkuFNQRQ@pbo.postgres.database.azure.com:5432/simplondb" # à décommenter si l'auto marche pas
print(DATABASE_URL)

# Créer une instance du moteur SQLAlchemy
engine = create_engine(DATABASE_URL)

# # Créer une factory de sessions SQLAlchemy (générateur de sessions)
# SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
# pas besoin pour le création des tables vides


# Exécuter la création des tables si ce script est exécuté directement
if __name__ == "__main__":
    Base.metadata.create_all(bind=engine)
    print("BDD créée")