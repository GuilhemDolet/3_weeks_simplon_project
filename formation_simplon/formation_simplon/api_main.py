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

# route ok
@app.get("/intitule")
def get_infos(intitule:str):
    session = session_open()
    intitule_test = f"%{intitule}%"
    match_intitule = session.query(FormationsSimplon).filter(FormationsSimplon.intitule_formation.ilike(intitule_test)).all()
    if match_intitule:
        session.close()
        return "trouvé", match_intitule
    else:
        session.close()
        return "pas trouvé"

# erreur 500 
@app.get("/session")
def get_session(id:int):
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
        .filter(FormationsSimplon.id_formation == id).first()
    if match_intitule:
        session.close()
        return "trouvé", match_intitule
    else:
        session.close()
        return "pas trouvé"

    # match_region = session.query(Regions).filter(Regions.region=="intitule").all()
    # for region in match_region:
    #     print(region.region)
    # match_intitule = session.query(FormationsSimplon, Regions, SessionsFormations)\
    #     .join(SessionsFormations, SessionsFormations.id_formation == FormationsSimplon.id_formation)\
    #     .join(Regions, Regions.region == SessionsFormations.region)\
    #     .filter(FormationsSimplon.intitule_formation.ilike(intitule_test)).all()
    # for intitule in match_intitule:
    #     print(intitule.intitule_formation,
    #         intitule.categorie,
    #         intitule.region,
    #         intitule.agence,
    #         intitule.distanciel,
    #         intitule.alternance,
    #         intitule.echelle_duree,
    #         intitule.date_limite,
    #         intitule.date_debut,
    #         intitule.date_fin)

    # correction IA    
    # for intitule_formation, categorie, region, agence, distanciel, alternance, echelle_duree, date_limite, date_debut, date_fin in match_intitule:
    #     print(intitule_formation,
    #       categorie,
    #       region,
    #       agence,
    #       distanciel,
    #       alternance,
    #       echelle_duree,
    #       date_limite,
    #       date_debut,
    #       date_fin)
def essai(id):
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
        .filter(FormationsSimplon.id_formation == id).first()
    if match_intitule:
        session.close()
        return "trouvé", match_intitule
    else:
        session.close()
        return "pas trouvé"

@app.get("/registre")
def get_infos(code_registre:int):
    session = session_open()
    dict = None
    # results = []
    match_registre = session.query(Registres).filter(Registres.code_registre==code_registre).first()
    if match_registre:
        dict = {"type_registre":match_registre.type_registre,
                    "code_registre":match_registre.code_registre,
                    "titre_registre":match_registre.titre_registre,
                    "statut_registre":match_registre.statut_registre,
                    "niveau_sortie":match_registre.niveau_sortie,
                    "url":match_registre.url}
        results = match_registre
        session.close()
        return "trouvé", dict, results
    else:
        session.close()
        return "pas trouvé"

# route ok    
@app.get("/regions")
def get_region(region:str):
    session = session_open()
    intitule_region = f"%{region}%"
    match_regions = session.query(Regions).filter(Regions.region.ilike(intitule_region)).all()
    if match_regions:
        session.close()
        return "trouvé", match_regions
    else:
        session.close()
        return "pas trouvé"
    
@app.get("/formacode")
def get_infos(code_formacode:int):
    session = session_open()
    dict = None
    results = []
    matchs = session.query(Formacodes, AssRegistresFormacodes, Registres)\
        .join(AssRegistresFormacodes, AssRegistresFormacodes.code_formacode==Formacodes.code_formacode)\
        .join(Registres, Registres.type_registre==AssRegistresFormacodes.type_registre and Registres.code_registre==AssRegistresFormacodes.code_registre)\
        .filter(Formacodes.code_formacode==code_formacode).first()
    if matchs:
               # for match in matchs:
            # dict = {"code_formacode":match.code_formacode,
            #         "nom_formacode":match.nom_formacode,
            #         "type_registre":match.type_registre,
            #         "code_registre":match.code_registre,
            #         "titre_registre":match.titre_registre,
            #         "statut_registre":match.statut_registre,
            #         "niveau_sortie":match.niveau_sortie,
            #         "url":match.url}
        session.close()
        return "trouvé", matchs
    else:
        session.close()
        return "pas trouvé"
