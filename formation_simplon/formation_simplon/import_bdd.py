from models import Session, FormationsExt, Regions, Registres, Nsf, Formacodes

import json
from contextlib import contextmanager

data_url = 'data.json'


@contextmanager
def session_scope(Session):
    session = Session()
    try:
        yield session
        session.commit()
    except:
        session.rollback()
        raise
    finally:
        session.close()

def load_json_into_databse(Session, data_url):
    with open(data_url, 'r', encoding='utf-8') as file:
        data = json.load(file)

    with session_scope(Session) as session:
        for entry in data:
            # Remplissage de la table FormationExt
            ligne_formation_ext = FormationsExt(
                intitule_formation=entry.get('intitule_certification'),
                organisme=entry.get('nom_of')
            )
            session.add(ligne_formation_ext)
            session.flush()  # Pour s'assurer que l'ID est généré

            # Remplissage de la table Region
            region_exist = session.query(Regions).filter_by(region=entry.get('nom_region')).first()

            if region_exist is None and entry.get('nom_region'):
                ligne_region = Regions(region=entry.get('nom_region'))
                session.add(ligne_region)
                session.flush()  # Pour s'assurer que l'ID est généré
                ligne_formation_ext.region.append(ligne_region)
            elif region_exist and entry.get('nom_region'):
                ligne_formation_ext.region.append(region_exist)

            # Remplissage de la table Registre + sa table d'association
            registre_exist = session.query(Registres).filter_by(
                type_registre=entry.get('type_referentiel'),
                code_registre=int(entry.get('code_inventaire') if entry.get('type_referentiel') == 'RS' else entry.get('code_rncp'))
            ).first()

            if registre_exist is None:
                ligne_registre = Registres(
                    type_registre=entry.get('type_referentiel'),
                    code_registre=int(entry.get('code_inventaire') if entry.get('type_referentiel') == 'RS' else entry.get('code_rncp')),
                    titre_registre=entry.get('intitule_certification'),
                    statut_registre="ACTIF",
                    niveau_sortie=entry.get('libelle_niveau_sortie_formation'),
                    url=None
                )
                session.add(ligne_registre)
                session.flush()  # Pour s'assurer que l'ID est généré
            else:
                ligne_registre = registre_exist

            ligne_formation_ext.formation_ext.append(ligne_registre)

            # Remplissage de la table NSF pour un référentiel type RS ou RNCP
            check_and_load_nsf(session, ligne_registre, entry)
            check_and_load_formacodes(session, ligne_registre, entry)

def check_and_load_nsf(session, ligne_registre, entry):
    nsf_dict = {
        'code_nsf_1': 'libelle_nsf_1',
        'code_nsf_2': 'libelle_nsf_2',
        'code_nsf_3': 'libelle_nsf_3'
    }

    nsf_codes = {code: entry.get(code) for code in nsf_dict}
    existing_nsfs = {code: session.query(Nsf).filter_by(code_nsf=nsf_code).first() for code, nsf_code in nsf_codes.items()}

    for code, nsf_code in nsf_codes.items():
        if nsf_code:
            nsf_instance = existing_nsfs.get(code) or session.query(Nsf).filter_by(code_nsf=nsf_code).first()
            if not nsf_instance:
                nsf_instance = Nsf(
                    code_nsf=nsf_code,
                    nom_nsf=entry.get(nsf_dict[code])
                )
                session.add(nsf_instance)
                session.flush()

            if nsf_instance not in ligne_registre.rel_nsf_registre:
                ligne_registre.rel_nsf_registre.append(nsf_instance)

def check_and_load_formacodes(session, ligne_registre, entry):
    formacode_keys = ['code_formacode_1', 'code_formacode_2', 'code_formacode_3', 'code_formacode_4', 'code_formacode_5']
    formacode_codes = [entry.get(key) for key in formacode_keys]
    existing_formacodes = {code: session.query(Formacodes).filter_by(code_formacode=code).first() for code in formacode_codes if code}

    for code in formacode_codes:
        if code:
            formacode_instance = existing_formacodes.get(code) or session.query(Formacodes).filter_by(code_formacode=code).first()
            if not formacode_instance:
                formacode_libelle = entry.get(f'libelle_formacode_{formacode_codes.index(code) + 1}')
                formacode_instance = Formacodes(
                    code_formacode=int(code),
                    nom_formacode=formacode_libelle
                )
                session.add(formacode_instance)
                session.flush()

            if formacode_instance not in ligne_registre.rel_formacode_registre:
                ligne_registre.rel_formacode_registre.append(formacode_instance)

load_json_into_databse(Session, data_url)


# def load_json_into_databse(Session, data_url):

#     with open(data_url, 'r', encoding= 'utf-8') as file:
#         data = json.load(file)

#     session = Session()
#     try:
#         for entry in data:
#             # Remplissage de la table FormationExt
#             ligne_formation_ext = FormationsExt(
#                 intitule_formation = entry.get('intitule_certification'),
#                 organisme = entry.get('nom_of')
#             )
#             session.add(ligne_formation_ext)

#             #Remplissage de la table Region
#             region_exist = session.query(Regions).filter_by(region=entry.get('nom_region')).first()
            
#             if region_exist is None and entry.get('nom_region'):
#                 ligne_region = Regions(
#                     region = entry.get('nom_region')
#                 )
#                 session.add(ligne_region)
#                 ligne_formation_ext.region.append(ligne_region)

#             elif region_exist and entry.get('nom_region'):
#                 ligne_formation_ext.region.append(region_exist)

#             # Remplissage de la table Registre + sa table d'association
#             #Type RS
#             if entry.get('type_referentiel') == 'RS': # type string
#                 registre_exist = session.query(Registres).filter_by(type_registre=entry.get('type_referentiel'), code_registre=entry.get('code_inventaire')).first()

#                 if registre_exist is None:
#                     ligne_registre = Registres(
#                         type_registre = entry.get('type_referentiel'),
#                         code_registre = entry.get('code_inventaire'),
#                         titre_registre = entry.get('intitule_certification'),
#                         statut_registre = "ACTIF",
#                         niveau_sortie = entry.get('libelle_niveau_sortie_formation'),
#                         url = None
#                     )
#                     session.add(ligne_registre)
#                 else:
#                     ligne_registre = registre_exist
                
#                 ligne_formation_ext.formation_ext.append(ligne_registre)

#                 #Remplissage de la table NSF pour un référentiel type RS:
#                 check_and_load_nsf(session, ligne_registre, entry)

#                 check_and_load_formacodes(session, ligne_registre, entry)

#             #Type RNCP
#             elif entry.get('type_referentiel') == 'RNCP': # type string
#                 registre_exist = session.query(Registres).filter_by(type_registre=entry.get('type_referentiel'), code_registre=entry.get('code_inventaire')).first()

#                 if registre_exist is None:
#                     ligne_registre = Registres(
#                         type_registre = entry.get('type_referentiel'),
#                         code_registre = entry.get('code_rncp'),
#                         titre_registre = entry.get('intitule_certification'),
#                         statut_registre = "ACTIF",
#                         niveau_sortie = entry.get('libelle_niveau_sortie_formation'),
#                         url = None
#                     )
#                     session.add(ligne_registre)
#                 else:
#                     ligne_registre = registre_exist

#                 ligne_formation_ext.formation_ext.append(ligne_registre)

#                 #Remplissage de la table NSF pour un référentiel type RNCP:
#                 check_and_load_nsf(session, ligne_registre, entry)

#                 check_and_load_formacodes(session, ligne_registre, entry)

#         session.commit()
#     except:
#         session.rollback()
#         raise
#     finally:
#         session.close()

# def check_and_load_nsf(session, ligne_registre, entry):
    
#     # Dictionnaire pour associer les codes NSF aux libellés
#     nsf_dict = {
#         'code_nsf_1': 'libelle_nsf_1',
#         'code_nsf_2': 'libelle_nsf_2',
#         'code_nsf_3': 'libelle_nsf_3'
#     }
    
#     # Obtenir les codes NSF de l'entrée
#     nsf_codes = {code: entry.get(code) for code in nsf_dict}

#     # Vérifier si les codes NSF existent déjà dans la base de données
#     existing_nsfs = {code: session.query(Nsf).filter_by(code_nsf=nsf_code).first() for code, nsf_code in nsf_codes.items()}

#     # Pour chaque code NSF, ajouter à la table Nsf si non existant
#     for code, nsf_code in nsf_codes.items():
#         if nsf_code and existing_nsfs.get(code) is None:
#             # Si le code NSF n'existe pas encore, l'ajouter
#             ligne_nfs = Nsf(
#                 code_nsf=nsf_code,
#                 nom_nsf=entry.get(nsf_dict[code])
#             )
#             session.add(ligne_nfs)
#             session.flush()  # Assurer que l'ID est généré pour l'association

#         # Ajouter l'association entre Registre et NSF
#         nsf_instance = existing_nsfs.get(code) or session.query(Nsf).filter_by(code_nsf=nsf_code).first()
#         if nsf_instance:
#             if nsf_instance not in ligne_registre.rel_nsf_registre:
#                 ligne_registre.rel_nsf_registre.append(nsf_instance)



# def check_and_load_formacodes(session, ligne_registre, entry):
#     # Liste des clés pour les codes de formacodes
#     formacode_keys = ['code_formacode_1', 'code_formacode_2', 'code_formacode_3', 'code_formacode_4', 'code_formacode_5']

#     # Obtenir les codes de formacodes de l'entrée
#     formacode_codes = [entry.get(key) for key in formacode_keys]

#     # Vérifier si les formacodes existent déjà dans la base de données
#     existing_formacodes = {formacode_code: session.query(Formacodes).filter_by(code_formacode=formacode_code).first()
#                            for formacode_code in formacode_codes if formacode_code}

#     # Pour chaque code de formacode, ajouter à la table Formacodes si non existant
#     for formacode_code in formacode_codes:
#         if formacode_code:
#             if existing_formacodes.get(formacode_code) is None:
#                 # Si le code formacode n'existe pas encore, l'ajouter
#                 formacode_libelle = entry.get(f'libelle_formacode_{formacode_codes.index(formacode_code) + 1}')
#                 ligne_formacode = Formacodes(
#                     code_formacode=formacode_code,
#                     nom_formacode=formacode_libelle
#                 )
#                 session.add(ligne_formacode)
#                 session.flush()  # Assurer que l'ID est généré pour l'association

#             # Ajouter l'association entre Registre et Formacode
#             formacode_instance = existing_formacodes.get(formacode_code) or session.query(Formacodes).filter_by(code_formacode=formacode_code).first()
#             if formacode_instance:
#                 if formacode_instance not in ligne_registre.rel_formacode_registre:
#                     ligne_registre.rel_formacode_registre.append(formacode_instance)

# load_json_into_databse(Session, data_url)