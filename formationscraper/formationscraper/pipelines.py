# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import sqlalchemy, re, datetime, dotenv, os, time
from sqlalchemy.exc import OperationalError
from sqlalchemy.exc import OperationalError
from formationscraper.orm import SessionLocal, session
from formationscraper.models import FormationsSimplon

###########################################################################################################################################################
###########################################################################################################################################################

# PIPELINE FORMATIONS :

###########################################################################################################################################################
###########################################################################################################################################################
class DatabasePipelineFormations :

    def open_spider(self, spider):
        # Se connecter à la base de données
        # Créer la table si elle n'existe pas
       
       ##### créer une connexion à la bdd postgre
       from formationscraper.orm import session
       self.session=session

    def process_item(self, item, spider):
        print(f" Processing item:{item}")
        # Insérer les données dans la base de données :
        # - règle pour vérifier l'existence de l'entité dans la table correspondante
        # - ajout de l'entité

        #table formationsimplon

        # existing_formation = self.session.query(FormationsSimplon).filter_by(id_formation_unique=item['id_formation_unique']).first()
        # if existing_formation is not None :
        #     formation=existing_formation
        # else : 
    
        # Ajouter d'autres étapes de nettoyage si nécessaire

        formation=FormationsSimplon(formation_id=item['formation_id'],
                                    formation_intitule=item['formation_intitule'],
                                    formation_rncp=item['formation_rncp'],
                                    formation_rs=item['formation_rs'],
                                    formation_reussite= item['formation_reussite'],
                                    session_sous_intitule=item['session_sous_intitule'],
                                    session_distanciel=item['session_distanciel'],
                                    session_alternance=item['session_alternance'],
                                    session_date_limite=item['session_date_limite'],
                                    session_date_debut=item['session_date_debut'],
                                    session_duree=item['session_duree'],
                                    session_lieu=item['session_lieu'],
                                    session_niveau=item['session_niveau'],
                                    session_region=item['session_region'])
        self.session.add(formation)
        self.session.commit()
        print(f"inserted formation with ID : {item['formation_id']}")
        return item

    def close_spider(self, spider):
        # Fermer la connexion à la base de données
        self.session.close() #
    
class FormationscraperPipeline:
        
        def process_item(self, item, spider): # méthode qui fait appel à une autre méthode
            # item = self.cleaned_intitule(item) # appel de chaque méthode
            # item = self.cleaned_lieu(item)
            # item = self.cleaned_debut(item)
            # item = self.cleaned_duree(item)
            # item = self.cleaned_niveau(item)
            # item = self.cleaned_region(item)
            # return item

            item['formation_intitule'] = self.clean_text(item.get('formation_intitule'))
            item['formation_rncp'] = self.clean_text(item.get('formation_rncp'))
            item['formation_rs'] = self.clean_text(item.get('formation_rs'))
            item['formation_reussite'] = self.clean_text(item.get('formation_reussite'))
            item['session_date_limite'] = self.clean_text(item.get('session_date_limite'))
            item['session_date_debut'] = self.clean_text_list(item.get('session_date_debut'))
            item['session_duree'] = self.clean_text_list(item.get('session_duree'))
            item['session_lieu'] = self.clean_text_list(item.get('session_lieu'))
            item['session_region'] = self.clean_text_list(item.get('session_region'))
            item['session_niveau'] = self.clean_text_list(item.get('session_niveau'))
            return item
        



        def clean_text(self, text):
            if text:
                # Remplacer les multiples espaces et virgules par un seul espace
                text = re.sub(r'[,\s]+', ' ', text).strip()
            return text

        def clean_text_list(self, text_list):
            if text_list:
                # Enlever les valeurs vides et nettoyer chaque texte dans la liste
                cleaned_list = [self.clean_text(text) for text in text_list if text.strip()]
                # Joindre les éléments de la liste en une seule chaîne de caractères
                return ', '.join(cleaned_list)
            return ''


###### nettoyage intitulé (saut de ligne)
        # def cleaned_intitule(self, item): 
        #     adapter = ItemAdapter(item)
        #     intitule_raw = adapter.get('formation_intitule')
        #     intitule_cleaned = intitule_raw.strip()
        #     adapter['formation_intitule'] = str(intitule_cleaned)
        #     return item
        
        # def cleaned_lieu(self, item): 
        #     print("lancement clean_lieu")
        #     # adapter = ItemAdapter(item)
        #     # lieu_raw = adapter.get('session_lieu')
        #     # lieu_raw = " ".join(lieu_raw)
        #     # lieu_raw = lieu_raw.strip()
        #     # lieu_raw = lieu_raw.replace('\n', '')
        #     # # lieu_cleaned = (' '.join(lieu_raw)).strip().replace('\n', '')
        #     # adapter['session_lieu'] = lieu_raw
        #     adapter = ItemAdapter(item)
        #     lieu_raw = adapter.get('session_lieu', [])
        #     if lieu_raw:
        #         lieu_raw = " ".join(lieu_raw).strip().replace('\n', '')
        #     else:
        #         lieu_raw = ''
        #     adapter['session_lieu'] = str(lieu_raw)
        #     return item
        # print("fin clean_lieu")
        # print("lieu_cleaned")
                
        # def cleaned_debut(self, item): 
        #     adapter = ItemAdapter(item)
        #     debut_raw = adapter.get('session_date_debut')            
        #     debut_cleaned = ' '.join(debut_raw).strip().replace('\n', '')
        #     adapter['session_date_debut'] = debut_cleaned
        #     return item
        
        # def cleaned_duree(self, item): 
        #     adapter = ItemAdapter(item)
        #     duree_raw = adapter.get('session_duree')
        #     duree_cleaned = ' '.join(duree_raw).strip().replace('\n', '')
        #     adapter['session_duree'] = str(duree_cleaned)
        #     return item
        
        # def cleaned_niveau(self, item): 
        #     adapter = ItemAdapter(item)
        #     niveau_raw = adapter.get('session_niveau')
        #     niveau_cleaned = ' '.join(niveau_raw).strip().replace('\n', '')
        #     adapter['session_niveau'] = str(niveau_cleaned)
        #     return item
        
        # def cleaned_region(self, item): 
        #     adapter = ItemAdapter(item)
        #     region_raw = adapter.get('session_region')
        #     if region_raw:
        #         region_cleaned = " ".join(region_raw).strip().replace('\n', '')
        #     else : 
        #         region_cleaned=''
        #     adapter['session_region'] = str(region_cleaned)
        #     return item

        
        # def cleaned_region(self, item): 
        #     adapter = ItemAdapter(item)
        #     region_raw = adapter.get('session_region')
        #     if region_raw is None:
        #         region_cleaned = None
        #     else :
        #         if isinstance(region_raw, list):
        #             region_cleaned =  ', '.join(region_raw)  
        #             region_cleaned = region_cleaned.strip()
        #         else : 
        #             region_cleaned = "N/C" 
        #     adapter['session_region'] = str(region_cleaned)
        #     return item




###### nettoyage date (formatage date)
#         def cleaned_date(self, item): 
#             adapter = ItemAdapter(item)
#             annee_raw = adapter.get('annee')
#             annee_cleaned = annee_raw.strip()
#             #annee_cleaned = dateparser.parse(annee_cleaned, date_formats=['%d %B %Y'])
#             adapter['annee'] = str(annee_cleaned)
#             return item