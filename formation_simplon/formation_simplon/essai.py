from fastapi import FastAPI, HTTPException
from sqlalchemy import Column, Integer, String, Float, MetaData, create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
from models import Base
# from .models import FormationsSimplon, FormationsExt, SessionsFormations, Regions, Registres, Nsf, Formacodes
# from .models import AssFormationsRegistres, AssFormationsExtRegistres, AssRegistresNsf, AssRegistresFormacodes, AssRegionsFormationsExt
from models import FormationsSimplon
from models import SessionsFormations
# from .models import FormationsExt
from models import Regions
from models import Registres
from models import Nsf
from models import Formacodes
from models import AssFormationsRegistres
# from .models import AssFormationsExtRegistres
from models import AssRegistresNsf
from models import AssRegistresFormacodes
# from .models import AssRegionsFormationsExt
from dotenv import load_dotenv
import os
import csv

load_dotenv()

username = os.getenv("USER_NAME")
password = os.getenv("PASSWORD")
server = os.getenv("SERVER")
nom_db = os.getenv("NOM_DB")

app = FastAPI()

def session_open():
    # url_db = f"postgresql://{username}:{password}@{server}.postgres.database.azure.com:5432/{nom_db}"
    # engine = create_engine(url_db)
    engine = create_engine('sqlite:///../mydatabase.db')
    
    Session = sessionmaker(bind=engine)
    session = Session()
    return session

def essai():
    
    session = session_open()
    # intitule_test = f"%{intitule}%"
    match_intitule = session.query(FormationsSimplon.id_formation,
                                   FormationsSimplon.intitule_formation,
                                   FormationsSimplon.categorie,
                                   SessionsFormations.agence,
                                   SessionsFormations.distanciel,
                                   SessionsFormations.alternance,
                                   SessionsFormations.date_limite,
                                   SessionsFormations.date_debut,
                                   SessionsFormations.date_fin)\
        .select_from(FormationsSimplon)\
        .outerjoin(SessionsFormations, SessionsFormations.id_formation == FormationsSimplon.id_formation)\
        .filter(FormationsSimplon.id_formation == 21).all()
    if match_intitule:
        session.close()
        return "trouvé", match_intitule
    else:
        session.close()
        return "pas trouvé"
    
print(essai())
    
    # if __name__==