from itemadapter import ItemAdapter
import re
import dateparser, datetime
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy import create_engine
from scrapy.exceptions import DropItem
from sqlalchemy.exc import IntegrityError 
from .models import Base
# from .models import FormationsSimplon, FormationsExt, SessionsFormations, Regions, Registres, Nsf, Formacodes
# from .models import AssFormationsRegistres, AssFormationsExtRegistres, AssRegistresNsf, AssRegistresFormacodes, AssRegionsFormationsExt
from .models import FormationsSimplon
from .models import SessionsFormations
# from .models import FormationsExt
from .models import Regions
from .models import Registres
from .models import Nsf
from .models import Formacodes
from .models import AssFormationsRegistres
# from .models import AssFormationsExtRegistres
from .models import AssRegistresNsf
from .models import AssRegistresFormacodes
# from .models import AssRegionsFormationsExt
# from .models import Session
# from .create_db import Session

# pipeline de nettoyage
class FormationSimplonPipeline:
    def process_item(self, item, spider):
        # items de la page formation
        item = self.clean_categorie(item)   
        item = self.clean_voie_acces(item)

        # items de la page session
        item = self.clean_date_limite(item)
        item = self.clean_region(item)
        item = self.clean_distanciel(item)
        item = self.clean_alternance(item)
        item = self.clean_echelle_duree(item)
        item = self.clean_date_debut(item)
        item = self.clean_date_fin(item)

        # items des pages francecompetences
        item = self.clean_type_registre(item)
        item = self.clean_code_registre(item)
        item = self.clean_code_nsf(item)
        item = self.clean_nom_nsf(item)
        item = self.clean_code_formacode(item)
        item = self.clean_nom_formacode(item)
        item = self.clean_niveau_sortie(item)
        item = self.clean_certificateur(item)
        item = self.clean_siret(item)

        return item
    
    # Nettoyage pages "découvrez la formation"
    def clean_categorie(self, item):
        adapter = ItemAdapter(item)
        categorie = adapter.get("categorie")
        if categorie:
            categorie = categorie.strip()
        adapter["categorie"] = categorie
        return item
    
    def clean_voie_acces(self, item):
        adapter = ItemAdapter(item)
        voie_acces = adapter.get("voie_acces")
        voie_temp = []
        if voie_acces:
            if voie_acces != []:
                for i in range(len(voie_acces)):
                    voie_acces[i] = voie_acces[i].replace(";","")
                    voie_acces[i] = voie_acces[i].strip()
                    if voie_acces[i]:
                        voie_temp.append(voie_acces[i])
                adapter["voie_acces"] = voie_temp
        return item
   
    # Nettoyage pages sessions/session
    def clean_date_limite(self, item):
        adapter = ItemAdapter(item)
        date_limite = adapter.get("date_limite")
        if date_limite:
            if date_limite != []:
                date_limite = ";".join(date_limite)
                date_limite = re.findall(r'(\d+)', date_limite)
                date_limite = "/".join(date_limite)
                date_limite = dateparser.parse(date_limite, date_formats=['%d/%m/%Y']).date()
                adapter["date_limite"] = date_limite
        return item
    
    def clean_region(self, item):
        adapter = ItemAdapter(item)
        region = adapter.get("region")
        region_temp = []
        if region:
            if region != []:
                for i in range(len(region)):
                    region[i] = region[i].strip()
                    if region[i]:
                        region_temp.append(region[i])
                adapter["region"] = region_temp[0]
        return item

    def clean_distanciel(self, item):
        adapter = ItemAdapter(item)
        distanciel = adapter.get("distanciel")
        if distanciel is not None:
            distanciel = True
        else:
            distanciel= False
        adapter["distanciel"] = distanciel
        return item
    
    def clean_alternance(self, item):
        adapter = ItemAdapter(item)
        alternance = adapter.get("alternance")
        if alternance is not None:
            alternance = True
        else:
            alternance = False
        adapter["alternance"] = alternance
        return item

    def clean_echelle_duree(self, item):
        adapter = ItemAdapter(item)
        echelle_duree = adapter.get("echelle_duree")
        if echelle_duree:
            for i in range(len(echelle_duree)):
                echelle_duree[i] = echelle_duree[i].strip()
            echelle_duree = "".join(echelle_duree)
        else:
            echelle_duree = None
        adapter["echelle_duree"] = echelle_duree
        return item

    def clean_date_debut(self, item):
        adapter = ItemAdapter(item)
        date_debut = adapter.get("date_debut")
        if date_debut:
            if date_debut != []:
                date_debut = "".join(date_debut)
                date_debut = re.findall(r'\d+/?', date_debut)
                date_debut = "".join(date_debut)
                date_debut = dateparser.parse(date_debut, date_formats=['%d/%m/%Y']).date()
                adapter["date_debut"] = date_debut
        return item
    
    def clean_date_fin(self, item):
        adapter = ItemAdapter(item)
        date_fin = adapter.get("date_fin")
        if date_fin is not None:
            date_fin = date_fin.replace("\xa0"," ")\
                .replace("Janvier", "01").replace("janvier","01")\
                .replace("Février", "02").replace("février", "02")\
                .replace("Mars", "03").replace("mars", "03")\
                .replace("Avril", "04").replace("avril", "04")\
                .replace("Mai", "05").replace("mai", "05")\
                .replace("Juin", "06").replace("juin", "06")\
                .replace("Juillet","07").replace("juillet", "07")\
                .replace("Août","08").replace("août", "08")\
                .replace("Septembre","09").replace("septembre", "09")\
                .replace("Octobre","10").replace("octobre", "10")\
                .replace("Novembre","11").replace("novembre", "11")\
                .replace("Décembre","12").replace("décembre", "12")
            try:
                date_fin = re.findall(r"(au .+\d{2,4})(?! ?[hH])",date_fin)[0]
            except IndexError:
                pass
            date_fin = re.findall(r'(\d+)', date_fin)
            date_fin = "".join(date_fin)
            if len(date_fin)>6:
                date_fin = f"{date_fin[:-6]}/{date_fin[-6:-4]}/{date_fin[-4:]}"
                date_fin = dateparser.parse(date_fin, date_formats=['%d/%m/%Y']).date()
                adapter["date_fin"] = date_fin
            else:
                adapter["date_fin"] = None
        return item

    # Nettoyage pages francecompetences
    def clean_type_registre(self, item):
        adapter = ItemAdapter(item)
        type_registre = adapter.get("type_registre")
        if type_registre:
            type_registre = re.findall(r'/([a-zA-Z]+)/\d+', type_registre)[0]
            type_registre = type_registre.upper()
        else:
            type_registre = None
        adapter["type_registre"] = type_registre
        return item 
    
    def clean_code_registre(self, item):
        adapter = ItemAdapter(item)
        code_registre = adapter.get("code_registre")
        if code_registre is not None:
            code_registre = re.findall(r'(\d+)', code_registre)[0]
            adapter["code_registre"] = code_registre
        return item    
        
    def clean_code_nsf(self, item):
        adapter = ItemAdapter(item)
        code_nsf = adapter.get("code_nsf")
        if code_nsf:
            if code_nsf != []:
                for i in range(len(code_nsf)):
                    code_nsf[i] = code_nsf[i].replace(":", "")
                    code_nsf[i] = code_nsf[i].strip()
                adapter["code_nsf"] = code_nsf
        return item
    
    def clean_nom_nsf(self, item):
        adapter = ItemAdapter(item)
        nom_nsf = adapter.get("nom_nsf")
        nom_nsf_temp = []
        if nom_nsf:
            if nom_nsf != []:
                for i in range(len(nom_nsf)):
                    nom_nsf[i] = nom_nsf[i].strip()
                    if nom_nsf[i]:
                        nom_nsf_temp.append(nom_nsf[i])
                adapter["nom_nsf"] = nom_nsf_temp
        return item
    
    def clean_code_formacode(self, item):
        adapter = ItemAdapter(item)
        code_formacode = adapter.get("code_formacode")
        if code_formacode:
            if code_formacode != []:
                for i in range(len(code_formacode)):
                    code_formacode[i] = re.findall(r'(\d+)',code_formacode[i])[0]
                adapter["code_formacode"] = code_formacode
        return item
    
    def clean_nom_formacode(self, item):
        adapter = ItemAdapter(item)
        nom_formacode = adapter.get("nom_formacode")
        nom_formacode_temp = []
        if nom_formacode:
            if nom_formacode != []:
                for i in range(len(nom_formacode)):
                    nom_formacode[i] = nom_formacode[i].strip()
                    if nom_formacode[i]:
                        nom_formacode_temp.append(nom_formacode[i])
                adapter["nom_formacode"] = nom_formacode_temp
        return item
    
    def clean_niveau_sortie(self, item):
        adapter = ItemAdapter(item)
        niveau_sortie = adapter.get("niveau_sortie")
        if niveau_sortie is not None:
            niveau_sortie = niveau_sortie.strip()
            adapter["niveau_sortie"] = niveau_sortie
        return item
    
    def clean_certificateur(self, item):
        adapter = ItemAdapter(item)
        certificateur = adapter.get("certificateur")
        if certificateur is not None:
            certificateur = certificateur.strip()
            adapter["certificateur"] = certificateur
        return item
    
    def clean_siret(self, item):
        adapter = ItemAdapter(item)
        siret = adapter.get("siret")
        if siret:
            siret = siret.strip()
            siret = int(siret)
            adapter["siret"] = siret
        return item

# pipeline de mise en base de données     
engine = create_engine('sqlite:///mydatabase.db')
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)

class Database:
    def __init__(self):
        
        self.session = Session()
        
    def process_item(self, item, spider):
        # table formations_simplon
        intitule_test = item.get("intitule_formation", None)
        categorie_test = item.get("categorie", None)
        existing_formation = self.session.query(FormationsSimplon).filter_by(intitule_formation=intitule_test, categorie=categorie_test).first()
        if existing_formation:
            formation = existing_formation
        elif intitule_test is not None and categorie_test is not None:
            formation = FormationsSimplon(intitule_formation=intitule_test, categorie=categorie_test)
            self.session.add(formation)
            self.session.flush()
            # self.session.commit()

        # table regions 
        region_test = item.get("region", None)
        existing_region = self.session.query(Regions).filter_by(region=region_test).first()
        if existing_region:
            region = existing_region
        elif region_test is not None:
            region = Regions(region=region_test)
            self.session.add(region)
            self.session.flush()
            # self.session.commit()

        # table sessions
        agence_test = item.get("agence", None)         
        distanciel_test = item.get("distanciel", None)
        alternance_test = item.get("alternance", None)
        echelle_test = item.get("echelle_duree", None)
        date_limite_test = item.get("date_limite", None)
        date_debut_test = item.get("date_debut", None)
        date_fin_test = item.get("date_fin", None)
        if region_test is not None:
            existing_session = self.session.query(SessionsFormations).filter_by(agence=agence_test,
                        distanciel=distanciel_test,
                        alternance=alternance_test,
                        echelle_duree=echelle_test,
                        date_limite=date_limite_test,
                        date_debut=date_debut_test,
                        date_fin=date_fin_test,
                        id_formation=formation.id_formation,
                        region=region.region).first()
        else:
            existing_session = self.session.query(SessionsFormations).filter_by(agence=agence_test,
                        distanciel=distanciel_test,
                        alternance=alternance_test,
                        echelle_duree=echelle_test,
                        date_limite=date_limite_test,
                        date_debut=date_debut_test,
                        date_fin=date_fin_test,
                        id_formation=formation.id_formation).first()

        if existing_session:
            session_formation = existing_session
        elif (agence_test, echelle_test, date_limite_test, date_debut_test, date_fin_test) != (None,None,None,None,None):
            session_formation = SessionsFormations(agence=agence_test,
                distanciel=distanciel_test,
                alternance=alternance_test,
                echelle_duree=echelle_test,
                date_limite=date_limite_test,
                date_debut=date_debut_test,
                date_fin=date_fin_test,
                id_formation=formation.id_formation,
                region=region.region)
               
            self.session.add(session_formation)
            self.session.flush()
            # self.session.commit()
       
        # table registres
        type_registre_test = item.get("type_registre", None)
        code_registre_test = item.get("code_registre", None)
        titre_registre_test = item.get("titre_registre", None)
        statut_test = item.get("statut_registre", None)
        niveau_sortie_test = item.get("niveau_sortie", None)
        url_test = item.get("url", None)
        existing_registre = self.session.query(Registres).filter_by(type_registre=type_registre_test, code_registre=code_registre_test).first()
        if existing_registre:
            registre = existing_registre
        elif type_registre_test is not None and code_registre_test is not None:
            registre = Registres(type_registre=type_registre_test, 
                        code_registre=code_registre_test,
                        titre_registre=titre_registre_test,
                        statut_registre=statut_test,
                        niveau_sortie=niveau_sortie_test,
                        url=url_test)
            self.session.add(registre)
            self.session.flush()
            # self.session.commit()

        if code_registre_test:
            existing_formation_registre = self.session.query(AssFormationsRegistres).filter_by(id_formation=formation.id_formation,
                                         type_registre=registre.type_registre, 
                                         code_registre=registre.code_registre).first()
            if not existing_formation_registre:
                registre.rel_formation_registre.append(formation)

        # table formacodes
        codes_formacodes = item.get("code_formacode", None)
        noms_formacodes = item.get("nom_formacode", None)
        if codes_formacodes and codes_formacodes!= []:
            for i in range(len(codes_formacodes)):
                existing_formacode = self.session.query(Formacodes).filter_by(code_formacode=codes_formacodes[i]).first()
                if existing_formacode:
                    formacode = existing_formacode
                elif codes_formacodes[i]:
                    formacode = Formacodes(code_formacode=codes_formacodes[i],
                                           nom_formacode=noms_formacodes[i])
                    self.session.add(formacode)
                    self.session.flush()

                # table ass_registres_formacodes
                if code_registre_test:
                    existing_registre_formacode = self.session.query(AssRegistresFormacodes).filter_by(code_formacode=formacode.code_formacode,
                                                type_registre=registre.type_registre, 
                                                code_registre=registre.code_registre).first()
                    if not existing_registre_formacode:
                        registre.rel_formacode_registre.append(formacode)

        # table nsf
        codes_nsf = item.get("code_nsf", None)
        noms_nsf = item.get("nom_nsf", None)
        if codes_nsf and codes_nsf!= []:
            for i in range(len(codes_nsf)):
                existing_nsf = self.session.query(Nsf).filter_by(code_nsf=codes_nsf[i]).first()
                if existing_nsf:
                    nsf = existing_nsf
                elif codes_nsf[i]:
                    nsf = Nsf(code_nsf=codes_nsf[i], nom_nsf=noms_nsf[i])
                    self.session.add(nsf)
                    self.session.flush()

                # table ass_registres_nsf
                if code_registre_test:
                    existing_registre_nsf = self.session.query(AssRegistresNsf).filter_by(code_nsf=nsf.code_nsf,
                                                type_registre=registre.type_registre, 
                                                code_registre=registre.code_registre).first()
                    if not existing_registre_nsf:
                        registre.rel_nsf_registre.append(nsf)


        self.session.commit()

        return item

    def close_spider(self, spider):
        self.session.close()
       