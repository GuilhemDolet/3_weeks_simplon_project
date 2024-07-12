from sqlalchemy import Column, Integer, String, Float, Boolean, Date, ForeignKey
from sqlalchemy.orm import declarative_base, relationship
from dotenv import load_dotenv
import os

load_dotenv()
Base = declarative_base()
# Définir la connexion à la base de données

# url de la BDD
DATABASE_URL = os.getenv("DATABASE_URL") 

class FormationsSimplon(Base):
    __tablename__ = 'formationssimplon'
    id_formation_unique = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    formation_id = Column(Integer, nullable=True)
    formation_intitule = Column(String, nullable=True)
    formation_rncp = Column(String, nullable=True)
    formation_rs = Column(String, nullable=True)
    formation_reussite = Column(String, nullable=True)
    session_sous_intitule = Column(String, nullable=True)
    session_distanciel = Column(Boolean, nullable=True)
    session_alternance = Column(Boolean, nullable=True)
    session_date_limite = Column(Date, nullable=True)
    session_date_debut = Column(String, nullable=True)
    session_duree = Column(String, nullable=True)
    session_lieu = Column(String, nullable=True)
    session_region = Column(String, nullable=True)
    session_niveau = Column(String, nullable=True)
    
    


    