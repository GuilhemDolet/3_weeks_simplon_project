import scrapy


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
            yield response.follow(formations_url, self.parse_formation)

        # next_page = response.css('a.next::attr(href)').get()
        # if next_page is not None:
        #     yield response.follow(next_page, self.parse)

        pass

    def parse_sessions_formation(self, response):
        # voir comment parcourir une page dans une page tout en revenant sur la page principale après
        # page 0 page d'accueil des formations, exemple de page : https://simplon.co/notre-offre-de-formation.html
        # page 1 page formation , exemple de page : https://simplon.co/formation/developpeur-web-et-web-mobile/11
        # page 2 page des sessions ouvertes : exemple de page : https://simplon.co/i-apply/developpeur-web-et-web-mobile/11
        # lien vers la page 2 (sous-sous home) "//a[contains(text(), 'sessions ouvertes')]""

        yield {
            'date_debut' : response.xpath("").get(),
            'date_fin' : response.xpath("").get(),
            'duree' : response.xpath("").get(),
            'lieu' : response.xpath("").get()
        }
        pass

    def parse_formation(self, response):
        yield {
            'intitule_formation' : response.xpath("//h1/text()").get(),
            'modalite' : response.xpath("").get(),
            'alternance' : response.xpath("").get(),
            'limite' : response.xpath("").get(),
            'niveau' : response.xpath("").get(),
            'rncp' : response.xpath("//a[contains(@href,'https://www.francecompetences.fr/recherche/rncp')]").get(),
            'reussite' : response.xpath("").get(),
            'certifications' : response.xpath("").get(),

        }
        # for formation in formations_url : # itération se répétant pour chaque lien présent dans la liste formations
        #     formations_url = response.xpath('//a[contains(text(), "Découvrez la formation")]') 
        #     film_url = film.xpath('./a').attrib['href']
        #     yield response.follow(film_url, self.parse_item)