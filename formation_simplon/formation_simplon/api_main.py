from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from sqlalchemy import Column, Integer, String, Float, MetaData, create_engine, and_
from sqlalchemy.orm import declarative_base, sessionmaker
from models import Base
# from models import FormationsSimplon, FormationsExt, SessionsFormations, Regions, Registres, Nsf, Formacodes
# from models import AssFormationsRegistres, AssFormationsExtRegistres, AssRegistresNsf, AssRegistresFormacodes, AssRegionsFormationsExt
from models import FormationsSimplon
from models import SessionsFormations
from models import FormationsExt
from models import Regions
from models import Registres
from models import Nsf
from models import Formacodes
from models import AssFormationsRegistres
# from models import AssFormationsExtRegistres
from models import AssRegistresNsf
from models import AssRegistresFormacodes
# from models import AssRegionsFormationsExt
from models import ass_formations_ext_registres
from models import ass_formations_ext_regions

app = FastAPI()

def session_open():
    engine = create_engine('sqlite:///mydatabase.db', connect_args={"check_same_thread": False})   
    Session = sessionmaker(bind=engine)
    session = Session()
    return session

# affichage des formations simplon dont l'intitulé de formation contient intitule
@app.get("/formation_simplon_from_intitule")
def get_formation_simplon(intitule:str):
    session = session_open()
    intitule_test = f"%{intitule}%"
    match_intitule = session.query(FormationsSimplon).filter(FormationsSimplon.intitule_formation.ilike(intitule_test)).all()
    if match_intitule:
        session.close()
        return match_intitule
    else:
        session.close()
        return "pas trouvé"
    
# affichage des formations simplon et des sessions dont l'intitulé de formation contient intitule
@app.get("/formations_sessions")
def get_formation_session(intitule:str):
    session = session_open()
    intitule_test = f"%{intitule}%"
    results = []
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
        .filter(FormationsSimplon.intitule_formation.ilike(intitule_test)).all()
    if match_intitule:
        for match in match_intitule:
            results.append(match._mapping)
        session.close()
        return results
    else:
        session.close()
        return "pas trouvé" 

# affichage des formations simplon,sessions et regions dont l'intitulé de formation contient intitule    
@app.get("/session_region")
def get_session_region(intitule:str):
    session = session_open()

    intitule_test = f"%{intitule}%"
    results = []
    match_intitule = session.query(FormationsSimplon.id_formation,
                                   FormationsSimplon.intitule_formation,
                                   FormationsSimplon.categorie,
                                   Regions.region,
                                   SessionsFormations.agence,
                                   SessionsFormations.distanciel,
                                   SessionsFormations.alternance,
                                   SessionsFormations.date_limite,
                                   SessionsFormations.date_debut,
                                   SessionsFormations.date_fin)\
        .select_from(FormationsSimplon)\
        .join(SessionsFormations, SessionsFormations.id_formation == FormationsSimplon.id_formation)\
        .join(Regions, SessionsFormations.region == Regions.region)\
        .filter(FormationsSimplon.intitule_formation.ilike(intitule_test)).all()
    if match_intitule:
        for match in match_intitule:
            results.append(match._mapping)
        session.close()
        return results
    else:
        session.close()
        return "pas trouvé"

# affichage formations simplon et registres
@app.get("/formations_simplon_registes")
def get_formations_registres(intitule:str):
    session = session_open()
    intitule_test = f"%{intitule}%"
    results = []
    match_intitule = session.query(FormationsSimplon, Registres)\
        .select_from(FormationsSimplon)\
        .outerjoin(AssFormationsRegistres, AssFormationsRegistres.id_formation == FormationsSimplon.id_formation)\
        .outerjoin(Registres, (Registres.code_registre == AssFormationsRegistres.code_registre and Registres.type_registre == AssFormationsRegistres.type_registre)) \
        .filter(FormationsSimplon.intitule_formation.ilike(intitule_test)).all()
    if match_intitule:
        for match in match_intitule:
            results.append(match._mapping)
        session.close()
        return results
    else:
        session.close()
        return "pas trouvé"

# affichage formacodes depuis registre
@app.get("/registes_formacodes")
def get_formacodes_from_registre(type_registre:str, code_registre:int):
    session = session_open()
    type = f"%{type_registre}%"
    code = code_registre
    results = []
    match_registre = session.query(Registres, Formacodes)\
        .select_from(Registres)\
        .outerjoin(AssRegistresFormacodes, and_(AssRegistresFormacodes.type_registre == Registres.type_registre, AssRegistresFormacodes.code_registre == Registres.code_registre))\
        .outerjoin(Formacodes, Formacodes.code_formacode == AssRegistresFormacodes.code_formacode)\
        .filter(and_(Registres.type_registre.ilike(type), Registres.code_registre == code)).all()
    if match_registre:
        for match in match_registre:
            results.append(match._mapping)
        session.close()
        return results
    else:
        session.close()
        return "pas trouvé"
    
# affichage formacodes et nsf depuis registre
@app.get("/registes_formacodes_nsf")
def get_formacodes_nsf_from_registre(type_registre:str, code_registre:int):
    session = session_open()
    type = f"%{type_registre}%"
    code = code_registre
    results = []
    match_registre = session.query(Registres, Formacodes, Nsf)\
        .select_from(Registres)\
        .outerjoin(AssRegistresFormacodes, and_(AssRegistresFormacodes.type_registre == Registres.type_registre, AssRegistresFormacodes.code_registre == Registres.code_registre))\
        .outerjoin(Formacodes, Formacodes.code_formacode == AssRegistresFormacodes.code_formacode)\
        .outerjoin(AssRegistresNsf, and_(AssRegistresNsf.type_registre == Registres.type_registre, AssRegistresNsf.code_registre == Registres.code_registre))\
        .outerjoin(Nsf, Nsf.code_nsf == AssRegistresNsf.code_nsf)\
        .filter(and_(Registres.type_registre.ilike(type), Registres.code_registre == code)).all()
    if match_registre:
        for match in match_registre:
            results.append(match._mapping)
        session.close()
        return results
    else:
        session.close()
        return "pas trouvé"
    
# affichage nsf depuis registre
@app.get("/registes_nsf")
def get_nsf_from_registre(type_registre:str, code_registre:int):
    session = session_open()
    type = f"%{type_registre}%"
    code = code_registre
    results = []
    match_registre = session.query(Registres, Nsf)\
        .select_from(Registres)\
        .join(AssRegistresNsf, and_(AssRegistresNsf.type_registre == Registres.type_registre, AssRegistresNsf.code_registre == Registres.code_registre))\
        .join(Nsf, Nsf.code_nsf == AssRegistresNsf.code_nsf)\
        .filter(and_(Registres.type_registre.ilike(type), Registres.code_registre == code)).all()
    if match_registre:
        for match in match_registre:
            results.append(match._mapping)
        session.close()
        return results
    else:
        session.close()
        return "pas trouvé"

# affichage toutes les infos pour une formation simplon    
@app.get("/formations_simplon_complete_from_intitule")
def get_formations_complete_from_intitule(intitule:str):
    session = session_open()
    intitule_test = f"%{intitule}%"
    results = []
    match_intitule = session.query(FormationsSimplon, SessionsFormations.region, SessionsFormations, Registres, Formacodes, Nsf)\
        .select_from(FormationsSimplon)\
        .join(SessionsFormations, SessionsFormations.id_formation == FormationsSimplon.id_formation)\
        .outerjoin(AssFormationsRegistres, AssFormationsRegistres.id_formation == FormationsSimplon.id_formation)\
        .outerjoin(Registres, and_(Registres.code_registre == AssFormationsRegistres.code_registre, Registres.type_registre == AssFormationsRegistres.type_registre))\
        .outerjoin(AssRegistresFormacodes, and_(AssRegistresFormacodes.type_registre == Registres.type_registre, AssRegistresFormacodes.code_registre == Registres.code_registre))\
        .outerjoin(Formacodes, Formacodes.code_formacode == AssRegistresFormacodes.code_formacode)\
        .outerjoin(AssRegistresNsf, and_(AssRegistresNsf.type_registre == Registres.type_registre, AssRegistresNsf.code_registre == Registres.code_registre))\
        .outerjoin(Nsf, Nsf.code_nsf == AssRegistresNsf.code_nsf)\
        .filter(FormationsSimplon.intitule_formation.ilike(intitule_test)).all()
    if match_intitule:
        for match in match_intitule:
            results.append(match._mapping)
        session.close()
        return results
    else:
        session.close()
        return "pas trouvé"

@app.get("/registre_from_formacode")
def get_registre_from_formacode(code_formacode:int):
    session = session_open()
    code = code_formacode
    results = []
    match_formacode = session.query(Formacodes, Registres)\
        .select_from(Formacodes)\
        .join(AssRegistresFormacodes, AssRegistresFormacodes.code_formacode == Formacodes.code_formacode)\
        .join(Registres, and_(AssRegistresFormacodes.type_registre == Registres.type_registre, AssRegistresFormacodes.code_registre == Registres.code_registre))\
        .filter(Formacodes.code_formacode == code).all()
    if match_formacode:
        for match in match_formacode:
            results.append(match._mapping)
        session.close()
        return results
    else:
        session.close()
        return "pas trouvé"

# affichage des formations/sessions/registres depuis formacode)
@app.get("/formation_from_formacode")
def get_formation_from_formacode(code_formacode:int):
    session = session_open()
    code = code_formacode
    results = []
    match_formacode = session.query(Formacodes, Registres, FormationsSimplon, SessionsFormations.region, SessionsFormations)\
        .select_from(Formacodes)\
        .join(AssRegistresFormacodes, AssRegistresFormacodes.code_formacode == Formacodes.code_formacode)\
        .join(Registres, and_(AssRegistresFormacodes.type_registre == Registres.type_registre, AssRegistresFormacodes.code_registre == Registres.code_registre))\
        .join(AssFormationsRegistres, and_(AssFormationsRegistres.type_registre == Registres.type_registre, AssFormationsRegistres.code_registre == Registres.code_registre))\
        .join(FormationsSimplon, FormationsSimplon.id_formation == AssFormationsRegistres.id_formation)\
        .filter(Formacodes.code_formacode == code).all()
    if match_formacode:
        for match in match_formacode:
            results.append(match._mapping)
        session.close()
        return results
    else:
        session.close()
        return "pas trouvé"

# affichage des formations extérieures 
@app.get("/formations_ext")    
def get_formations_ext_from_intitule(intitule:str):
    session = session_open()
    intitule_test = f"%{intitule}%"
    match_intitule = session.query(FormationsExt).filter(FormationsExt.intitule_formation.ilike(intitule_test)).all()
    if match_intitule:
        session.close()
        return match_intitule
    else:
        session.close()
        return "pas trouvé"
    
# affichage régions depuis intitulé formation_ext
@app.get("/region_from_formations_ext")
def get_region_from_formation_ext(intitule):
    session = session_open()
    intitule_test = f"%{intitule}%"
    results = []
    match_intitule = session.query(FormationsExt, Regions)\
        .select_from(FormationsExt)\
        .outerjoin(ass_formations_ext_regions, ass_formations_ext_regions.c.id_formation == FormationsExt.id_formation)\
        .outerjoin(Regions, Regions.region == ass_formations_ext_regions.c.region)\
        .filter(FormationsExt.intitule_formation.ilike(intitule_test)).all()
    if match_intitule:
        for match in match_intitule:
            results.append(match._mapping)
            session.close()
        return results
    else:
        session.close()
        return "pas trouvé"

# affichage registre depuis formations_ext
@app.get("/registre_from_formation")    
def get_registre_from_formation_ext(intitule):
    session = session_open()
    intitule_test = f"%{intitule}%"
    results = []
    match_intitule = session.query(FormationsExt, Registres)\
        .select_from(FormationsExt)\
        .outerjoin(ass_formations_ext_registres, ass_formations_ext_registres.c.id_formation == FormationsExt.id_formation)\
        .outerjoin(Registres, and_(Registres.type_registre == ass_formations_ext_registres.c.type_registre, Registres.code_registre == ass_formations_ext_registres.c.code_registre))\
        .filter(FormationsExt.intitule_formation.ilike(intitule_test)).all()
    if match_intitule:
        for match in match_intitule:
            results.append(match._mapping)
        session.close()
        return results
    else:
        session.close()
        return "pas trouvé"

# affichage infos complètes formations ext depuis intitule    
@app.get("/formations_ext_complete")
def get_formations_ext_complete(intitule):
    session = session_open()
    intitule_test = f"%{intitule}%"
    results = []
    match_intitule = session.query(FormationsExt, Regions, Registres, Formacodes, Nsf)\
        .select_from(FormationsExt)\
        .outerjoin(ass_formations_ext_regions, ass_formations_ext_regions.c.id_formation == FormationsExt.id_formation)\
        .outerjoin(Regions, Regions.region == ass_formations_ext_regions.c.region)\
        .outerjoin(ass_formations_ext_registres, ass_formations_ext_registres.c.id_formation == FormationsExt.id_formation)\
        .outerjoin(Registres, and_(Registres.type_registre == ass_formations_ext_registres.c.type_registre, Registres.code_registre == ass_formations_ext_registres.c.code_registre))\
        .outerjoin(AssRegistresFormacodes, and_(AssRegistresFormacodes.type_registre == Registres.type_registre, AssRegistresFormacodes.code_registre == Registres.code_registre))\
        .outerjoin(Formacodes, Formacodes.code_formacode == AssRegistresFormacodes.code_formacode)\
        .outerjoin(AssRegistresNsf, and_(AssRegistresNsf.type_registre == Registres.type_registre, AssRegistresNsf.code_registre == Registres.code_registre))\
        .outerjoin(Nsf, Nsf.code_nsf == AssRegistresNsf.code_nsf)\
        .filter(FormationsExt.intitule_formation.ilike(intitule_test)).all()
    if match_intitule:
        for match in match_intitule:
            results.append(match._mapping)
        session.close()
        return results
    else:
        session.close()
        return "pas trouvé"

# affichage des formations/registres depuis formacode)
@app.get("/formation_ext_from_formacode")
def get_formation_ext_from_formacode(code_formacode:int):
    session = session_open()
    code =code_formacode
    results = []
    match_formacode = session.query(Formacodes,Registres, FormationsExt, Regions)\
        .select_from(Formacodes)\
        .join(AssRegistresFormacodes, AssRegistresFormacodes.code_formacode==Formacodes.code_formacode)\
        .join(Registres, and_(Registres.code_registre==AssRegistresFormacodes.code_registre, Registres.type_registre==AssRegistresFormacodes.type_registre))\
        .join(ass_formations_ext_registres, and_(ass_formations_ext_registres.c.type_registre==Registres.type_registre, ass_formations_ext_registres.c.code_registre==Registres.code_registre))\
        .join(FormationsExt, FormationsExt.id_formation==ass_formations_ext_registres.c.id_formation)\
        .outerjoin(ass_formations_ext_regions, ass_formations_ext_regions.c.id_formation==FormationsExt.id_formation)\
        .outerjoin(Regions, Regions.region==ass_formations_ext_regions.c.region)\
        .filter(Formacodes.code_formacode == code).all()
    if match_formacode:
        for match in match_formacode:
            results.append(match._mapping)
        session.close()
        return results
    else:
        session.close()
        return "pas trouvé"