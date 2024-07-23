from sqlalchemy import Column, Integer, String, Float, Date, Boolean, create_engine, ForeignKey, Table
from sqlalchemy.orm import sessionmaker,declarative_base, relationship 
from sqlalchemy.schema import PrimaryKeyConstraint, ForeignKeyConstraint

Base = declarative_base()

class FormationsSimplon(Base):
    __tablename__ = 'formations_simplon'
    id_formation = Column(Integer, primary_key=True, autoincrement=True)
    intitule_formation = Column(String)
    categorie = Column(String)
    # voie_acces = Column(String)

    rel_session_formation = relationship('SessionsFormations', back_populates='rel_formation_session')
    rel_registre_formation = relationship('Registres', secondary='ass_formations_registres', back_populates='rel_formation_registre')


# class FormationsExt(Base):
#     __tablename__ = 'formations_ext'
#     id_formation = Column(Integer, primary_key=True, autoincrement=True)
#     intitule_formation = Column(String)
#     organisme = Column(String)

#     rel_registre_formation_ext = relationship('Registres', secondary='ass_formations_ext_registres', back_populates='rel_formation_ext_registre')
#     rel_region_formation_ext = relationship('Regions', secondary='ass_regions_formations_ext', back_populates='rel_formation_ext_region')

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

    rel_session_region = relationship('SessionsFormations', back_populates='rel_region_session')
    # rel_formation_ext_region = relationship('FormationsExt', secondary='ass_regions_formations_ext', back_populates='rel_region_formation_ext')

class Registres(Base):
    __tablename__ = "registres"
    type_registre = Column(String)
    code_registre = Column(Integer)
    titre_registre = Column(String)
    statut_registre= Column(String)
    niveau_sortie = Column(String)
    url = Column(String)

    __table_args__ =(PrimaryKeyConstraint('type_registre', 'code_registre'),)

    rel_formation_registre = relationship('FormationsSimplon', secondary='ass_formations_registres', back_populates='rel_registre_formation')
    rel_nsf_registre = relationship('Nsf', secondary='ass_registres_nsf', back_populates='rel_registre_nsf')
    rel_formacode_registre = relationship('Formacodes', secondary='ass_registres_formacodes', back_populates='rel_registre_formacode')
    # rel_formation_ext_registre = relationship('FormationsExt', secondary='ass_formations_ext_registres', back_populates='rel_registre_formation_ext')

class Nsf(Base):
    __tablename__ = "nsf"
    code_nsf = Column(String, primary_key=True, nullable=False)
    nom_nsf = Column(String)

    rel_registre_nsf = relationship('Registres', secondary='ass_registres_nsf', back_populates='rel_nsf_registre')    

class Formacodes(Base):
    __tablename__ = "formacodes"
    code_formacode = Column(Integer, primary_key=True, nullable=False)
    nom_formacode = Column(String)

    rel_registre_formacode = relationship('Registres', secondary='ass_registres_formacodes', back_populates='rel_formacode_registre')
   
class AssFormationsRegistres(Base):
    __tablename__ = "ass_formations_registres"
    id_formation = Column(Integer, ForeignKey('formations_simplon.id_formation'), primary_key=True)
    type_registre = Column(String, primary_key=True, nullable=False)
    code_registre = Column(Integer, primary_key=True, nullable=False)

    __table_args__ = (ForeignKeyConstraint(['type_registre','code_registre'],['registres.type_registre','registres.code_registre'],),)

# class AssFormationsExtRegistres(Base):
#     __tablename__ = "ass_formations_ext_registres"
#     id_formation = Column(Integer, ForeignKey('formations_ext.id_formation'), primary_key=True)
#     type_registre = Column(String, primary_key=True)
#     code_registre = Column(Integer, primary_key=True)

    # __table_args__ = (ForeignKeyConstraint(['type_registre','code_registre'],['registres.type_registre','registres.code_registre'],),)

class AssRegistresNsf(Base):
    __tablename__ = "ass_registres_nsf"
    code_nsf= Column(String, ForeignKey('nsf.code_nsf'), primary_key=True)
    type_registre = Column(String, primary_key=True)
    code_registre = Column(Integer, primary_key=True)

    __table_args__ = (ForeignKeyConstraint(['type_registre','code_registre'],['registres.type_registre','registres.code_registre'],),)

class AssRegistresFormacodes(Base):
    __tablename__ = "ass_registres_formacodes"
    code_formacode = Column(Integer, ForeignKey('formacodes.code_formacode'), primary_key=True)
    type_registre = Column(String, primary_key=True)
    code_registre = Column(Integer, primary_key=True)

    __table_args__ = (ForeignKeyConstraint(['type_registre','code_registre'],['registres.type_registre','registres.code_registre'],),)

# class AssRegionsFormationsExt(Base):
#     __tablename__ = 'ass_regions_formations_ext'
#     id_formation = Column(Integer, ForeignKey('formations_ext.id_formation'), primary_key=True)
#     region = Column(String, ForeignKey('regions.region'), primary_key=True)

# engine = create_engine('sqlite:///mydatabase.db')
# Base.metadata.create_all(engine)
# Session = sessionmaker(bind=engine)