import os
from sqlalchemy import Column, Integer, String, Boolean, Date, ForeignKey, Table
from sqlalchemy.orm import declarative_base, relationship, mapped
from sqlalchemy import create_engine

# Définir la connexion à la base de données à partir des variables d'environnement
DATABASE_URL3 = os.environ.get("DATABASE_URL3")

Base = declarative_base()


# Table d'association pour la relation many-to-many entre FormationsExt et Registres
association_table_formations_ext_registres = Table(
    "association_table_formations_ext_registres",
    Base.metadata,
    Column("id_formation_ext", Integer, ForeignKey("formations_ext.id_formation_ext"), primary_key=True),
    Column("id_registre", Integer, ForeignKey("registres.id_registre"), primary_key=True),
)

# Table d'association pour la relation many-to-many entre Registres et Nsf
association_table_registres_nsf = Table(
    "association_table_registres_nsf",
    Base.metadata,
    Column("id_registre", Integer, ForeignKey("registres.id_registre"), primary_key=True),
    Column("nsf_code", Integer, ForeignKey("nsf.nsf_code"), primary_key=True),
)

# Table d'association pour la relation many-to-many entre Registres et Formacodes
association_table_registres_formacodes = Table(
    "association_table_registres_formacodes",
    Base.metadata,
    Column("formacode_code", Integer, ForeignKey("formacodes.formacode_code"), primary_key=True),
    Column("id_registre", Integer, ForeignKey("registres.id_registre"), primary_key=True),
)

# Table d'association pour la relation many-to-many entre FormationsSimplon et Registres
association_table_formations_simplon_registres = Table(
    "association_table_formations_simplon_registres",
    Base.metadata,
    Column("id_formation", Integer, ForeignKey("formations_simplon.id_formation"), primary_key=True),
    Column("id_registre", Integer, ForeignKey("registres.id_registre"), primary_key=True),
)

# Classe Formation
class Formation(Base):
    __tablename__ = "formation"
    id_formation = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100))
    url = Column(String(100))
    
    # Relation one-to-many avec Session
    sessions = relationship("Session", back_populates="formation")
    

# Classe FormationsExt
class FormationsExt(Base):
    __tablename__ = 'formations_ext'
    id_formation_ext = Column(Integer, primary_key=True, autoincrement=True)
    intitule_formation = Column(String)
    organisme = Column(String)

    # Relation many-to-many avec Registres
    registres = relationship("Registres", secondary=association_table_formations_ext_registres, backref="formations_ext")

# Classe Registres
class Registres(Base):
    __tablename__ = 'registres'
    id_registre = Column(Integer, primary_key=True, autoincrement=True)
    type_registre = Column(String)
    code_registre = Column(Integer)
    titre = Column(String)
    statut = Column(String)
    niveau_sortie = Column(String)
    url = Column(String)

    # Relation many-to-many avec FormationsExt
    formations_ext = relationship("FormationsExt", secondary=association_table_formations_ext_registres, backref="registres")

    # Relation many-to-many avec Nsf
    nsf = relationship("Nsf", secondary=association_table_registres_nsf, backref="registres")

    # Relation many-to-many avec Formacodes
    formacodes = relationship("Formacodes", secondary=association_table_registres_formacodes, backref="registres")

    # Relation many-to-many avec FormationsSimplon
    formations_simplon = relationship("FormationsSimplon", secondary=association_table_formations_simplon_registres, backref="registres")

# Classe Nsf
class Nsf(Base):
    __tablename__ = 'nsf'
    nsf_code = Column(Integer, primary_key=True)
    nsf_nom = Column(String)

    # Relation many-to-many avec Registres
    registres = relationship("Registres", secondary=association_table_registres_nsf, backref="nsf")

# Classe Formacodes
class Formacodes(Base):
    __tablename__ = 'formacodes'
    formacode_code = Column(Integer, primary_key=True)
    formacode_nom = Column(String)

    # Relation many-to-many avec Registres
    registres = relationship("Registres", secondary=association_table_registres_formacodes, backref="formacodes")

# Classe Session (exemple)
class Session(Base):
    __tablename__ = "session"
    id_session = Column(Integer, primary_key=True, autoincrement=True)
    session_name = Column(String(100))
    formation_id = Column(Integer, ForeignKey("formation.id_formation"))
    
    # Relation inverse one-to-many avec Formation
    formation = relationship("Formation", back_populates="sessions")


# Classe Formation
class Formation(Base):
    __tablename__ = "formation"
    id_formation = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100))
    url = Column(String(100))
    
    # Relation one-to-many avec Session
    sessions = relationship("Session", back_populates="formation")
    
# Classe Rncp
class Rncp(Base):
    __tablename__ = "rncp"
    format_code = Column(Integer, primary_key=True)
    name = Column(String(100))

# Classe FormationsExt
class FormationsExt(Base):
    __tablename__ = 'formations_ext'
    id_formation_ext = Column(Integer, primary_key=True, autoincrement=True)
    intitule_formation = Column(String)
    organisme = Column(String)

    # Relation many-to-many avec Registres
    registres = relationship("Registres", secondary=association_table_formations_ext_registres, backref="formations_ext")

# Classe Registres
class Registres(Base):
    __tablename__ = 'registres'
    id_registre = Column(Integer, primary_key=True, autoincrement=True)
    type_registre = Column(String)
    code_registre = Column(Integer)
    titre = Column(String)
    statut = Column(String)
    niveau_sortie = Column(String)
    url = Column(String)

    # Relation many-to-many avec FormationsExt
    formations_ext = relationship("FormationsExt", secondary=association_table_formations_ext_registres, backref="registres")

    # Relation many-to-many avec Nsf
    nsf = relationship("Nsf", secondary=association_table_registres_nsf, backref="registres")

    # Relation many-to-many avec Formacodes
    formacodes = relationship("Formacodes", secondary=association_table_registres_formacodes, backref="registres")

    # Relation many-to-many avec FormationsSimplon
    formations_simplon = relationship("FormationsSimplon", secondary=association_table_formations_simplon_registres, backref="registres")

# Classe Nsf
class Nsf(Base):
    __tablename__ = 'nsf'
    nsf_code = Column(Integer, primary_key=True)
    nsf_nom = Column(String)

    # Relation many-to-many avec Registres
    registres = relationship("Registres", secondary=association_table_registres_nsf, backref="nsf")

# Classe Formacodes
class Formacodes(Base):
    __tablename__ = 'formacodes'
    formacode_code = Column(Integer, primary_key=True)
    formacode_nom = Column(String)

    # Relation many-to-many avec Registres
    registres = relationship("Registres", secondary=association_table_registres_formacodes, backref="formacodes")

# Classe Session (exemple)
class Session(Base):
    __tablename__ = "session"
    id_session = Column(Integer, primary_key=True, autoincrement=True)
    session_name = Column(String(100))
    formation_id = Column(Integer, ForeignKey("formation.id_formation"))
    
    # Relation inverse one-to-many avec Formation
    formation = relationship("Formation", back_populates="sessions")

if __name__ == "__main__":
    # Fonction pour créer la base de données
    def create_database():
        if not DATABASE_URL3:
            raise ValueError("DATABASE_URL3 is not set")

        # Créer le moteur de base de données
        engine = create_engine(DATABASE_URL3)
        Base.metadata.create_all(bind=engine)

    create_database()

if __name__ == "__main__":
    # Fonction pour créer la base de données
    def create_database():
        if not DATABASE_URL3:
            raise ValueError("DATABASE_URL3 is not set")

        # Créer le moteur de base de données
        engine = create_engine(DATABASE_URL3)
        Base.metadata.create_all(bind=engine)

    create_database()