# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class FormationSimplonItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    intitule_formation = scrapy.Field()
    categorie = scrapy.Field()
    code_rncp = scrapy.Field()
    code_rs = scrapy.Field()
    voie_acces = scrapy.Field()
    date_limite = scrapy.Field()
    agence = scrapy.Field()
    distanciel = scrapy.Field()
    alternance = scrapy.Field()
    echelle_duree = scrapy.Field()    
    date_debut = scrapy.Field()
    date_fin = scrapy.Field()

    titre = scrapy.Field()
    etat_registre = scrapy.Field()
    formacode_code = scrapy.Field()
    formacode_nom = scrapy.Field()
    niveau_sortie = scrapy.Field()
    certificateur_nom = scrapy.Field()
    siret = scrapy.Field()

