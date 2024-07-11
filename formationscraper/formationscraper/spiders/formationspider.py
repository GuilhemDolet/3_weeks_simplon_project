import scrapy
from formationscraper.items import FormationscraperItem
import re

class FormationSpider(scrapy.Spider):
    name = "formationspider"
    allowed_domains = ["simplon.co", "www.francecompetences.fr"]
    start_urls = ["https://simplon.co/notre-offre-de-formation.html"]
    # custom_settings = {"ITEM_PIPELINES" : {
    # "formationscraper.pipelines.FormationscraperPipeline": 100,
    # "formationscraper.pipelines.DatabasePipelineFormations": 200
    
    # }}

    def parse(self, response):
        item = FormationscraperItem()
        formations_url = response.xpath('.//a[contains(text(), "Découvrez la formation")]/@href').getall()
        #liste avec tous les raccourcis permettant de reconnaître chaque lien vers une formation
        for url in formations_url:
            formation_id = None  # Initialisation de la variable vide
            match = re.search(r'\d+', url)  # Recherche du numéro dans l'URL

            if match:
                formation_id = match.group()
                item['formation_id'] = formation_id
            print(f"id: {formation_id}")
            yield scrapy.Request(url, callback=self.parse_formation, meta={'item': item})


    def parse_formation(self, response):
        # on stocke les informations dans une variable "formation"
        # on ne yield pas pour pouvoir continuer de nourrir la variable dans la fonction suivante

        item = response.meta['item']

        formation_intitule = response.xpath(".//h1/text()").get()
        formation_rncp = response.xpath(".//a[contains(@href,'https://www.francecompetences.fr/recherche/rncp')]/text()").get()
        formation_rs = response.xpath(".//a[contains(@href,'https://www.francecompetences.fr/recherche/rs')]/text()").get()
        formation_reussite = response.xpath(".//b[contains(text(),'%')][1]/text()").get()

        item['formation_intitule'] = formation_intitule
        item['formation_rncp'] = formation_rncp
        item['formation_rs']= formation_rs
        item['formation_reussite'] = formation_reussite
        
        print(f"intitulé: {formation_intitule}")
        print(f"rncp: {formation_rncp}")
        print(f"rs: {formation_rs}")
        print(f"reussite: {formation_reussite}")

        sessions_url = response.xpath(".//div[1]/a[contains(text(), 'Les sessions ouvertes')]/@href").getall()
        # session url pour aller sur les url correspondant aux dates et lieux des prochaines sessions de formation
        if sessions_url is not None :
            for session in sessions_url:
                yield scrapy.Request(session, callback=self.parse_sessions_formation, meta={'item': item})
        else :
            yield item

    def parse_sessions_formation(self, response):
        # voir comment parcourir une page dans une page tout en revenant sur la page principale après
        # ==> on le fait grâce à meta qui stocke toutes les infos d'une formation d'un yield à l'autre
        # page 0 page d'accueil des formations, exemple de page : https://simplon.co/notre-offre-de-formation.html
        # page 1 page formation , exemple de page : https://simplon.co/formation/developpeur-web-et-web-mobile/11
        # page 2 page des sessions ouvertes : exemple de page : https://simplon.co/i-apply/developpeur-web-et-web-mobile/11
        # lien vers la page 2 (sous-sous home) "//a[contains(text(), 'sessions ouvertes')]""
        item = response.meta['item']
        blocs_sessions = response.xpath("//div[@class='smp-card']") #permet de retourner le début de l'url dans la suite du for
        # Récupérer l'item SimplonFormationItem depuis meta
        
        for sess in blocs_sessions : 
        # au lieu de nb session dire xpath du bloc : //div[@class='smp-card']
        # on stocke les informations dans plusieurs variables "session"
        # on ne yield pas pour pouvoir continuer de nourrir la variable dans la fonction suivante
            session_sous_intitule = sess.xpath(".//h2[@class='card-title']/text()").get()
            session_distanciel = True if (sess.xpath(".//a[contains(@href,'distanciel')]").get()) else False
            session_alternance = True if (sess.xpath(".//a[contains(@href,'https://simplon.co/i-apply?tags=alternance')]").get()) else False
            session_date_limite = sess.xpath(".//div[contains(@class, 'date-bloc')]/@data-sort").get()
            session_date_debut = sess.xpath(".//div[@class= 'card-session-info calendar']/text()").getall()
            session_duree = sess.xpath(".//div[@class= 'card-session-info'][1]/text()").getall()
            session_lieu = sess.xpath(".//div[contains(@class, 'card-content-tag-container')]/parent::*/text()").getall()
            session_region = sess.xpath(".//div[@class= 'card-session-info'][2]/text()").getall()
            session_niveau = sess.xpath(".//div[@class= 'card-session-info'][3]/text()").getall()
            # région : //div[@class= 'card-session-info'][2]/text()
            # région : //div[contains(@class, 'card-session-info')][3]/i/parent::*/text()

            item['session_sous_intitule'] = session_sous_intitule
            item['session_distanciel'] = session_distanciel
            item['session_alternance'] = session_alternance
            item['session_date_limite'] = session_date_limite
            item['session_date_debut'] = session_date_debut
            item['session_duree'] = session_duree
            item['session_lieu'] = session_lieu
            item['session_region'] = session_region
            item['session_niveau'] = session_niveau


             # Imprimer pour déboguer



            print(f"distanciel: {session_distanciel}")
            print(f"alt: {session_alternance}")
            print(f"date limite: {session_date_limite}")
            print(f"Date début: {session_date_debut}")
            print(f"Durée: {session_duree}")
            print(f"Lieu: {session_lieu}")
            print(f"Niveau: {session_niveau}")


            yield item