import scrapy
from scrapy import Request
from bs4 import BeautifulSoup


class BouquinisteSpider(scrapy.Spider):
    name = "petitbouquiniste"
    allowed_domains = ["lepetitbouquiniste.fr"]
    start_urls = []

    custom_settings = {
        'DOWNLOAD_DELAY': 0.5,  # Laisser un délai pour ne pas surcharger le serveur
        'CONCURRENT_REQUESTS_PER_DOMAIN': 1,
        'USER_AGENT': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36'
    }
   

    def __init__(self):
        url = 'https://lepetitbouquiniste.fr/boutique/?product-page='
        for page in range(1,2): # 176 pages -- Exemple : seulement 1 pages pour tester
            self.start_urls.append(url + str(page))


    def parse(self, response):
        # Localiser tous les produits sur la page actuelle
        items = response.xpath('/html/body/div[1]/div/div/div/div/div/div[2]/div/div[2]/div/div/ul/li')

        for item in items:
            # Récupérer l'URL de chaque produit
            product_url = item.css('a::attr(href)').get()
            if product_url:
                # Faire une requête vers la page du produit
                yield Request(product_url, callback=self.parse_item)      



    def parse_item(self, response):
        # Récupérer le contenu HTML brut de la page du produit
        html_content = response.text  # Utiliser .text pour obtenir le contenu HTML complet

        # Utiliser BeautifulSoup pour analyser le contenu HTML
        soup = BeautifulSoup(html_content, 'html.parser')

        # Dictionnaire pour stocker les données extraites
        data = {}

        # Extraire les informations du livre
        desc = soup.find('h1')
        if desc:
            data['desc'] = desc.get_text(strip=True)

        # Extraire le prix
        price = soup.find('p', class_='price')
        if price:
            data['prix'] = price.get_text(strip=True) 


        # Extraire une image (première image trouvée)
        image = soup.find('img', class_='wp-post-image')
        if image and 'data-src' in image.attrs:
            data['image'] = image['data-src']   


        # Extraire les catégories
        span_tag = soup.find('span', class_='posted_in')
        categories = [a.text.strip() for a in span_tag.find_all('a', rel='tag')]
        data['categories'] =  categories 


        # Extraire les informations sur l'état du livre
        for b in soup.find_all("b"):
            label = b.get_text(strip=True).replace(" :", "")  # Nettoyer le label
            value = b.next_sibling.get_text(strip=True) if b.next_sibling and hasattr(b.next_sibling, 'get_text') else None
            if("Etat" in label):
                data[label] = value       

        
    
        # Retourner les données
        yield data