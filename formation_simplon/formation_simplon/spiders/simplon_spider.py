import scrapy
from formation_simplon.items import FormationSimplonItem

class SimplonSpiderSpider(scrapy.Spider):
    name = "simplon_spider"
    allowed_domains = ["simplon.co", "francecompetences.fr"]
    start_urls = ["https://simplon.co/notre-offre-de-formation.html#nos-formations0"]

    custom_settings = {
        'DUPEFILTER_CLASS': 'scrapy.dupefilters.BaseDupeFilter',
        'COOKIES_ENABLED': False
    }

    def parse(self, response):
        formations = response.xpath("//a[@class='btn btn-pricipale btn-formation' and contains(text(), 'Découvrez la formation')]")
        for formation in formations:
            formation_url = formation.xpath("./@href").get()
            yield response.follow(formation, callback=self.parse_formation)

    # version rncp et rs rassemblés
    def parse_formation(self, response):
        item = FormationSimplonItem()
        item["intitule_formation"] = response.xpath("//h1/text()").get()
        item["categorie"] = response.xpath("//ol/li/a/text()").getall()[-1]
        item["voie_acces"] = response.xpath("//h3[contains(text(), 'Voie d’accès à la certification')]/following-sibling::ul/li/text()|//h3[contains(text(), 'Voie d’accès à la certification')]/following-sibling::ul/li/p/text()").getall()
        
        # # "route" vers registres
        # urls = response.xpath("//a[contains(@href, '//www.francecompetences.fr/recherche')]/@href").getall()
        # for i in range(len(urls)):
        #     urls[i] =  urls[i].replace("http:", "https:")
        #     if urls[i][-1]=="/":
        #         urls[i] = urls[i][:-1]
        # if urls != []:
        #     urls = set(urls)
        #     for url in urls:
        #         yield response.follow(url, meta={"item":item}, callback=self.parse_registre)
        # else:
        #     yield item

        # "route" page sessions avec francecompétences
        session_page = response.xpath("//a[contains(text(),'Les sessions ouvertes')]/@href").get()
        urls = response.xpath("//a[contains(@href, '//www.francecompetences.fr/recherche')]/@href").getall()
        if session_page:
            yield response.follow(session_page, meta={"item":item}, callback=self.parse_page_sessions)
        else:
            for i in range(len(urls)):
                urls[i] =  urls[i].replace("http:", "https:")
                if urls[i][-1]=="/":
                    urls[i] = urls[i][:-1]
            if urls != []:
                urls = set(urls)
                for url in urls:
                    item_url = FormationSimplonItem(item)
                    yield response.follow(url, meta={"item":item_url}, callback=self.parse_registre)
            else:
                yield item   

    def parse_page_sessions(self, response):
        item = response.meta["item"]
        sessions = response.xpath("//a[contains(text(),'Découvrez la session')]")
        agences = response.xpath("//div[@class='card-content']/text()").getall()
        agences=[i.strip() for i in agences if i.strip()]
        for session,agence in zip(sessions,agences):
            session_item = FormationSimplonItem(item)
            session_item["agence"] = agence
            session_url = session.xpath("./@href").get()
            if session_url:
                yield response.follow(session_url, meta={"item":session_item}, callback=self.parse_session)
            else:
                yield item

    def parse_session(self, response):
        item = response.meta["item"]   
        item["date_limite"] = response.xpath("//div[@class='date-bloc']/div/text()").getall()
        item["region"] = response.xpath("//i[contains(text(), 'location_on')]/parent::div/text()").getall()
        item["distanciel"] = response.xpath("//strong[contains(text(), '100%')]/text()").get()
        item["alternance"] = response.xpath("//strong[contains(text(), 'alternance')]/text()").get()
        item["echelle_duree"] = response.xpath("//i[contains(text(), 'hourglass_empty')]/parent::div/text()").getall()
        item["date_debut"] = response.xpath("//div[@class='card-session-info calendar']/text()").getall()
        item["date_fin"] = response.xpath("//strong[contains(text(), 'du') and contains(text(), 'au')]/text()").get()
        
        urls = response.xpath("//a[contains(@href, '//www.francecompetences.fr/recherche')]/@href").getall()
        for i in range(len(urls)):
            urls[i] =  urls[i].replace("http:", "https:")
            if urls[i][-1]=="/":
                urls[i] = urls[i][:-1]
        if urls != []:
            urls = set(urls)
            for url in urls:
                item_url = FormationSimplonItem(item)
                yield response.follow(url, meta={"item":item_url}, callback=self.parse_registre)
        else:
            yield item                

    def parse_registre(self, response):
        item = response.meta["item"]
        item["type_registre"] = response.url
        item["code_registre"] = response.url
        item["titre_registre"] = response.xpath("//h1/text()").get()
        item["statut_registre"] = response.xpath("//span[contains(text(), 'Etat')]/following-sibling::span/text()").get()
        item["code_nsf"] = response.xpath("//p[contains(text(),'NSF')]/following-sibling::div/p/span/text()").getall()
        item["nom_nsf"] = response.xpath("//p[contains(text(),'NSF')]/following-sibling::div/p/text()").getall()    
        item["code_formacode"] = response.xpath("//p[contains(text(),'Formacode')]/following-sibling::div/p/span/text()").getall()
        item["nom_formacode"] = response.xpath("//p[contains(text(),'Formacode')]/following-sibling::div/p/text()").getall()
        item["niveau_sortie"] = response.xpath("//p[contains(text(),'Nomenclature')]/following-sibling::div//span/text()").get()
        item["certificateur"] = response.xpath("//button[contains(text(),'Certificateur(s)')]/parent::div//td/text()").getall()[0]
        item["siret"] = response.xpath("//button[contains(text(),'Certificateur(s)')]/parent::div//td/text()").getall()[1] 
        item["url"] = response.url 
 
        yield item    
