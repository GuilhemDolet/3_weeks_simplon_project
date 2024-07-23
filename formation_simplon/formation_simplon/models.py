from sqlalchemy import Column, Integer, String, Float, Date, Boolean, create_engine, ForeignKey, Table
from sqlalchemy.orm import sessionmaker,declarative_base, relationship 
from sqlalchemy.schema import PrimaryKeyConstraint, ForeignKeyConstraint

Base = declarative_base()
engine = create_engine('sqlite:///mydatabase.db')
Session = sessionmaker(bind=engine)

#-------------------------- TABLE ASSOCIATIONS --------------------# 
# Uniquement pour la partie de la BDD peuplé par les données de Mon compte formation

ass_formations_ext_registres = Table(
                    'ass_formations_ext_registres', Base.metadata,
                    Column('id_formation', Integer, ForeignKey('formations_ext.id_formation'), primary_key=True),
                    Column('type_registre', String, ForeignKey('registres.type_registre'), primary_key=True),
                    Column('code_registre', String, ForeignKey('registres.code_registre'), primary_key=True)
)
ass_formations_ext_regions = Table (
                    'ass_formations_ext_regions', Base.metadata,
                    Column('id_formation', Integer, ForeignKey('formations_ext.id_formation'), primary_key=True),
                    Column('region', String, ForeignKey('regions.region'), primary_key=True)
)
# ---------------------------------------------------------------------


# class FormationsSimplon(Base):
#     __tablename__ = 'formations_simplon'
#     id_formation = Column(Integer, primary_key=True, autoincrement=True)
#     intitule_formation = Column(String)
#     categorie = Column(String)
#     # voie_acces = Column(String)

#     rel_session_formation = relationship('SessionsFormations', back_populates='rel_formation_session')
#     rel_registre_formation = relationship('Registres', secondary='ass_formations_registres', back_populates='rel_formation_registre')


class FormationsExt(Base):
    __tablename__ = 'formations_ext'
    id_formation = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    intitule_formation = Column(String)
    organisme = Column(String)

    # relation many-to-many avec Registres
    formation_ext = relationship("Registres", secondary=ass_formations_ext_registres, 
                                 foreign_keys=[ass_formations_ext_registres.c.id_formation, 
                                 ass_formations_ext_registres.c.type_registre, 
                                 ass_formations_ext_registres.c.code_registre],
                                 back_populates="registres_formation_ext",
                                 primaryjoin='FormationsExt.id_formation == ass_formations_ext_registres.c.id_formation',
                                 secondaryjoin='and_(Registres.type_registre == ass_formations_ext_registres.c.type_registre, '
                                 'Registres.code_registre == ass_formations_ext_registres.c.code_registre)'
                                 )

    # relation many-to-many avec Registres
    region = relationship("Regions", secondary=ass_formations_ext_regions, back_populates="formation_ext")

# class SessionsFormations(Base):
#     __tablename__ = 'sessions'
#     id_session = Column(Integer, primary_key=True, autoincrement=True)
#     agence = Column(String)
#     distanciel = Column(Boolean)
#     alternance = Column(Boolean)
#     echelle_duree = Column(String)
#     date_limite = Column(Date)
#     date_debut = Column(Date)
#     date_fin = Column(Date)
#     id_formation = Column(Integer, ForeignKey('formations_simplon.id_formation'))
#     region = Column(String, ForeignKey('regions.region'))

#     rel_formation_session = relationship('FormationsSimplon', back_populates='rel_session_formation')
#     rel_region_session = relationship('Regions', back_populates='rel_session_region')

class Regions(Base):
    __tablename__ = "regions" 
    region = Column(String, primary_key=True)

    # rel_session_region = relationship('SessionsFormations', back_populates='rel_region_session')
     # Relation many-to-many avec FormationExt
    formation_ext = relationship("FormationsExt", secondary=ass_formations_ext_regions, back_populates='region')
class Registres(Base):
    __tablename__ = "registres"
    type_registre = Column(String)
    code_registre = Column(Integer)
    titre_registre = Column(String)
    statut_registre= Column(String)
    niveau_sortie = Column(String)
    url = Column(String)

    __table_args__ =(PrimaryKeyConstraint('type_registre', 'code_registre'),)

    # rel_formation_registre = relationship('FormationsSimplon', secondary='ass_formations_registres', back_populates='rel_registre_formation')
    rel_nsf_registre = relationship('Nsf', secondary='ass_registres_nsf', back_populates='rel_registre_nsf')
    rel_formacode_registre = relationship('Formacodes', secondary='ass_registres_formacodes', back_populates='rel_registre_formacode')
    # Relation many-to-many avec FormationExt
    registres_formation_ext = relationship('FormationsExt', secondary=ass_formations_ext_registres, 
                                           foreign_keys=[ass_formations_ext_registres.c.id_formation, 
                                                        ass_formations_ext_registres.c.type_registre, 
                                                        ass_formations_ext_registres.c.code_registre], 
                                                        back_populates='formation_ext',
                                                        primaryjoin='and_(Registres.type_registre == ass_formations_ext_registres.c.type_registre, '
                                                        'Registres.code_registre == ass_formations_ext_registres.c.code_registre)',
                                                        secondaryjoin='FormationsExt.id_formation == ass_formations_ext_registres.c.id_formation'
                                                        )
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
   
# class AssFormationsRegistres(Base):
#     __tablename__ = "ass_formations_registres"
#     id_formation = Column(Integer, ForeignKey('formations_simplon.id_formation'), primary_key=True)
#     type_registre = Column(String, primary_key=True, nullable=False)
#     code_registre = Column(Integer, primary_key=True, nullable=False)

#     __table_args__ = (ForeignKeyConstraint(['type_registre','code_registre'],['registres.type_registre','registres.code_registre'],),)

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


if "__main__" == __name__:
    
    Base.metadata.create_all(engine)