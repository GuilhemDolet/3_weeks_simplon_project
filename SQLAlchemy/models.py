from sqlalchemy import create_engine, Column, Integer, String, Date, Boolean, Float, ForeignKey, PrimaryKeyConstraint, Table
from sqlalchemy.orm import relationship, declarative_base

Base = declarative_base()
engine = create_engine('sqlite:///simplon_bdd.db')

#-------------------------- TABLE ASSOCIATIONS -----------------------#


ass_registres_nsf = Table(
                    'ass_registres_nsf', Base.metadata, # vous dites à SQLAlchemy que cette table fait partie du modèle ORM et qu'elle doit être incluse dans le schéma de la base de données.
                    Column('nsf_code', Integer, ForeignKey('nsf.nsf_code'), primary_key=True),
                    Column('type_registre', String, ForeignKey('registres.type_registre'), primary_key=True),
                    Column('code_registre', String, ForeignKey('registres.code_registre'), primary_key=True),

)

ass_registres_formacodes = Table(
                    'ass_registres_formacodes', Base.metadata,
                    Column('formacodes', Integer, ForeignKey('formacodes.formacode_code'), primary_key=True),
                    Column('type_registre', String, ForeignKey('registres.type_registre'), primary_key=True),
                    Column('code_registre', String, ForeignKey('registres.code_registre'), primary_key=True),
)

ass_formations_simplon_registres = Table(
                    'ass_formations_simplon_registres', Base.metadata,
                    Column('id_formation', Integer, ForeignKey('formations_simplon.id_formation'), primary_key=True),
                    Column('type_registre', String, ForeignKey('registres.type_registre'), primary_key=True),
                    Column('code_registre', String, ForeignKey('registres.code_registre'), primary_key=True),

)

ass_formations_ext_registres = Table(
                    'ass_formations_ext_registres', Base.metadata,
                    Column('id_formation', Integer, ForeignKey('formations_ext.id_formation'), primary_key=True),
                    Column('type_registre', String, ForeignKey('registres.type_registre'), primary_key=True),
                    Column('code_registre', String, ForeignKey('registres.code_registre'), primary_key=True),
)

ass_formations_ext_regions = Table (
                    'ass_formations_ext_regions', Base.metadata,
                    Column('id_formation', Integer, ForeignKey('formations_ext.id_formation'), primary_key=True),
                    Column('region', String, ForeignKey('regions.region'), primary_key=True)
)

#-------------------------- TABLE PRINCIPAL -----------------------#

class Registres(Base):
    __tablename__ = 'registres'
    type_registre = Column(String, nullable=False, primary_key=True, index=True)
    code_registre = Column(Integer, nullable=False, primary_key=True)
    titre = Column(String)
    statut = Column(String)
    niveau_sortie = Column(String)
    url = Column(String)

    #Relation many-to-many avec Nsf (table d'association registres_nsf)
    registres = relationship('Nsf', secondary=ass_registres_nsf, back_populates='nsf')

    # Relation many-to-many avec Formacodes
    registres_formacodes = relationship('Formacodes', secondary=ass_registres_formacodes, back_populates='formacodes')

    # Relation many-to-many avec FormationSimplon
    registres_formation_simplon = relationship('FormationsSimplon', secondary=ass_formations_simplon_registres, back_populates='formation_simplon')
    
    # Relation many-to-many avec FormationExt
    registres_formation_ext = relationship('FormationsExt', secondary=ass_formations_ext_registres, back_populates='formation_ext')

class Nsf(Base):
    __tablename__ = 'nsf'
    nsf_code = Column(Integer, primary_key=True, nullable=False)
    nsf_nom = Column(String)

    #Relation many-to-many avec Registres (table d'association registres_nsf)
    nsf = relationship('Registres', secondary=ass_registres_nsf, back_populates='registres')

class Formacodes(Base):
    __tablename__ = 'formacodes'
    formacode_code = Column(Integer, primary_key=True, nullable=False)
    formacode_nom = Column(String)

    # Relation many-to-many avec Registres
    formacodes = relationship('Registres', secondary=ass_registres_formacodes, back_populates='registres_formacodes')

class FormationsExt(Base):
    __tablename__ = 'formations_ext'
    id_formation = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    intitule_formation = Column(String)
    organisme = Column(String)

    # relation many-to-many avec Registres
    formation_ext = relationship("Registres", secondary=ass_formations_ext_registres, back_populates="registres_formation_ext")

    # relation many-to-many avec Registres
    region = relationship("Regions", secondary=ass_formations_ext_regions, back_populates="formation_ext")

class FormationsSimplon(Base):
    __tablename__ = 'formations_simplon'
    id_formation = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    intitule_formation = Column(String)
    categorie = Column(String)
    voie_acces = Column(String)

    # relation one-to-many avec Sessions
    rel_sessions = relationship("Sessions", back_populates="rel_formations_simplon")

    # relation many-to-many avec Registres
    formation_simplon = relationship("Registres", secondary=ass_formations_simplon_registres, back_populates="registres_formation_simplon")

class Sessions(Base):
    __tablename__ = 'sessions'
    id_session = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    agence = Column(String)
    distanciel = Column(Boolean)
    alternance = Column(Boolean)
    echelle_duree = Column(String)
    date_limite = Column(Date)
    date_debut = Column(Date)
    date_fin = Column(Date)
    id_formation = Column(Integer, ForeignKey('formations_simplon.id_formation'))
    region = Column(Integer, ForeignKey('regions.region'))

    # Relation many-to-one avec FormationsSimplon
    rel_formations_simplon = relationship("FormationsSimplon", back_populates='rel_sessions')

    # Relation many-to-one avec Sessions
    rel_regions = relationship("Regions", back_populates='rel_sessions')

class Regions(Base):

    __tablename__ = 'regions'
    region = Column(String, primary_key=True, nullable=False)

    # Relation one-to-many avec Sessions
    rel_sessions = relationship("Regions", back_populates='rel_regions')

    # Relation many-to-many avec FormationExt
    formation_ext = relationship("FormationsExt", secondary=ass_formations_ext_regions, back_populates='region')


if "__main__" == __name__:
    
    Base.metadata.create_all(engine)