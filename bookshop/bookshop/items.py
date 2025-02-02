# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class BookshopItem(scrapy.Item):
    
    titre = scrapy.Field()  # Titre
    auteur = scrapy.Field()  # Auteur
    editeur = scrapy.Field()  # Editeur
    date_edition = scrapy.Field()  # Date d'édition
    prix = scrapy.Field()  # Prix 
    photo = scrapy.Field()  # Lien vers la photo de la couverture du livre
    categories = scrapy.Field()  # Liste des catégories (ex. : Livre rare, Poésie)
    etat = scrapy.Field()  # État du livre
    resume = scrapy.Field()  # Résumé
    
    
    
