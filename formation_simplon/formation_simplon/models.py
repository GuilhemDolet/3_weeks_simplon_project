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
    __tablename__ = 'formations_simplon'
    id_formation = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    intitule_formation = Column(String, nullable=True)
    categorie = Column(String, nullable=True)
    voie_acces = Column(String, nullable=True)

class SessionsSimplon(Base):
    __tablename__ = 'sessions_simplon'
    id_session = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    agence = Column(String, nullable=True)
    distanciel = Column(Boolean, nullable=True)
    alternance = Column(Boolean, nullable=True)
    echelle_duree = Column(String, nullable=True)
    date_limite = Column(Date, nullable=True)
    date_debut = Column(String, nullable=True)
    date_fin = Column(String, nullable=True)
    id_formation = Column(Integer, foreign_key=True, nullable=False)
    region = Column(String, foreign_key=True, nullable=False)


#liaison formations_simplon et registres
class AssFormationsSimplonRegistres(Base):
    __tablename__ = 'ass_formations_simplon_registres'
    id_formation = Column(Integer, ForeignKey('formations_simplon.id_formation'), primary_key=True,  nullable=False)
    type_registre = Column(Integer, ForeignKey('registres.type_registre'), primary_key=True,  nullable=False)
    code_registre = Column(Integer, ForeignKey('registres.code_registre'), primary_key=True,  nullable=False)

class Registres(Base):
    __tablename__ = 'registres'
    type_registre = Column(Integer, primary_key=True, nullable=False)
    code_registre = Column(String, nullable=True)
    titre = Column(String, nullable=True)
    statut = Column(String, nullable=True)
    niveau_sortie = Column(String, nullable=True)
    url = Column(String, nullable=True)

class FormationsExt(Base):
    __tablename__ = 'formations_ext'
    id_formation = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    intitule_formation = Column(String, nullable=True)
    organisme = Column(String, nullable=True)

#liaison formations_ext et registres
class AssFormationsExtRegistres(Base):
    __tablename__ = 'ass_formations_ext_registres'
    id_formation = Column(Integer, ForeignKey('formations_ext.id_formation'), primary_key=True, nullable=False)
    type_registre = Column(Integer, ForeignKey('registres.type_registre'), primary_key=True,  nullable=False)
    code_registre = Column(Integer, ForeignKey('registres.code_registre'), primary_key=True,  nullable=False)

#liaison formations_ext et regions
class AssFormationsExtRegions (Base):
    __tablename__ = 'sessions_simplon'
    id_formation = Column(Integer, ForeignKey('formations_ext.id_formation'), primary_key=True, nullable=False)
    region = Column(Integer, ForeignKey('regions.region'), primary_key=True,  nullable=False)

class Regions(Base):
    tablename__ = 'regions'
    region = Column(String, primary_key=True, nullable=False)
    
#liaison registres et formacodes
class AssRegistresFormacodes(Base):
    __tablename__ = 'ass_registre_formacodes'
    formacode_code = Column(Integer, ForeignKey('formacode.code'), primary_key=True,  nullable=False)
    type_registre = Column(String, ForeignKey('registres.type_registre'), primary_key=True,  nullable=False)
    code_registre = Column(Integer, ForeignKey('registres.code_registre'), primary_key=True,  nullable=False)

class Formacodes(Base):
    __tablename__ = 'formacodes'
    formacode_code = Column(Integer, primary_key=True,  nullable=False)
    formacode_nom = Column(String,  nullable=True)

#liaison registres et nsf
class AssRegistresNsf(Base):
    __tablename__ = 'ass_registre_nsf'
    nsf_code = Column(Integer, ForeignKey('nsf.nsf_code'), primary_key=True,  nullable=False)
    formacode_code = Column(Integer, ForeignKey('formacodes.formacode_code'), primary_key=True,  nullable=False)

class Nsf(Base):
    __tablename__ = 'nsf'
    nsf_code = Column(Integer, primary_key=True, nullable=False)
    nsf_nom = Column(String, nullable=True)
