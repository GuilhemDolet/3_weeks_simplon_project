from model_bdd.models import Session, FormationsExt, Regions, Registres, Nsf, Formacodes
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
                    session.add(ligne_registre)
                else:
                    ligne_registre = registre_exist
                
                ligne_formation_ext.formation_ext.append(ligne_registre)

                #Remplissage de la table NSF pour un référentiel type RS:
                check_and_load_nsf(session, ligne_registre, entry)

                check_and_load_formacodes(session, ligne_registre, entry)

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
                    session.add(ligne_registre)
                else:
                    ligne_registre = registre_exist

                ligne_formation_ext.formation_ext.append(ligne_registre)

                #Remplissage de la table NSF pour un référentiel type RNCP:
                check_and_load_nsf(session, ligne_registre, entry)

                check_and_load_formacodes(session, ligne_registre, entry)

        session.commit()
    except:
        session.rollback()
        raise
    finally:
        session.close()

def check_and_load_nsf(session, ligne_registre, entry):
    
    # Dictionnaire pour associer les codes NSF aux libellés
    nsf_dict = {
        'code_nsf_1': 'libelle_nsf_1',
        'code_nsf_2': 'libelle_nsf_2',
        'code_nsf_3': 'libelle_nsf_3'
    }
    
    # Obtenir les codes NSF de l'entrée
    nsf_codes = {code: entry.get(code) for code in nsf_dict}

    # Vérifier si les codes NSF existent déjà dans la base de données
    existing_nsfs = {code: session.query(Nsf).filter_by(nsf_code=nsf_code).first() for code, nsf_code in nsf_codes.items()}

    # Pour chaque code NSF, ajouter à la table Nsf si non existant
    for code, nsf_code in nsf_codes.items():
        if nsf_code and existing_nsfs.get(code) is None:
            # Si le code NSF n'existe pas encore, l'ajouter
            ligne_nfs = Nsf(
                nsf_code=nsf_code,
                nsf_nom=entry.get(nsf_dict[code])
            )
            session.add(ligne_nfs)
            session.flush()  # Assurer que l'ID est généré pour l'association

        # Ajouter l'association entre Registre et NSF
        nsf_instance = existing_nsfs.get(code) or session.query(Nsf).filter_by(nsf_code=nsf_code).first()
        if nsf_instance:
            if nsf_instance not in ligne_registre.registres_nsf:
                ligne_registre.registres_nsf.append(nsf_instance)

    # Algo pour vérifier si un code nsf n'est pas déjà dans la table Nsf. 
    # checking_nsfs = ['code_nsf_1', 'code_nsf_2', 'code_nsf_3']
    # result_list = []

    # for nfs in checking_nsfs:
    #     result_list.append(session.query(Nsf).filter_by(nsf_code=entry.get(nfs)).first())
    
    # if all(result is None for result in result_list): # J'utilise la fonction all pour aller vérifier si tout mes éléments de la liste result_list sont None. La fonction all retourne alors True
    #     for nfs in checking_nsfs:
    #         if entry.get(nfs) == entry.get('code_nsf_1'):
    #             ligne_nfs = Nsf(
    #                 nsf_code = entry.get(nfs),
    #                 nsf_nom = entry.get('libelle_nsf_1')
    #             )
    #             #ajout dans la table d'association 
    #             session.add(ligne_nfs)
    #             ligne_registre.registres_nsf.append(ligne_nfs)
                                                    
    #         elif entry.get(nfs) == entry.get('code_nsf_2'):
    #             ligne_nfs = Nsf(
    #                 nsf_code = entry.get(nfs),
    #                 nsf_nom = entry.get('libelle_nsf_2')
    #             )
    #             #ajout dans la table d'association 
    #             session.add(ligne_nfs)
    #             ligne_registre.registres_nsf.append(ligne_nfs)

    #         elif entry.get(nfs) == entry.get('code_nsf_3'):
    #             ligne_nfs = Nsf(
    #                 nsf_code = entry.get(nfs),
    #                 nsf_nom = entry.get('libelle_nsf_3')
    #             )
    #             #ajout dans la table d'association 
    #             session.add(ligne_nfs)
    #             ligne_registre.registres_nsf.append(ligne_nfs)

def check_and_load_formacodes(session, ligne_registre, entry):
    # Liste des clés pour les codes de formacodes
    formacode_keys = ['code_formacode_1', 'code_formacode_2', 'code_formacode_3', 'code_formacode_4', 'code_formacode_5']

    # Obtenir les codes de formacodes de l'entrée
    formacode_codes = [entry.get(key) for key in formacode_keys]

    # Vérifier si les formacodes existent déjà dans la base de données
    existing_formacodes = {formacode_code: session.query(Formacodes).filter_by(formacode_code=formacode_code).first()
                           for formacode_code in formacode_codes if formacode_code}

    # Pour chaque code de formacode, ajouter à la table Formacodes si non existant
    for formacode_code in formacode_codes:
        if formacode_code:
            if existing_formacodes.get(formacode_code) is None:
                # Si le code formacode n'existe pas encore, l'ajouter
                formacode_libelle = entry.get(f'libelle_formacode_{formacode_codes.index(formacode_code) + 1}')
                ligne_formacode = Formacodes(
                    formacode_code=formacode_code,
                    formacode_nom=formacode_libelle
                )
                session.add(ligne_formacode)
                session.flush()  # Assurer que l'ID est généré pour l'association

            # Ajouter l'association entre Registre et Formacode
            formacode_instance = existing_formacodes.get(formacode_code) or session.query(Formacodes).filter_by(formacode_code=formacode_code).first()
            if formacode_instance:
                if formacode_instance not in ligne_registre.registres_formacodes:
                    ligne_registre.registres_formacodes.append(formacode_instance)

load_json_into_databse(Session, data_url)