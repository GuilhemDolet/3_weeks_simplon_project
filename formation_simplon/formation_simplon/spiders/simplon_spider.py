import scrapy
from simplon_formation.items import FormationSimplonItem

class SimplonSpiderSpider(scrapy.Spider):
    name = "simplon_spider"
    allowed_domains = ["simplon.co", "francecompetences.fr"]
    start_urls = ["https://simplon.co/notre-offre-de-formation.html#nos-formations0"]

    def parse(self, response):
        formations = response.xpath("//a[@class='btn btn-pricipale btn-formation' and contains(text(), 'Découvrez la formation')]")
        for formation in formations:
            formation_url = formation.xpath("./@href").get()
            yield response.follow(formation_url, callback=self.parse_formation)

    def parse_formation(self, response):
        item = FormationSimplonItem()
        item["intitule_formation"] = response.xpath("//h1/text()").get()
        item["categorie"] = response.xpath("//ol/li/a/text()").getall()[-1]
        item["code_rncp"] = response.xpath("//a[contains(@href, 'https://www.francecompetences.fr/recherche/rncp/')]/text()").get()
        item["code_rs"] = response.xpath("//a[contains(@href, 'https://www.francecompetences.fr/recherche/rs/')]/text()").get()
        item["voie_acces"] = response.xpath("//h3[contains(text(), 'Voie d’accès à la certification')]/following-sibling::ul/li/text()").getall()
        session_page = response.xpath("//a[contains(text(),'Les sessions ouvertes')]/@href").get()
        # if session_page is not None:
        #     yield response.follow(session_page, callback=self.parse_session)
        # else:
        #     yield item
        yield item


    def parse_session(self, response):
        item = FormationSimplonItem()    
        item["date_limite"] = response.xpath("//div[@class='date-bloc']/div/text()").getall()
        item["agence"] = response.xpath("//div[@class='card-session-info']/text()").getall()[1]
        item["distanciel"] = response.xpath("//strong[contains(text(), 'alternance')]").get()
        item["alternance"] = response.xpath("//strong[contains(text(), 'alternance')]").get()
        item["echelle_duree"] = response.xpath("//div[@class='card-session-info']/text()").getall()[0]
        item["date_debut"] = response.xpath("//div[@class='card-session-info calendar']/text()").get()
        item["date_fin"] = response.xpath("//strong[contains(text(), 'Dates de la formation')]").get()

        yield item

    def parse_registre(self, response):
        item = FormationSimplonItem()
        item["titre"] = response.xpath("//h1/text()").get()
        item["etat_registre"] = response.xpath("//span[contains(text(), 'Etat')]/following-sibling::span/text()").get()
        item["formacode_code"] = response.xpath("//p[contains(text(),'Formacode')]/following-sibling::div/p/span/text()").getall()
        item["formacode_nom"] = response.xpath("//p[contains(text(),'Formacode')]/following-sibling::div/p/text()").getall()
        item["niveau_sortie"] = response.xpath("//p[contains(text(),'Nomenclature')]/following-sibling::div//span/text()").get()
        item["certificateur_nom"] = response.xpath("//button[contains(text(),'Certificateur(s)')]/parent::div//td/text()").getall()[0]
        item["siret"] = response.xpath("//button[contains(text(),'Certificateur(s)')]/parent::div//td/text()").getall()[1]

        yield item