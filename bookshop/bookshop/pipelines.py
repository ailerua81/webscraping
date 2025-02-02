# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from .items import BookshopItem
import pymongo
from itemadapter import ItemAdapter
from scrapy.exceptions import DropItem 
import logging
import hashlib



class BookshopPipeline:

    COLLECTION_NAME = 'books'
    mongo_host = "localhost"


    def __init__(self, mongo_uri, mongo_db):
        if not isinstance(mongo_uri, str) or not isinstance(mongo_db, str):
            raise ValueError("Erreur: mongo_uri et mongo_db doivent être des chaînes de caractères !")
        
        self.mongo_uri = mongo_uri
        self.mongo_db = mongo_db

    @classmethod
    def from_crawler(cls, crawler):
        mongo_uri = crawler.settings.get("MONGO_URI")
        mongo_db = crawler.settings.get("MONGO_DATABASE")

        if not isinstance(mongo_db, str):
            raise ValueError(f"Erreur: MONGO_DATABASE doit être une chaîne, mais a reçu {type(mongo_db)}")

        return cls(mongo_uri, mongo_db)

    def open_spider(self, spider):
        try:
            self.client = pymongo.MongoClient(self.mongo_uri, serverSelectionTimeoutMS=5000)
            self.db = self.client[self.mongo_db]
            # Vérifier la connexion
            self.client.server_info()
            logging.info("Connexion MongoDB réussie !")
        except Exception as e:
            logging.error(f"Erreur de connexion à MongoDB : {e}")



    def close_spider(self, spider):
        self.client.close()


    def process_item(self, item, spider):
        logging.info(f"Traitement de l'item : {item}")

        item_id = self.compute_item_id(item)

        if self.db[self.COLLECTION_NAME].find_one({"_id": item_id}):
            logging.info(f"Item en double : {item['photo']}")
            raise DropItem(f"Duplicate item found: {item}")
        else:
            item["_id"] = item_id
            self.db[self.COLLECTION_NAME].insert_one(ItemAdapter(item).asdict())
            logging.info(f"Insertion réussie : {item['photo']}")
            return item

     # Ajout de compute_item_id()
    def compute_item_id(self, item):
        """ Génère un identifiant unique basé sur l'image du livre (ou son titre si pas d'URL). """
        unique_key = item.get("photo", item.get("titre", ""))
        return hashlib.sha256(unique_key.encode("utf-8")).hexdigest()





    
