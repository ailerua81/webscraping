import scrapy
from scrapy.crawler import CrawlerProcess
from scrapy import Request
from bs4 import BeautifulSoup
import re



class BookshopSpider(scrapy.Spider):
    name = "bookshop"
    allowed_domains = ["loccasiondelire.fr"]
    start_urls = []

    url_base = 'https://www.loccasiondelire.fr/'


    custom_settings = {
        'DOWNLOAD_DELAY': 0.5,  # Laisser un délai pour ne pas surcharger le serveur
        'CONCURRENT_REQUESTS_PER_DOMAIN': 1,
        'USER_AGENT': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36'
    }


    def __init__(self):
        url = 'https://www.loccasiondelire.fr/?p='
        for page in range(1,2): # 507 pages - 12662 résultats
            self.start_urls.append(url + str(page))


    def parse(self, response):
        
        # Récupérer le contenu HTML brut de la page du produit
        html_content = response.text 

        # Utiliser BeautifulSoup pour analyser le contenu HTML
        soup = BeautifulSoup(html_content, 'html.parser')

        # Trouver tous les blocs qui représentent un livre
        livres = soup.find_all('div', class_='livre-image-mini')

        # Extraire les informations pour chaque livre
        for livre in livres:
            href = livre.find('a')['href'] 
            livre_url = self.url_base + href
            if livre_url:
                # Faire une requête vers la page du produit
                yield Request(livre_url, callback=self.parse_item)  


    def parse_item(self, response): 
        item_content = response.text 
        item_soup = BeautifulSoup(item_content, 'html.parser')   

        # Dictionnaire pour stocker les données extraites
        data = {}  

        # Extraire les informations du livre

        # Titre
        titre = item_soup.find('div', class_='titreLivre-detail') 
        if titre:
            data['titre'] = titre.get_text(strip=True) 

        # Auteur
        auteur = item_soup.find('div', class_='auteur')
        if auteur:
            data['auteur'] = auteur.get_text(strip=True)
        else:
            data['auteur'] =  None


        # Editeur
        editeur =  item_soup.find('div', class_='editeur')
        if editeur:
            data['editeur'] = editeur.get_text(strip=True)        
        else:
            data['editeur'] =  None


        # Date d'édition
        date_edition =  item_soup.find('div', class_='date-edition')
        if date_edition:
            data['date_edition'] = date_edition.get_text(strip=True)        
        else:
            data['date_edition'] =  None 


        # Prix du livre
        prix =  item_soup.find('span', class_='prix')
        if prix:
            data['prix'] = prix.get_text(strip=True)        
        else:
            data['prix'] =  None  


        # Photo du livre
        link = item_soup.find('a', class_='images-detail')
        style = link['style'] if link and 'style' in link.attrs else None
        if style:
            match = re.search(r"url\('(.+?)'\)", style)
            if match:
                image_url = match.group(1)
                if image_url:
                    data['photo'] = self.url_base + image_url
                else:
                    data['photo'] = None 


        # Catégories (liste)
        genres = []
        for genre_div in item_soup.find_all('div', class_='genre'):
            # Extraire le texte de chaque <a> dans ce div
            for a in genre_div.find_all('a'):
                genres.append(a.get_text(strip=True))

        data['categories'] = genres



        
        # Etat et 4eme de couverture du livre (résumé)
        for details in item_soup.find_all('div', class_='width100'):
            if details:
                value = details.get_text(strip=True)
                
                etat_match = re.search(r"État:(.*?)(?=4ème de couverture|ISBN|$)", value, re.DOTALL)
                couverture_match = re.search(r"4ème de couverture:(.*?)(?=ISBN|Vous voulez plus d'information|$)", value, re.DOTALL)

                etat_livre = etat_match.group(1).strip() if etat_match else "Non disponible"
                quatrieme_couverture = couverture_match.group(1).strip() if couverture_match else "Non disponible"

                data['etat'] = etat_livre
                data['resume'] = quatrieme_couverture
 

        # Retourner les données
        yield data              
     
