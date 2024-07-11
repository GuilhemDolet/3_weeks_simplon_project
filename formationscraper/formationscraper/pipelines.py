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
        # Insérer les données dans la base de données :
        # - règle pour vérifier l'existence de l'entité dans la table correspondante
        # - ajout de l'entité

        #table formationsimplon

        # existing_formation = self.session.query(FormationsSimplon).filter_by(id_formation_unique=item['id_formation_unique']).first()
        # if existing_formation is not None :
        #     formation=existing_formation
        # else : 
        formation=FormationsSimplon(formation_id=item['formation_id'], formation_intitule = item['formation_intitule'], formation_rncp = item['formation_rncp'], formation_rs = item['formation_rs'], formation_reussite = item['formation_reussite'], session_sous_intitule = item['session_sous_intitule'], session_distanciel = item['session_distanciel'], session_alternance = item['session_alternance'], session_date_limite = item['session_date_limite'], session_date_debut = ['session_date_debut'], session_lieu = ['session_lieu'], session_duree = ['session_duree'], session_niveau = ['session_niveau'], session_region = ['session_region'])
        self.session.add(formation)
        self.session.commit()

    def close_spider(self, spider):
        # Fermer la connexion à la base de données
        self.session.close() #
    
class FormationscraperPipeline:
        
        def process_item(self, item, spider): # méthode qui fait appel à une autre méthode
            self.cleaned_intitule(item) # appel de chaque méthode
            self.cleaned_lieu(item)
            self.cleaned_debut(item)
            self.cleaned_duree(item)
            self.cleaned_niveau(item)
            self.cleaned_region(item)
            return item
        
###### nettoyage intitulé (saut de ligne)
        def cleaned_intitule(self, item): 
            adapter = ItemAdapter(item)
            intitule_raw = adapter.get('formation_intitule')
            intitule_cleaned = intitule_raw.strip()
            adapter['formation_intitule'] = str(intitule_cleaned)
            return item
        
        def cleaned_lieu(self, item): 
            print("lancement clean_lieu")
            adapter = ItemAdapter(item)
            lieu_raw = adapter.get('session_lieu')
            lieu_raw = " ".join(lieu_raw)
            lieu_raw = lieu_raw.strip()
            lieu_raw = lieu_raw.replace('\n', '')
            # lieu_cleaned = (' '.join(lieu_raw)).strip().replace('\n', '')
            adapter['session_lieu'] = lieu_raw
            return item
                
        def cleaned_debut(self, item): 
            adapter = ItemAdapter(item)
            debut_raw = adapter.get('session_date_debut')            
            debut_cleaned = ' '.join(debut_raw).strip().replace('\n', '')
            adapter['session_date_debut'] = debut_cleaned
            return item
        
        def cleaned_duree(self, item): 
            adapter = ItemAdapter(item)
            duree_raw = adapter.get('session_duree')
            duree_cleaned = ' '.join(duree_raw).strip().replace('\n', '')
            adapter['session_duree'] = str(duree_cleaned)
            return item
        
        def cleaned_niveau(self, item): 
            adapter = ItemAdapter(item)
            niveau_raw = adapter.get('session_niveau')
            niveau_cleaned = ' '.join(niveau_raw).strip().replace('\n', '')
            adapter['session_niveau'] = str(niveau_cleaned)
            return item
        
        def cleaned_region(self, item): 
            adapter = ItemAdapter(item)
            region_raw = adapter.get('session_region')
            region_cleaned = ' '.join(region_raw).strip().replace('\n', '')
            adapter['session_region'] = str(region_cleaned)
            return item

###### nettoyage date (formatage date)
#         def cleaned_date(self, item): 
#             adapter = ItemAdapter(item)
#             annee_raw = adapter.get('annee')
#             annee_cleaned = annee_raw.strip()
#             #annee_cleaned = dateparser.parse(annee_cleaned, date_formats=['%d %B %Y'])
#             adapter['annee'] = str(annee_cleaned)
#             return item



#         def cleaned_genre(self, item) :
#             adapter = ItemAdapter(item)
#             genre_raw = adapter.get('genre')
#             genre_cleaned = ', '.join(genre_raw)   
#             adapter['genre'] = genre_cleaned
#             return item
            
#         def cleaned_boxoffice(self, item) :
#             adapter = ItemAdapter(item)
#             boxoff = adapter.get('boxofficefr')
#             if boxoff is not None:
#                 cleanbox = boxoff.strip().replace(" ","").replace("entrées","") # enleve l'espace et l'espace et entrées
#                 adapter['boxofficefr'] = int(cleanbox)
#             else:
#                 adapter['boxofficefr'] = 0
#             return item
        
#         def cleaned_pays(self, item) :
#             adapter = ItemAdapter(item)
#             pays_cleaned = adapter.get('pays')
#             if pays_cleaned is None:
#                 pays_cleaned = "N/C"
#             else :
#                 pays_cleaned = pays_cleaned.strip()
#             adapter['pays'] = str(pays_cleaned)
#             return item
        
#         def cleaned_acteurs(self, item) : 
#             adapter = ItemAdapter(item)
#             acteurs_raw = adapter.get('acteurs')
#             if acteurs_raw is None:
#                 acteurs_cleaned = "N/C"
#             else :
#                 if isinstance(acteurs_raw, list):
#                     acteurs_cleaned =  ', '.join(acteurs_raw)  
#                     acteurs_cleaned = acteurs_cleaned.strip()
#                 else : 
#                     acteurs_cleaned = "N/C" 
#             adapter['acteurs'] = str(acteurs_cleaned)
#             return item
        
#         def cleaned_scorespectateurs(self, item) : 
#             adapter = ItemAdapter(item)
#             scorespectateurs_raw = adapter.get('scorespectateurs')
#             if scorespectateurs_raw is not None:
#                 scorespectateurs_cleaned = scorespectateurs_raw.replace(",",".")
#             else : 
#                 scorespectateurs_cleaned = None
#             adapter['scorespectateurs'] = scorespectateurs_cleaned
#             return item
        
#         def cleaned_scorepresse(self, item) : 
#             adapter = ItemAdapter(item)
#             scorepresse_raw = adapter.get('scorepresse')
#             if scorepresse_raw is not None:
#                 scorepresse_cleaned = scorepresse_raw.replace(",",".")
#             else : 
#                 scorepresse_cleaned = None
#             adapter['scorepresse'] = scorepresse_cleaned
#             return item  
        