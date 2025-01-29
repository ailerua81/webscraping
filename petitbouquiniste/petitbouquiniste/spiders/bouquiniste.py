import scrapy
from scrapy import Request
from bs4 import BeautifulSoup
from petitbouquiniste.items import PetitbouquinisteItem
import re


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
        for page in range(1,3): # 176 pages
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
            raw_desc = desc.get_text(strip=True)
            data['desc'] = raw_desc  # Garder le champ brut si besoin

        # Appeler la fonction parse_desc pour séparer les données
        parsed_desc = self.parse_desc(raw_desc)
        data.update(parsed_desc)  # Ajouter titre, auteur, éditeur, format, année au dictionnaire


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


        # Extraire un résumé
        div_tag = soup.find('div', class_='et_pb_wc_description_1_tb_body')
        # Extraire le texte du résumé à l'intérieur de la balise <p>
        if div_tag:
            p_tag_sum = div_tag.find('p')  # Trouver la première balise <p> à l'intérieur
            if p_tag_sum:
                summary = p_tag_sum.get_text(strip=True)  # Récupérer et nettoyer le texte
                data['resume'] = summary
            else:
                data['resume'] = "neant"

        data['etat'] = []
        # Extraire les informations sur l'état du livre
        for b in (soup.find_all("b") or soup.find_all("strong") or soup.find_all("p")):
            value = b.get_text(strip=True)
            if("Etat" in value):
                data['etat'].append(value)
                if (b.next_sibling and hasattr(b.next_sibling, 'get_text')):
                    data['etat'].append(b.next_sibling.get_text(strip=True))
    
        
    
        # Retourner les données
        yield data



    # Fonction pour extraire le titre, l'auteur, l'éditeur, le format, et l'année à partir du champ desc.
    # Structures trouvées : 
    #        "Titre – Auteur / Editeur / Format / Année"
    #        ""
    def parse_desc(self, desc):
        print("IN PARSE_DESC")

        # Initialisation des champs
        parsed_data = {
            "titre": None,
            "auteur": None,
            "editeur": None,
            "format": None,
            "annee": None
        }

        # Nettoyage de base
        desc = desc.strip()


        # 1. Extraire titre et auteur (séparés par "–")
        if "–" in desc:
            titre_auteur = desc.split("–")
            if len(titre_auteur) > 1:
                parsed_data["titre"] = titre_auteur[0].strip()
                parsed_data["auteur"] = titre_auteur[1].strip()

        # 2. Extraire l'éditeur (Ed : ou Editions :)
        match_editeur = re.search(r'(Ed\s?:|Editions\s?:)\s?([^/]+)', desc)
        if match_editeur:
            parsed_data["editeur"] = match_editeur.group(2).strip()

        # 3. Extraire le format (mention de "Format")
        match_format = re.search(r'(Format\s?:?\s?[^/]+)', desc, re.IGNORECASE)
        if match_format:
            parsed_data["format"] = match_format.group(1).strip()

        # 4. Extraire l'année (4 chiffres)
        match_annee = re.search(r'\b(19|20)\d{2}\b', desc)
        if match_annee:
            parsed_data["annee"] = match_annee.group(0)

        # 5. Gestion des cas particuliers
        # Si le titre ou l'auteur n'ont pas été correctement identifiés, utiliser le début de `desc`
        if not parsed_data["titre"] and not parsed_data["auteur"]:
            parts = desc.split("/")
            if parts:
                parsed_data["titre"] = parts[0].strip()

        return parsed_data


       






            