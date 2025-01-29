# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class BookshopItem(scrapy.Item):
    
    title = scrapy.Field()  # Titre
    autor = scrapy.Field()  # Auteur
    editor = scrapy.Field()  # Editeur
    edition_date = scrapy.Field()  # Date d'édition
    price = scrapy.Field()  # Prix 
    image = scrapy.Field()  # Lien vers l'image
    categories = scrapy.Field()  # Liste des catégories (ex. : Livre rare, Poésie)
    state = scrapy.Field()  # État du livre
    summary = scrapy.Field()  # Résumé
    
    
    
