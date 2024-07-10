import scrapy
from scrapy import Request, xpath
from items import FormationscraperItem
import re

class FormationspiderSpider(scrapy.Spider):
    name = "formationspider"
    allowed_domains = ["simplon.co"]
    start_urls = ["https://simplon.co/notre-offre-de-formation.html"]
    custom_settings = {"ITEM_PIPELINES" : {
    "bookscraper.pipelines.DatabasePipelineFilm": 200,
    "bookscraper.pipelines.BookscraperPipelineFilm": 100
    }}

    def parse(self, response):

        formations_url = response.xpath('//a[contains(text(), "Découvrez la formation")]') 
        #liste avec tous les raccourcis permettant de reconnaître chaque lien vers une formation
        for formation in formations_url:
            yield scrapy.Request(formations_url, self.parse_formation)

    def parse_formation(self, response):
        # on stocke les informations dans une variable "formation"
        # on ne yield pas pour pouvoir continuer de nourrir la variable dans la fonction suivante

        item = FormationscraperItem()

        formation_intitule = response.xpath(".//h1/text()").get()
        formation_rncp = response.xpath(".//a[contains(@href,'https://www.francecompetences.fr/recherche/rncp')]").get()
        formation_rs = response.xpath(".//a[contains(@href,'https://www.francecompetences.fr/recherche/rs')]").get()
        formation_reussite = response.xpath(".//b[contains(text(),'%')][1]").get()
        element = response.xpath('.//a[contains(text(), "Sessions ouvertes")]')

        if element:
            url = element[0].get('href') # on récupère l'URL de l'attribut href
            match = re.search(r'\d+', url) # on recherche le numéro dans l'URL
            if match:
                formation_id = match.group()

        item['intitule_formation'] = formation_intitule
        item['rncp'] = formation_rncp
        item['rs']= formation_rs
        item['reussite'] = formation_reussite
        item['id_formation'] = formation_id
        
        sessions_url = response.xpath('.//a[contains(text(), "Sessions ouvertes")]') 
        # session url pour aller sur les url correspondant aux dates et lieux des prochaines sessions de formation

        yield scrapy.Request(sessions_url, callback=self.parse_sessions_formation, meta={'item': item})

    def parse_sessions_formation(self, response):
        # voir comment parcourir une page dans une page tout en revenant sur la page principale après
        # ==> on le fait grâce à meta qui stocke toutes les infos d'une formation d'un yield à l'autre
        # page 0 page d'accueil des formations, exemple de page : https://simplon.co/notre-offre-de-formation.html
        # page 1 page formation , exemple de page : https://simplon.co/formation/developpeur-web-et-web-mobile/11
        # page 2 page des sessions ouvertes : exemple de page : https://simplon.co/i-apply/developpeur-web-et-web-mobile/11
        # lien vers la page 2 (sous-sous home) "//a[contains(text(), 'sessions ouvertes')]""
        item = response.meta[item]
        blocs_sessions = response.xpath("//div[@class='smp-card']") #permet de retourner le début de l'url dans la suite du for
        # Récupérer l'item SimplonFormationItem depuis meta
        
        for sess in blocs_sessions : 
        # au lieu de nb session dire xpath du bloc : //div[@class='smp-card']
        # on stocke les informations dans plusieurs variables "session"
        # on ne yield pas pour pouvoir continuer de nourrir la variable dans la fonction suivante
            session_sous_intitule = sess.xpath(".//h2[@class='card-title']").get()
            session_distanciel = True if (sess.xpath(".//a[contains(@href,'distanciel')]").get()) else False
            session_alternance = True if (sess.xpath(".//a[contains(@href,'https://simplon.co/i-apply?tags=alternance')]").get()) else False
            session_date_limite = sess.xpath(".//div[contains(@class, 'date-bloc')]").get()
            session_date_debut = sess.xpath(".//div[@class='card-session-info calendar']").get()
            session_duree = sess.xpath("(//i[contains(@class,'material-icons')])[2]/parent::node()/text()[1]").get() 
            session_lieu = sess.xpath("(//i[contains(@class,'material-icons')])[1]/parent::node()/text()[1]").get()
            session_niveau = sess.xpath("(//i[contains(@class,'material-icons')])[4]/parent::node()/text()[1]").get()

            item['sous-intitule'] = session_sous_intitule
            item['distanciel'] = session_distanciel
            item['alternance'] = session_alternance
            item['date_limite'] = session_date_limite
            item['date_debut'] = session_date_debut
            item['duree'] = session_duree
            item['lieu'] = session_lieu
            item['niveau'] = session_niveau

        yield item