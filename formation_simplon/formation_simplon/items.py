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
    
    agence = scrapy.Field()
    date_limite = scrapy.Field()
    region = scrapy.Field()
    distanciel = scrapy.Field()
    alternance = scrapy.Field()
    echelle_duree = scrapy.Field()    
    date_debut = scrapy.Field()
    date_fin = scrapy.Field()

    titre = scrapy.Field()
    etat_registre = scrapy.Field()
    nsf_code = scrapy.Field()
    nsf_nom = scrapy.Field()
    formacode_code = scrapy.Field()
    formacode_nom = scrapy.Field()
    niveau_sortie = scrapy.Field()
    certificateur_nom = scrapy.Field()
    siret = scrapy.Field()
    rncp_url =scrapy.Field()

    titre_rs = scrapy.Field()
    etat_registre_rs = scrapy.Field()
    nsf_code_rs = scrapy.Field()
    nsf_nom_rs = scrapy.Field()
    formacode_code_rs = scrapy.Field()
    formacode_nom_rs = scrapy.Field()
    certificateur_nom_rs = scrapy.Field()
    siret_rs = scrapy.Field()
    rs_url =scrapy.Field()

