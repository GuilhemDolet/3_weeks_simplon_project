from model_bdd.models import Session, FormationsExt, Regions
import json


def load_json_into_databse(Session):

    with open('formation_simplon/data.json', 'r', encoding= 'utf-8') as file:
        data = json.load(file)

    session = Session()
    try:
        for entry in data:
            # Remplissage de la table FormationExt
            ligne_formation_ext = FormationsExt(
                intitule_formation = entry.get('intitule_certification'),
                organisme = entry.get('nom_of')
            )
            session.add(ligne_formation_ext)

            #Remplissage de la table Region
            region_exist = session.query(Regions).filter_by(region=entry.get('nom_region')).first()
            
            if region_exist is None and entry.get('nom_region'):
                ligne_region = Regions(
                    region = entry.get('nom_region')
                )
                session.add(ligne_region)
                ligne_formation_ext.region.append(ligne_region)

            elif region_exist and entry.get('nom_region'):
                ligne_formation_ext.region.append(region_exist)

        session.commit()
    except:
        session.rollback()
        raise

    finally:
        session.close()

load_json_into_databse(Session)