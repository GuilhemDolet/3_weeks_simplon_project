from itemadapter import ItemAdapter
import re
import dateparser
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
# from .models import Nsf
# from .models import Formacodes
from .models import AssFormationsRegistres
# from .models import AssFormationsExtRegistres
# from .models import AssRegistresNsf
# from .models import AssRegistresFormacodes
# from .models import AssRegionsFormationsExt


class FormationSimplonPipeline:
    def process_item(self, item, spider):
        # items de la page formation
        item = self.clean_categorie(item)
        item = self.clean_rncp(item)
        item = self.clean_rs(item)
        item = self.clean_voie_acces(item)

        # items de la page session
        item = self.clean_date_limite(item)
        item = self.clean_region(item)
        item = self.clean_distanciel(item)
        item = self.clean_alternance(item)
        item = self.clean_echelle_duree(item)
        item = self.clean_date_debut(item)
        item = self.clean_date_fin(item)

        # item des pages francecompetences
        item = self.clean_nsf_code_rncp(item)
        item = self.clean_nsf_nom_rncp(item)
        item = self.clean_formacode_code_rncp(item)
        item = self.clean_formacode_nom_rncp(item)
        item = self.clean_niveau_sortie_rncp(item)
        item = self.clean_certificateur_nom_rncp(item)
        item = self.clean_siret_rncp(item)

        item = self.clean_nsf_code_rs(item)
        item = self.clean_nsf_nom_rs(item)
        item = self.clean_formacode_code_rs(item)
        item = self.clean_formacode_nom_rs(item)
        item = self.clean_certificateur_nom_rs(item)
        item = self.clean_siret_rs(item)

        return item
    
    # Nettoyage pages "découvrez la formation"
    def clean_categorie(self, item):
        adapter = ItemAdapter(item)
        categorie = adapter.get("categorie")
        if categorie:
            categorie = categorie.strip()
        adapter["categorie"] = categorie
        return item
    
    def clean_rncp(self, item):
        adapter = ItemAdapter(item)
        rncp = adapter.get("code_rncp")
        if rncp is not None:
            rncp = re.findall(r'(\d+)', rncp)[0]
            adapter["code_rncp"] = rncp
        return item
    
    def clean_rs(self, item):
        adapter = ItemAdapter(item)
        rs = adapter.get("code_rs")
        if rs is not None:
            rs = re.findall(r'(\d+)', rs)[0]
            adapter["code_rs"] = rs
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
                date_limite = dateparser.parse(date_limite).date()
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
        distanciel = adapter.get(item)
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
                date_debut = dateparser.parse(date_debut).date()
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
                date_fin = dateparser.parse(date_fin).date()
                adapter["date_fin"] = date_fin
            else:
                adapter["date_fin"] = None
        return item

    # Nettoyage pages francecompetences    
    def clean_nsf_code_rncp(self, item):
        adapter = ItemAdapter(item)
        nsf_code_rncp = adapter.get("nsf_code_rncp")
        if nsf_code_rncp:
            if nsf_code_rncp != []:
                for i in range(len(nsf_code_rncp)):
                    nsf_code_rncp[i] = nsf_code_rncp[i].replace(":", "")
                    nsf_code_rncp[i] = nsf_code_rncp[i].strip()
                adapter["nsf_code_rncp"] = nsf_code_rncp
        return item
    
    def clean_nsf_nom_rncp(self, item):
        adapter = ItemAdapter(item)
        nsf_nom_rncp = adapter.get("nsf_nom_rncp")
        nsf_nom_temp = []
        if nsf_nom_rncp:
            if nsf_nom_rncp != []:
                for i in range(len(nsf_nom_rncp)):
                    nsf_nom_rncp[i] = nsf_nom_rncp[i].strip()
                    if nsf_nom_rncp[i]:
                        nsf_nom_temp.append(nsf_nom_rncp[i])
                adapter["nsf_nom_rncp"] = nsf_nom_temp
        return item
    
    def clean_formacode_code_rncp(self, item):
        adapter = ItemAdapter(item)
        formacode_code_rncp = adapter.get("formacode_code_rncp")
        if formacode_code_rncp:
            if formacode_code_rncp != []:
                for i in range(len(formacode_code_rncp)):
                    formacode_code_rncp[i] = re.findall(r'(\d+)',formacode_code_rncp[i])[0]
                adapter["formacode_code_rncp"] = formacode_code_rncp
        return item
    
    def clean_formacode_nom_rncp(self, item):
        adapter = ItemAdapter(item)
        formacode_nom_rncp = adapter.get("formacode_nom_rncp")
        formacode_nom_temp = []
        if formacode_nom_rncp:
            if formacode_nom_rncp != []:
                for i in range(len(formacode_nom_rncp)):
                    formacode_nom_rncp[i] = formacode_nom_rncp[i].strip()
                    if formacode_nom_rncp[i]:
                        formacode_nom_temp.append(formacode_nom_rncp[i])
                adapter["formacode_nom_rncp"] = formacode_nom_temp
        return item
    
    def clean_niveau_sortie_rncp(self, item):
        adapter = ItemAdapter(item)
        niveau_sortie_rncp = adapter.get("niveau_sortie_rncp")
        if niveau_sortie_rncp is not None:
            niveau_sortie_rncp = niveau_sortie_rncp.strip()
            adapter["niveau_sortie_rncp"] = niveau_sortie_rncp
        return item
    
    def clean_certificateur_nom_rncp(self, item):
        adapter = ItemAdapter(item)
        certificateur_nom_rncp = adapter.get("certificateur_nom_rncp")
        if certificateur_nom_rncp is not None:
            certificateur_nom_rncp = certificateur_nom_rncp.strip()
            adapter["certificateur_nom_rncp"] = certificateur_nom_rncp
        return item
    
    def clean_siret_rncp(self, item):
        adapter = ItemAdapter(item)
        siret_rncp = adapter.get("siret_rncp")
        if siret_rncp:
            siret_rncp = siret_rncp.strip()
            siret_rncp = int(siret_rncp)
            adapter["siret_rncp"] = siret_rncp
        return item
    
    def clean_nsf_code_rs(self, item):
        adapter = ItemAdapter(item)
        nsf_code_rs = adapter.get("nsf_code_rs")
        if nsf_code_rs:
            if nsf_code_rs != []:
                for i in range(len(nsf_code_rs)):
                    nsf_code_rs[i] = nsf_code_rs[i].replace(":", "")
                    nsf_code_rs[i] = nsf_code_rs[i].strip()
                adapter["nsf_code_rs"] = nsf_code_rs
        return item
    
    def clean_nsf_nom_rs(self, item):
        adapter = ItemAdapter(item)
        nsf_nom = adapter.get("nsf_nom_rs")
        nsf_nom_temp = []
        if nsf_nom:
            if nsf_nom != []:
                for i in range(len(nsf_nom)):
                    nsf_nom[i] = nsf_nom[i].strip()
                    if nsf_nom[i]:
                        nsf_nom_temp.append(nsf_nom[i])
                adapter["nsf_nom_rs"] = nsf_nom_temp
        return item

    def clean_formacode_code_rs(self, item):
        adapter = ItemAdapter(item)
        formacode_code = adapter.get("formacode_code_rs")
        if formacode_code:
            if formacode_code != []:
                for i in range(len(formacode_code)):
                    formacode_code[i] = re.findall(r'(\d+)',formacode_code[i])[0]
                adapter["formacode_code_rs"] = formacode_code
        return item
    
    def clean_formacode_nom_rs(self, item):
        adapter = ItemAdapter(item)
        formacode_nom = adapter.get("formacode_nom_rs")
        formacode_nom_temp = []
        if formacode_nom:
            if formacode_nom != []:
                for i in range(len(formacode_nom)):
                    formacode_nom[i] = formacode_nom[i].strip()
                    if formacode_nom[i]:
                        formacode_nom_temp.append(formacode_nom[i])
                adapter["formacode_nom_rs"] = formacode_nom_temp
        return item
    
    def clean_certificateur_nom_rs(self, item):
        adapter = ItemAdapter(item)
        certificateur_nom = adapter.get("certificateur_nom_rs")
        if certificateur_nom is not None:
            certificateur_nom = certificateur_nom.strip()
            adapter["certificateur_nom_rs"] = certificateur_nom
        return item
    
    def clean_siret_rs(self, item):
        adapter = ItemAdapter(item)
        siret = adapter.get("siret_rs")
        if siret:
            siret = siret.strip()
            siret = int(siret)
            adapter["siret_rs"] = siret
        return item
    
class Database:
    def __init__(self):
        engine = create_engine('sqlite:///mydatabase.db')
        Base.metadata.create_all(engine)
        Session = sessionmaker(bind=engine)
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
        type = item.get("rncp_url", None)
        if type:
            type = re.findall(r'/([a-zA-Z]+)/\d+', type)[0]
            type = type.upper()
        else:
            type = None

        code_registre_test = item.get("code_rncp", None)
        titre_registre_test = item.get("titre_rncp", None)
        statut_test = item.get("statut_registre_rncp", None)
        niveau_test = item.get("niveau_sortie_rncp", None)
        url_test = item.get("rncp_url", None)
        existing_registre = self.session.query(Registres).filter_by(type_registre=type, code_registre=code_registre_test).first()
        if existing_registre:
            registre = existing_registre
        elif type is not None and code_registre_test is not None:
            registre = Registres(type_registre=type, 
                        code_registre=titre_registre_test,
                        titre_registre=titre_registre_test,
                        statut=statut_test,
                        niveau_sortie=niveau_test,
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
        self.session.commit()

        return item

    def close_spider(self, spider):
        self.session.close()
       