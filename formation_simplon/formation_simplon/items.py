# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class FormationSimplonItem(scrapy.Item):

    intitule_formation = scrapy.Field()
    categorie = scrapy.Field()
    voie_acces = scrapy.Field()

    agence = scrapy.Field()
    date_limite = scrapy.Field()
    region = scrapy.Field()
    distanciel = scrapy.Field()
    alternance = scrapy.Field()
    echelle_duree = scrapy.Field()    
    date_debut = scrapy.Field()
    date_fin = scrapy.Field()

    type_registre = scrapy.Field()
    code_registre = scrapy.Field()
    titre_registre = scrapy.Field()
    statut_registre = scrapy.Field()
    code_nsf = scrapy.Field()
    nom_nsf = scrapy.Field()
    code_formacode = scrapy.Field()
    nom_formacode = scrapy.Field()
    niveau_sortie = scrapy.Field()
    certificateur = scrapy.Field()
    siret = scrapy.Field()
    url = scrapy.Field()

