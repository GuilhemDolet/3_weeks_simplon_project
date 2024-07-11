# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class FormationscraperItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()

    #### items de formation
    id_formation_unique = scrapy.Field() 
    formation_id = scrapy.Field()
    formation_intitule = scrapy.Field()
    formation_rncp = scrapy.Field()
    formation_rs = scrapy.Field()
    formation_reussite = scrapy.Field()

    #### items de session
    session_sous_intitule = scrapy.Field()
    session_distanciel = scrapy.Field()
    session_alternance = scrapy.Field()
    session_date_limite = scrapy.Field()
    session_date_debut = scrapy.Field()
    session_duree = scrapy.Field()
    session_lieu = scrapy.Field()
    session_region = scrapy.Field()
    session_niveau = scrapy.Field()
