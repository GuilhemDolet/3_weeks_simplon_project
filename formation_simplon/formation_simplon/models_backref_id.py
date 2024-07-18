# exemple avec la doc officielle : 
# from sqlalchemy import Column, ForeignKey, Integer, String
# from sqlalchemy.orm import DeclarativeBase, relationship


# class Base(DeclarativeBase):
#     pass


# class User(Base):
#     __tablename__ = "user"
#     id = mapped_column(Integer, primary_key=True)
#     name = mapped_column(String)

#     addresses = relationship("Address", backref="user")


# class Address(Base):
#     __tablename__ = "address"
#     id = mapped_column(Integer, primary_key=True)
#     email = mapped_column(String)
#     user_id = mapped_column(Integer, ForeignKey("user.id"))

# peut etre juste donner un nom de variable-relation qui soit unique ? on dirait que c'est le seul truc qui change
# https://docs.sqlalchemy.org/en/20/orm/declarative_tables.html


from sqlalchemy import Column, Integer, String, Boolean, Date, ForeignKey
from sqlalchemy.orm import declarative_base, relationship
# from dotenv import load_dotenv
import os

# url de la BDD
DATABASE_URL2=os.environ.get("DATABASE_URL3")

Base = declarative_base()

# load_dotenv()
# Définir la connexion à la base de données

class Registres(Base):
    __tablename__ ='registres'
    id_registre = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    type_registre = Column(String, nullable=True)
    code_registre = Column(Integer, nullable=True)
    titre = Column(String, nullable=True)
    statut = Column(String, nullable=True)
    niveau_sortie = Column(String, nullable=True)
    url = Column(String, nullable=True)

    # Définir une clé primaire composite
    # __table_args__ = (PrimaryKeyConstraint('type_registre', 'code_registre'),)

    # Relation avec Registres
    reg_form_simpl = relationship("AssFormationsSimplonRegistres", backref="registres")
    reg_nsf = relationship("AssNsfRegistres", backref="registres")
    reg_formacodes = relationship("AssRegistresFormacodes", backref="registres")
    reg_form_ext = relationship("AssFormationsExtRegistres", backref="registres")

#liaison formations_ext et registres
class AssFormationsExtRegistres(Base):
    __tablename__ = 'ass_formations_ext_registres'
    id_formation_ext = Column(Integer, ForeignKey('formations_ext.id_formation_ext'), primary_key=True, nullable=False)
    id_registre = Column(Integer, ForeignKey('registres.id_registre'), primary_key=True, nullable=False)

    # type_registre = Column(String, ForeignKey('registres.type_registre'), primary_key=True, nullable=False)
    # code_registre = Column(Integer, ForeignKey('registres.code_registre'), primary_key=True, nullable=False)

    # Relation avec FormationsExt
    formation_ext = relationship("FormationsExt", backref="ass_formations_ext_registres")

    # # Définir une clé primaire composite
    # __table_args__ = (PrimaryKeyConstraint('id_formation_ext', 'type_registre', 'code_registre'),)


    #liaison registres et nsf
class AssRegistresNsf(Base):
    __tablename__ = 'ass_registres_nsf'
    # type_registre = Column(String, ForeignKey('registres.type_registre'), primary_key=True, nullable=False)
    # code_registre = Column(Integer, ForeignKey('registres.code_registre'), primary_key=True, nullable=False)
    id_registre = Column(Integer, ForeignKey('registres.id_registre'), primary_key=True, nullable=False)
    nsf_code = Column(Integer, ForeignKey('nsf.nsf_code'), primary_key=True, nullable=False)

    # __table_args__ = (PrimaryKeyConstraint('type_registre', 'code_registre', 'formacode_code'),)

    # Relation avec nsf
    nsf = relationship("Nsf", backref="ass_registres_nsf")

    #liaison registres et formacodes
class AssRegistresFormacodes(Base):
    __tablename__ = 'ass_registres_formacodes'
    formacode_code = Column(Integer, ForeignKey('formacodes.formacode_code'), primary_key=True, nullable=False)
    id_registre = Column(Integer, ForeignKey('registres.id_registre'), primary_key=True, nullable=False)
    # type_registre = Column(String, ForeignKey('registres.type_registre'), primary_key=True, nullable=False)
    # code_registre = Column(Integer, ForeignKey('registres.code_registre'), primary_key=True, nullable=False)
    
    # __table_args__ = (PrimaryKeyConstraint('formacode_code', 'type_registre', 'code_registre'),)

    # Relation avec Formacodes
    formacodes = relationship("Formacodes", backref="ass_registres_formacodes")


    #liaison formations_simplon et registres
class AssFormationsSimplonRegistres(Base):
    __tablename__ = 'ass_formations_simplon_registres'
    id_ass_formations_simplon_registres = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    id_formation = Column(Integer, ForeignKey('formations_simplon.id_formation'))
    id_registre = Column(Integer, ForeignKey('registres.id_registre'))

    # type_registre = Column(String, ForeignKey('registres.type_registre'))
    # code_registre = Column(Integer, ForeignKey('registres.code_registre'))

    # Relation avec FormationsSimplon
    formation_simplon = relationship("FormationsSimplon", backref="ass_formations_simplon_registres")

    # # Définir la clé primaire composite
    # __table_args__ = (PrimaryKeyConstraint('id_formation', 'type_registre', 'code_registre'),)


class FormationsSimplon(Base):
    __tablename__ = 'formations_simplon'
    id_formation = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    intitule_formation = Column(String, nullable=True)
    categorie = Column(String, nullable=True)
    voie_acces = Column(String, nullable=True)

    # Relation avec SessionsSimplon
    sessions = relationship("SessionsSimplon", backref="formations_simplon")


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
    id_formation = Column(Integer, ForeignKey('formations_simplon.id_formation'), nullable=False)
    region = Column(String, ForeignKey('regions.region'), nullable=False)

    # Relation avec Regions
    formation = relationship("Regions", backref="sessions_simplon")

class Regions(Base):
    __tablename__ = 'regions'
    region = Column(String, primary_key=True, nullable=False)

    # Relation avec AssFormationsExtRegions
    ass_formations_ext_regions = relationship("AssFormationsExtRegions", backref="regions")

    #liaison formations_ext et regions
class AssFormationsExtRegions(Base):
    __tablename__ = 'ass_formations_ext_regions'
    id_formation_ext = Column(Integer, ForeignKey('formations_ext.id_formation_ext'), primary_key=True, nullable=False)
    region = Column(String, ForeignKey('regions.region'), primary_key=True, nullable=False)

    # __table_args__ = (PrimaryKeyConstraint('region', 'id_formation_ext'),)

    # Relation avec FormationsExt
    formations_ext = relationship("FormationsExt", backref="ass_formations_ext_regions")

class FormationsExt(Base):
    __tablename__ = 'formations_ext'
    id_formation_ext = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    intitule_formation = Column(String, nullable=True)
    organisme = Column(String, nullable=True)

    # Relation avec AssRegistresFormacodes
    ass_formations_ext_registres = relationship("AssFormationsExtRegistres", backref="formations_ext")


class Formacodes(Base):
    __tablename__ = 'formacodes'
    formacode_code = Column(Integer, primary_key=True, nullable=False)
    formacode_nom = Column(String, nullable=True)

    # Relation avec AssRegistresFormacodes
    ass_registres_formacodes = relationship("AssRegistresFormacodes", backref="formacodes")


class Nsf(Base):
    __tablename__ = 'nsf'
    nsf_code = Column(Integer, primary_key=True, nullable=False)
    nsf_nom = Column(String, nullable=True)

    ass_registres_nsf = relationship("AssRegistresNsf", backref="nsf")

