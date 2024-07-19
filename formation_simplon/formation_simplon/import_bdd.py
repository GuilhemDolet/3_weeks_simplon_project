from model_bdd.models import Session, FormationsExt, Regions, Registres
import json

data_url = 'formation_simplon/data.json'

def load_json_into_databse(Session, data_url):

    with open(data_url, 'r', encoding= 'utf-8') as file:
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

            # Remplissage de la table Registre + sa table d'association
            #Type RS
            if entry.get('type_referentiel') == 'RS': # type string
                registre_exist = session.query(Registres).filter_by(type_registre=entry.get('type_referentiel'), code_registre=entry.get('code_inventaire')).first()

                if registre_exist is None:
                    ligne_registre = Registres(
                        type_registre = entry.get('type_referentiel'),
                        code_registre = entry.get('code_inventaire'),
                        titre = entry.get('intitule_certification'),
                        statut = "ACTIF",
                        niveau_sortie = entry.get('libelle_niveau_sortie_formation'),
                        url = None
                    )
                ligne_formation_ext.formation_ext.append(ligne_registre)

            #Type RNCP
            elif entry.get('type_referentiel') == 'RNCP': # type string
                registre_exist = session.query(Registres).filter_by(type_registre=entry.get('type_referentiel'), code_registre=entry.get('code_inventaire')).first()

                if registre_exist is None:
                    ligne_registre = Registres(
                        type_registre = entry.get('type_referentiel'),
                        code_registre = entry.get('code_rncp'),
                        titre = entry.get('intitule_certification'),
                        statut = "ACTIF",
                        niveau_sortie = entry.get('libelle_niveau_sortie_formation'),
                        url = None
                    )
                ligne_formation_ext.formation_ext.append(ligne_registre)



        session.commit()
    except:
        session.rollback()
        raise
    finally:
        session.close()

load_json_into_databse(Session, data_url)