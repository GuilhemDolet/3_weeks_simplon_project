#une fois la DB créée sur Azure, lancer ce fichier une seule fois pour créer les tables
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from models import Base
import os

# Définir la connexion à la base de données
DATABASE_URL="postgresql+psycopg2://iratevenison3:qkDvlq24qQ1PUwqkuFNQRQ@pbo.postgres.database.azure.com:5432/flexibleserverdb"
print(DATABASE_URL)

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