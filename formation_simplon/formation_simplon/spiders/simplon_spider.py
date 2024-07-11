import scrapy
from formation_simplon.items import FormationSimplonItem

class SimplonSpiderSpider(scrapy.Spider):
    name = "simplon_spider"
    allowed_domains = ["simplon.co", "francecompetences.fr"]
    start_urls = ["https://simplon.co/notre-offre-de-formation.html#nos-formations0"]

    def parse(self, response):
        formations = response.xpath("//a[@class='btn btn-pricipale btn-formation' and contains(text(), 'Découvrez la formation')]")
        for formation in formations:
            formation_url = formation.xpath("./@href").get()
            yield response.follow(formation, callback=self.parse_formation)

    def parse_formation(self, response):
        item = FormationSimplonItem()
        item["intitule_formation"] = response.xpath("//h1/text()").get()
        item["categorie"] = response.xpath("//ol/li/a/text()").getall()[-1]
        item["code_rncp"] = response.xpath("//a[contains(@href, 'https://www.francecompetences.fr/recherche/rncp/')]/@href").get()
        item["code_rs"] = response.xpath("//a[contains(@href, 'https://www.francecompetences.fr/recherche/rs/')]/@href").get()
        item["voie_acces"] = response.xpath("//h3[contains(text(), 'Voie d’accès à la certification')]/following-sibling::ul/li/text()|//h3[contains(text(), 'Voie d’accès à la certification')]/following-sibling::ul/li/p/text()").getall()
        
        item["rncp_url"] = response.xpath("//a[contains(@href, 'https://www.francecompetences.fr/recherche/rncp/')]/@href").get()
        item["rs_url"] = response.xpath("//a[contains(@href, 'https://www.francecompetences.fr/recherche/rs/')]/@href").get()

        # # "route" vers registre rncp
        # if item["rncp_url"] is not None:
        #     yield response.follow(item["rncp_url"], meta={"item":item}, callback=self.parse_registre)
        # else:
        #     yield item

        # # "route" vers registre rs
        # if item["rs_url"] is not None:
        #     yield response.follow(item["rs_url"], meta={"item":item}, callback=self.parse_registre_rs)
        # else:
        #     yield item

        # "routes" intégrées vers registres rncp et rs
        # if item["rncp_url"] is not None:
        #     yield response.follow(item["rncp_url"], meta={"item":item}, callback=self.parse_registre)
        # elif item["rs_url"] is not None:
        #     yield response.follow(item["rs_url"], meta={"item":item}, callback=self.parse_registre_rs)
        # else:
        #     yield item

        # "route" sans francecompétences
        session_page = response.xpath("//a[contains(text(),'Les sessions ouvertes')]/@href").get()
        if session_page is not None:
            yield response.follow(session_page, meta={"item":item}, callback=self.parse_page_sessions)
        else:
            yield item

    def parse_page_sessions(self, response):
        item = response.meta["item"]
        sessions = response.xpath("//a[contains(text(),'Découvrez la session')]")
        for session in sessions:
            session_item = FormationSimplonItem(item)
            session_url = session.xpath("./@href").get()
            if session_url is not None:
                yield response.follow(session_url, meta={"item":session_item}, callback=self.parse_session)
            else:
                yield item

    def parse_session(self, response):
        item = response.meta["item"] 
        # item = FormationSimplonItem()   
        item["date_limite"] = response.xpath("//div[@class='date-bloc']/div/text()").getall()
        item["region"] = response.xpath("//i[contains(text(), 'location_on')]/parent::div/text()").getall()
        item["distanciel"] = response.xpath("//strong[contains(text(), '100%')]/text()").get()
        item["alternance"] = response.xpath("//strong[contains(text(), 'alternance')]/text()").get()
        item["echelle_duree"] = response.xpath("//i[contains(text(), 'hourglass_empty')]/parent::div/text()").getall()
        item["date_debut"] = response.xpath("//div[@class='card-session-info calendar']/text()").getall()
        item["date_fin"] = response.xpath("//strong[contains(text(), 'du') and contains(text(), 'au')]/text()").get()
        item["date_test"] = response.xpath("//strong[contains(text(), 'du') and contains(text(), 'au')]/text()").get()
        # item["date_test"] = response.xpath("//strong[contains(text(), 'Dates de la formation')]/text()").get()
        yield item
        
 
    # # mtéhode rncp sans rs
    # def parse_registre(self, response):
    #     item = response.meta["item"]
    #     item["titre"] = response.xpath("//h1/text()").get()
    #     item["etat_registre"] = response.xpath("//span[contains(text(), 'Etat')]/following-sibling::span/text()").get()
    #     item["nsf_code"] = response.xpath("//p[contains(text(),'NSF')]/following-sibling::div/p/span/text()").getall()
    #     item["nsf_nom"] = response.xpath("//p[contains(text(),'NSF')]/following-sibling::div/p/text()").getall()    
    #     item["formacode_code"] = response.xpath("//p[contains(text(),'Formacode')]/following-sibling::div/p/span/text()").getall()
    #     item["formacode_nom"] = response.xpath("//p[contains(text(),'Formacode')]/following-sibling::div/p/text()").getall()
    #     item["niveau_sortie"] = response.xpath("//p[contains(text(),'Nomenclature')]/following-sibling::div//span/text()").get()
    #     item["certificateur_nom"] = response.xpath("//button[contains(text(),'Certificateur(s)')]/parent::div//td/text()").getall()[0]
    #     item["siret"] = response.xpath("//button[contains(text(),'Certificateur(s)')]/parent::div//td/text()").getall()[1]

    #     yield item

    # mtéhode rncp avec rs
    def parse_registre(self, response):
        item = response.meta["item"]
        item["titre"] = response.xpath("//h1/text()").get()
        item["etat_registre"] = response.xpath("//span[contains(text(), 'Etat')]/following-sibling::span/text()").get()
        item["nsf_code"] = response.xpath("//p[contains(text(),'NSF')]/following-sibling::div/p/span/text()").getall()
        item["nsf_nom"] = response.xpath("//p[contains(text(),'NSF')]/following-sibling::div/p/text()").getall()    
        item["formacode_code"] = response.xpath("//p[contains(text(),'Formacode')]/following-sibling::div/p/span/text()").getall()
        item["formacode_nom"] = response.xpath("//p[contains(text(),'Formacode')]/following-sibling::div/p/text()").getall()
        item["niveau_sortie"] = response.xpath("//p[contains(text(),'Nomenclature')]/following-sibling::div//span/text()").get()
        item["certificateur_nom"] = response.xpath("//button[contains(text(),'Certificateur(s)')]/parent::div//td/text()").getall()[0]
        item["siret"] = response.xpath("//button[contains(text(),'Certificateur(s)')]/parent::div//td/text()").getall()[1]
        if item["code_rs"]:
            yield scrapy.Request(item["rs_url"], met={"item":item}, callback=self.parse_registre_rs)
        else:    
            yield item    

    def parse_registre_rs(self, response):
        item = response.meta["item"]
        item["titre_rs"] = response.xpath("//h1/text()").get()
        item["etat_registre_rs"] = response.xpath("//span[contains(text(), 'Etat')]/following-sibling::span/text()").get()
        item["nsf_code_rs"] = response.xpath("//p[contains(text(),'NSF')]/following-sibling::div/p/span/text()").getall()
        item["nsf_nom_rs"] = response.xpath("//p[contains(text(),'NSF')]/following-sibling::div/p/text()").getall()    
        item["formacode_code_rs"] = response.xpath("//p[contains(text(),'Formacode')]/following-sibling::div/p/span/text()").getall()
        item["formacode_nom_rs"] = response.xpath("//p[contains(text(),'Formacode')]/following-sibling::div/p/text()").getall()
        item["certificateur_nom_rs"] = response.xpath("//button[contains(text(),'Certificateur(s)')]/parent::div//td/text()").getall()[0]
        item["siret_rs"] = response.xpath("//button[contains(text(),'Certificateur(s)')]/parent::div//td/text()").getall()[1]

        yield item