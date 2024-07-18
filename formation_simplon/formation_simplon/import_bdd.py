from models import Session, FormationsExt
import json

def load_json_into_databse(Session):

    with open('formation_simplon/data.json', 'r', encoding= 'utf-8') as file:
        data = json.load(file)

    session = Session()
    try:
        for entry in data:
            une_ligne = FormationsExt(
                intitule_formation = entry.get('intitule_certification'),
                organisme = entry.get('nom_of')
            )
            session.add(une_ligne)
        session.commit()
    except:
        session.rollback()
        raise

    finally:
        session.close()

load_json_into_databse(Session)