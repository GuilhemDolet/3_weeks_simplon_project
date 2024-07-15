from sqlalchemy import Column, Integer, String, Float, Date, Boolean, BLOB, create_engine, ForeignKey
from sqlalchemy.orm import sessionmaker,declarative_base, relationship 

Base = declarative_base()

class FormationsSimplon(Base):
    __tablename__ = 'formations_simplon'
    id_formation = Column(Integer, primary_key=True, autoincrement=True)
    intitule_formation = Column(String)
    categorie = Column(String)
    voie_acces = Column(String)

    rel_session_formation = relationship('SessionsFormations', back_populates='rel_formation_session')
    rel_registre_formation = relationship('AssFormationsRegistres', back_populates='rel_ass_formation_registre')

class FormationsExt(Base):
    __tablename__ = 'formations_ext'
    id_formation = Column(Integer, primary_key=True, autoincrement=True)
    intitule_formation = Column(String)
    organisme = Column(String)

    rel_registre_formation_ext = relationship('AssFormationsExtRegistres', back_populates='rel_ass_formation_ext_registre')
    rel_region_formation_ext = relationship('AssRegionsFormationsExt', back_populates='rel_ass_formation_ext_region')

class SessionsFormations(Base):
    __tablename__ = 'sessions'
    id_session = Column(Integer, primary_key=True, autoincrement=True)
    agence = Column(String)
    distanciel = Column(Boolean)
    alternance = Column(Boolean)
    echelle_duree = Column(String)
    date_limite = Column(Date)
    date_debut = Column(Date)
    date_fin = Column(Date)
    id_formation = Column(Integer, ForeignKey('FormationsSimplon.id_formation'))
    region = Column(String, ForeignKey('Regions.region'))

    rel_formation_session = relationship('FormationsSimplon', back_populates='rel_session_formation')
    rel_region_session = relationship('Regions', back_populates='rel_session_region')

class Regions(Base):
    __tablename__ = "regions" 
    region = Column(String, primary_key=True)

    rel_session_region = relationship('SessionsFormations', back_populates='rel_region_session')
    rel_formation_ext_region = relationship('AssRegionsFormationsExt', back_populates='rel_ass_region_formation_ext')

class Registres(Base):
    __tablename__ = "registres"
    type_registre = Column(String, primary_key=True, nullable=False)
    code_registre = Column(Integer, primary_key=True, nullable=False)
    titre_registre = Column(String)
    statut = Column(String)
    niveau_sortie = Column(String)
    url = Column(BLOB)

    rel_formation_registre = relationship('AssFormationsRegistres', back_populates='rel_ass_registre_formation')
    rel_nsf_registre = relationship('AssRegistresNsf', back_populates='rel_ass_nsf_registre')
    rel_formacode_registre = relationship('AssRegistresFormacodes', back_populates='rel_ass_formacode_registre')
    rel_formation_ext_registre = relationship('AssFormationsExtRegistres', back_populates='rel_ass_registre_formation_ext')

class Nsf(Base):
    __tablename__ = "nsf"
    nsf_code = Column(Integer)
    nsf_name = Column(String)

    rel_registre_nsf = relationship('AssRegistresNsf', back_populates='rel_ass_registre_nsf')

class Formacodes(Base):
    __tablename__ = "formacodes"
    formacode_code = Column(Integer)
    formacode_nom = Column(String)

    rel_registre_formacode = relationship('AssRegistresFormacodes', back_populates='rel_ass_registre_formacode')

class AssFormationsRegistres(Base):
    __tablename__ = "ass_formations_registres"
    id_formation = Column(Integer, ForeignKey('FormationsSimplon.id_formation'), primary_key=True)
    type_registre = Column(String, ForeignKey('Registres.type_registre'), primary_key=True)
    code_registre = Column(Integer, ForeignKey('Registres.code_registre'), primary_key=True)

    rel_ass_formation_registre = relationship('FormationsSimplon', back_populates='rel_registre_formation')
    rel_ass_registre_formation = relationship('Registres', back_populates='rel_formation_registre')

class AssFormationsExtRegistres(Base):
    __tablename__ = "ass_formations_registres"
    id_formation = Column(Integer, ForeignKey('FormationsSimplon.id_formation'), primary_key=True)
    type_registre = Column(String, ForeignKey('Registres.type_registre'), primary_key=True)
    code_registre = Column(Integer, ForeignKey('Registres.code_registre'), primary_key=True)

    rel_ass_registre_formation_ext = relationship('Registres', back_populates='rel_formation_ext_registre')
    rel_ass_formation_ext_registre = relationship('FormationsExt', back_populates='rel_registre_formation_ext')

class AssRegistresNsf(Base):
    __tablename__ = "ass_registres_nsf"
    code_nsf = Column(Integer, ForeignKey('Nsf.code_nsf'), primary_key=True)
    type_registre = Column(String, ForeignKey('Registres.type_registre'), primary_key=True)
    code_registre = Column(Integer, ForeignKey('Registres.code_registre'), primary_key=True)

    rel_ass_nsf_registre = relationship('Registres', back_populates='rel_nsf_registre')
    rel_ass_registre_nsf = relationship('Nsf', back_populates='rel_registre_nsf')

class AssRegistresFormacodes(Base):
    __tablename__ = "ass_registres_formacodes"
    formacode_code = Column(Integer, ForeignKey('Formacodes.formacode_code'), primary_key=True)
    type_registre = Column(String, ForeignKey('Registres.type_registre'), primary_key=True)
    code_registre = Column(Integer, ForeignKey('Registres.code_registre'), primary_key=True)

    rel_ass_formacode_registre = relationship('Registres', back_populates='rel_formacode_registre')
    rel_ass_registre_formacode = relationship('Formacodes', back_populates='rel_registre_formacode')

class AssRegionsFormationsExt(Base):
    __tablename__ = 'ass_regions_formations_ext'
    id_formation = Column(Integer, ForeignKey('FormationsExt.id_formation'), primary_key=True)
    region = Column(String, ForeignKey('Regions.region'), primary_key=True)

    rel_ass_region_formation_ext = relationship('Regions', back_populates='rel_formation_ext_region')
    rel_ass_formation_ext_region = relationship('FormationsExt', back_populates='rel_region_formation_ext')