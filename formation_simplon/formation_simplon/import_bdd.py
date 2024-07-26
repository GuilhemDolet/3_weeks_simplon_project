from models import Session, FormationsExt, Regions, Registres, Nsf, Formacodes

import json
from contextlib import contextmanager

data_url = 'mon_compte_formation/data.json'


# Fonction pour sécuriser le fonctionnement d'ouverture et de fermeture des Sessions (débugage)
@contextmanager # Créer un gestionnaire de contexte pour utiliser la constructions with avec la fonction session_scope.
def session_scope(Session):
    session = Session()
    try:
        yield session # return la session au moment de son utilisation avec 'with'
        session.commit()
    except:
        session.rollback()
        raise
    finally:
        session.close()

def load_json_into_databse(Session, data_url):
    """
    Charge les données à partir d'un fichier JSON dans une base de données en utilisant une session SQLAlchemy.

    Cette fonction lit un fichier JSON, puis utilise une session de base de données pour remplir les tables
    FormationsExt, Regions et Registres avec les données du fichier. Elle gère les relations et les vérifications
    pour éviter les duplications et s'assure que les identifiants sont correctement générés.

    Args:
        Session (sqlalchemy.orm.sessionmaker): Une fabrique de sessions SQLAlchemy.
        data_url (str): Le chemin vers le fichier JSON contenant les données à charger.

    Raises:
        Exception: Relève toutes les exceptions rencontrées lors de la gestion de la session de base de données.
    """
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
    """
    Vérifie et charge les données NSF dans la base de données et les associe à un registre.

    Cette fonction vérifie si les codes NSF existent déjà dans la base de données. Si un code NSF n'existe pas,
    il crée une nouvelle entrée. Ensuite, elle associe les codes NSF à la ligne de registre donnée.

    Args:
        session (sqlalchemy.orm.Session): La session SQLAlchemy utilisée pour les opérations de base de données.
        ligne_registre (Registres): L'objet de registre auquel les codes NSF seront associés.
        entry (dict): Les données de l'entrée JSON contenant les informations NSF.

    Raises:
        Exception: Relève toutes les exceptions rencontrées lors de la gestion de la session de base de données.
    """
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
    """
    Vérifie et charge les données Formacodes dans la base de données et les associe à un registre.

    Cette fonction vérifie si les codes Formacodes existent déjà dans la base de données. Si un code Formacode
    n'existe pas, il crée une nouvelle entrée. Ensuite, elle associe les codes Formacodes à la ligne de registre donnée.

    Args:
        session (sqlalchemy.orm.Session): La session SQLAlchemy utilisée pour les opérations de base de données.
        ligne_registre (Registres): L'objet de registre auquel les codes Formacodes seront associés.
        entry (dict): Les données de l'entrée JSON contenant les informations Formacodes.

    Raises:
        Exception: Relève toutes les exceptions rencontrées lors de la gestion de la session de base de données.
    """
    
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

