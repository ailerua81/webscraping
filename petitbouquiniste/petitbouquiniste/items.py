# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class PetitbouquinisteItem(scrapy.Item):
   
    # Définir les champs
    desc = scrapy.Field()  # Description du livre
    titre = scrapy.Field()  # Titre
    auteur = scrapy.Field()  # Auteur
    editeur = scrapy.Field()  # Editeur
    format_ = scrapy.Field()  # Format
    annee = scrapy.Field()  # Année de sortie
    prix = scrapy.Field()  # Prix 
    image = scrapy.Field()  # Lien vers l'image
    categories = scrapy.Field()  # Liste des catégories (ex. : Livre rare, Poésie)
    resume = scrapy.Field()  # Résumé
    etat = scrapy.Field()  # État du livre


    



