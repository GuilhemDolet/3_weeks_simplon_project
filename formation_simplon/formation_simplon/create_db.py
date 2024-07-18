#une fois la DB créée sur Azure, lancer ce fichier une seule fois pour créer les tables
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import declarative_base, relationship
from sqlalchemy import create_engine
from models import Base
import os
import sqlite3

# Définir la connexion à la base de données
DATABASE_URL2=os.environ.get('DATABASE_URL3')
print(DATABASE_URL2)


# Créer une instance du moteur SQLAlchemy
engine = create_engine(DATABASE_URL2)

# Créer une factory de sessions SQLAlchemy (générateur de sessions)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Fonction pour créer toutes les tables dans la base de données
def create_database():
    Base.metadata.create_all(bind=engine)
    print("Base de données créée avec succès.")

# Exécuter la création des tables si ce script est exécuté directement
if __name__ == "__main__":
    create_database()