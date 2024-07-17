from sqlalchemy import Column, Integer, String, Float, Date, Boolean, BLOB, create_engine, ForeignKey
from sqlalchemy.orm import sessionmaker,declarative_base, relationship 

Base = declarative_base()

class FormationsSimplon(Base):
    __tablename__ = 'formations_simplon'
    id_formation = Column(Integer, primary_key=True, autoincrement=True)
    intitule_formation = Column(String)
    categorie = Column(String)
    voie_acces = Column(String)

    rel_session_formation = relationship('SessionsFormations', back_populates='rel_formation_session',foreign_keys='sessions.id_formation')
    rel_registre_formation = relationship('AssFormationsRegistres', back_populates='rel_ass_formation_registre', foreign_keys='ass_formations_registres.id_formation')

class FormationsExt(Base):
    __tablename__ = 'formations_ext'
    id_formation = Column(Integer, primary_key=True, autoincrement=True)
    intitule_formation = Column(String)
    organisme = Column(String)

    rel_registre_formation_ext = relationship('AssFormationsExtRegistres', back_populates='rel_ass_formation_ext_registre', foreign_keys='ass_formations_ext_registres.id_formation')
    rel_region_formation_ext = relationship('AssRegionsFormationsExt', back_populates='rel_ass_formation_ext_region', foreign_keys='ass_regions_formations_ext')

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
    id_formation = Column(Integer, ForeignKey('formations_simplon.id_formation'))
    region = Column(String, ForeignKey('regions.region'))

    rel_formation_session = relationship('FormationsSimplon', back_populates='rel_session_formation')
    rel_region_session = relationship('Regions', back_populates='rel_session_region')

class Regions(Base):
    __tablename__ = "regions" 
    region = Column(String, primary_key=True)

    rel_session_region = relationship('SessionsFormations', back_populates='rel_region_session', foreign_keys='sessions.region')
    rel_formation_ext_region = relationship('AssRegionsFormationsExt', back_populates='rel_ass_region_formation_ext', foreign_keys='ass_regions_formations_ext.region')

class Registres(Base):
    __tablename__ = "registres"
    type_registre = Column(String, primary_key=True, nullable=False)
    code_registre = Column(Integer, primary_key=True, nullable=False)
    titre_registre = Column(String)
    statut = Column(String)
    niveau_sortie = Column(String)
    url = Column(String)

    rel_formation_registre = relationship('AssFormationsRegistres', back_populates='rel_ass_registre_formation', foreign_keys=('ass_formations_registres.type_registre', 'ass_formations_registres.code_registre'))
    rel_nsf_registre = relationship('AssRegistresNsf', back_populates='rel_ass_nsf_registre', foreign_keys=('ass_registres_nsf.code_registre', 'ass_registres_nsf.type_registre'))
    rel_formacode_registre = relationship('AssRegistresFormacodes', back_populates='rel_ass_formacode_registre', foreign_keys=('ass_registres_formacodes.type_registre', 'ass_registres_formacodes.code_registre'))
    rel_formation_ext_registre = relationship('AssFormationsExtRegistres', back_populates='rel_ass_registre_formation_ext', foreign_keys=('ass_formations_registres.type_registre', 'ass_formations_registres.code_registre'))

class Nsf(Base):
    __tablename__ = "nsf"
    nsf_code = Column(String, primary_key=True, nullable=False)
    nsf_name = Column(String)

    rel_registre_nsf = relationship('AssRegistresNsf', back_populates='rel_ass_registre_nsf', foreign_keys='ass_registres_nsf.nsf_code')

class Formacodes(Base):
    __tablename__ = "formacodes"
    formacode_code = Column(Integer, primary_key=True, nullable=False)
    formacode_nom = Column(String)

    rel_registre_formacode = relationship('AssRegistresFormacodes', back_populates='rel_ass_registre_formacode', foreign_keys='ass_registres_formacodes.formacode_code')

class AssFormationsRegistres(Base):
    __tablename__ = "ass_formations_registres"
    id_formation = Column(Integer, ForeignKey('formations_simplon.id_formation'), primary_key=True)
    type_registre = Column(String, ForeignKey('registres.type_registre'), primary_key=True)
    code_registre = Column(Integer, ForeignKey('registres.code_registre'), primary_key=True)

    rel_ass_formation_registre = relationship('FormationsSimplon', back_populates='rel_registre_formation')
    rel_ass_registre_formation = relationship('Registres', back_populates='rel_formation_registre')

class AssFormationsExtRegistres(Base):
    __tablename__ = "ass_formations_ext_registres"
    id_formation = Column(Integer, ForeignKey('formations_ext.id_formation'), primary_key=True)
    type_registre = Column(String, ForeignKey('registres.type_registre'), primary_key=True)
    code_registre = Column(Integer, ForeignKey('registres.code_registre'), primary_key=True)

    rel_ass_registre_formation_ext = relationship('Registres', back_populates='rel_formation_ext_registre')
    rel_ass_formation_ext_registre = relationship('FormationsExt', back_populates='rel_registre_formation_ext')

class AssRegistresNsf(Base):
    __tablename__ = "ass_registres_nsf"
    code_nsf = Column(Integer, ForeignKey('nsf.nsf_code'), primary_key=True)
    type_registre = Column(String, ForeignKey('registres.type_registre'), primary_key=True)
    code_registre = Column(Integer, ForeignKey('registres.code_registre'), primary_key=True)

    rel_ass_nsf_registre = relationship('Registres', back_populates='rel_nsf_registre')
    rel_ass_registre_nsf = relationship('Nsf', back_populates='rel_registre_nsf')

class AssRegistresFormacodes(Base):
    __tablename__ = "ass_registres_formacodes"
    formacode_code = Column(Integer, ForeignKey('formacodes.formacode_code'), primary_key=True)
    type_registre = Column(String, ForeignKey('registres.type_registre'), primary_key=True)
    code_registre = Column(Integer, ForeignKey('registres.code_registre'), primary_key=True)

    rel_ass_formacode_registre = relationship('Registres', back_populates='rel_formacode_registre')
    rel_ass_registre_formacode = relationship('Formacodes', back_populates='rel_registre_formacode')

class AssRegionsFormationsExt(Base):
    __tablename__ = 'ass_regions_formations_ext'
    id_formation = Column(Integer, ForeignKey('formations_ext.id_formation'), primary_key=True)
    region = Column(String, ForeignKey('regions.region'), primary_key=True)

    rel_ass_region_formation_ext = relationship('Regions', back_populates='rel_formation_ext_region')
    rel_ass_formation_ext_region = relationship('FormationsExt', back_populates='rel_region_formation_ext')

engine = create_engine('sqlite:///mydatabase.db')
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)