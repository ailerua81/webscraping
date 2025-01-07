import scrapy
from scrapy import Request

class EurekaSpider(scrapy.Spider):
    name = "eureka"
    allowed_domains = ["eureka.valdemarne.fr"]
    start_urls = []

    custom_settings = {
        'DOWNLOAD_DELAY': 0,
        'CONCURENT_REQUESTS_PER_DOMAIN': 1
    }

    def __init__(self):
        url = 'https://eureka.valdemarne.fr/livres/catalogue?sort=class_vus&jeunesse=0&tagid=0&labelid=0&reflgid=0&pag='
        for page in range(1,121):
            self.start_urls.append(url + str(page))


    def parse(self, response):
        books = response.css('.catalogue--item')
        url_base = 'https://eureka.valdemarne.fr'
        for book in books:
            yield Request(url_base + book.css('a::attr(href)').get(), callback=self.parse_album)
         

    def parse_album(self, response):
        print("Response : ",response) 
        item = response.css('.container')

        titre = item.css('.albumname::text').get()
        auteur = response.xpath('//*[@id="tracklist2"]/div[1]/div[3]/ul/li/a/@title').get()
        editeur = response.xpath('//*[@id="plusinfo"]/dl[2]/dd/a/@title').get()

        resume = response.xpath('//*[@id="dxhr"]/div[3]/div[1]/div/div/p/text()').get()
        couv = response.css('#playervdo_wrapper > div.thumbWrapper.revealo > img::attr(src)').get()
        tranche_age = response.xpath('//*[@id="plusinfo"]/dl[4]/dd/a/text()').get()
        date_sortie = response.xpath('//*[@id="plusinfo"]/dl[3]/dd/text()').get()


        if resume is None:
            resume = response.xpath('//*[@id="dxhr"]/div[3]/div[1]/div/div/text()').get()
            if resume is None:
                resume = response.xpath('//*[@id="dxhr"]/div[3]/div[1]/div/div/p/span/text()').get()
            
        # genre = response.xpath('').get()
        yield {
                    'titre': titre,
                    'auteur': auteur,
                    'editeur': editeur,
                    'resume': resume,
                    'couv': couv,
                    'tranche_age': tranche_age,
                    'date_sortie': date_sortie,
                    # 'genre': genre,
        }             


    

