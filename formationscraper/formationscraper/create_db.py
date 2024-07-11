from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base
from dotenv import load_dotenv
import os

load_dotenv()
# Définir la connexion à la base de données
DATABASE_URL = os.getenv("DATABASE_URL") 

# Créer une instance du moteur SQLAlchemy
engine = create_engine(DATABASE_URL)

# Créer une factory de sessions SQLAlchemy (générateur de sessions)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Fonction pour créer toutes les tables dans la base de données
def create_database():
    Base.metadata.create_all(bind=engine)
    print("Base de données créée avec succès.")

# Exécuter la création des tables si ce script est exécuté directement
if __name__ == "__main__":
    create_database()