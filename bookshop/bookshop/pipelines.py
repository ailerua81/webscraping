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
from elasticsearch import Elasticsearch





class BookshopPipeline:

    COLLECTION_NAME = 'books'
    mongo_host = "localhost"
    es_host = "http://elasticsearch:9200"  # Adresse du conteneur Elasticsearch



    def __init__(self, mongo_uri, mongo_db):
        if not isinstance(mongo_uri, str) or not isinstance(mongo_db, str):
            raise ValueError("Erreur: mongo_uri et mongo_db doivent être des chaînes de caractères !")
        
        self.mongo_uri = mongo_uri
        self.mongo_db = mongo_db


    def create_index_if_not_exists(self):
        # Crée l'index 'books' dans Elasticsearch s'il n'existe pas."""
        if not self.es.indices.exists(index="books"):
            logging.info("Index 'books' non trouvé, création en cours...")
            self.es.indices.create(index="books", body={
                "settings": {
                    "number_of_shards": 1,
                    "number_of_replicas": 1
                },
                "mappings": {
                    "properties": {
                        "titre": { "type": "text" },
                        "auteur": { "type": "text" },
                        "editeur": { "type": "text" },
                        "prix": { "type": "float" }
                    }
                }
            })
            logging.info("Index 'books' créé avec succès !")
    

    @classmethod
    def from_crawler(cls, crawler):
        mongo_uri = crawler.settings.get("MONGO_URI")
        mongo_db = crawler.settings.get("MONGO_DATABASE")
        es_host = crawler.settings.get("ELASTICSEARCH_HOST", "http://elasticsearch:9200")

        if not isinstance(mongo_db, str):
            raise ValueError(f"Erreur: MONGO_DATABASE doit être une chaîne, mais a reçu {type(mongo_db)}")

        return cls(mongo_uri, mongo_db, es_host)



    def open_spider(self, spider):
        try:
            # Connexion MongoDB
            self.client = pymongo.MongoClient(self.mongo_uri, serverSelectionTimeoutMS=5000)
            self.db = self.client[self.mongo_db]
            self.client.server_info()
            logging.info("Connexion MongoDB réussie !")

            # Connexion Elasticsearch
            self.es = Elasticsearch(self.es_host)
            if not self.es.ping():
                raise ValueError("Impossible de se connecter à Elasticsearch")
            logging.info("Connexion Elasticsearch réussie !")

            # Vérifier et créer l'index Elasticsearch
            self.create_index_if_not_exists()

        except Exception as e:
            logging.error(f"Erreur de connexion : {e}")



    def close_spider(self, spider):
        self.client.close()

    def process_item(self, item, spider):
        logging.info(f"Traitement du livre : {item['titre']}")

        item_id = self.compute_item_id(item)

        # Vérifier si le livre est déjà en base
        if self.db[self.COLLECTION_NAME].find_one({"_id": item_id}):
            logging.info(f"Livre en double (ignoré) : {item['titre']}")
            raise DropItem(f"Duplicate item found: {item}")
        else:
            item["_id"] = item_id

            # Insertion MongoDB
            self.db[self.COLLECTION_NAME].insert_one(ItemAdapter(item).asdict())
            logging.info(f"✅ Livre ajouté dans MongoDB : {item['titre']}")

            # Indexation Elasticsearch
            try:
                self.es.index(index="books", document=ItemAdapter(item).asdict())
                logging.info(f"Livre indexé dans Elasticsearch : {item['titre']}")
            except Exception as e:
                logging.error(f"Erreur lors de l'indexation Elasticsearch : {e}")

            return item


     # Ajout de compute_item_id()
    def compute_item_id(self, item):
        """ Génère un identifiant unique basé sur l'image du livre (ou son titre si pas d'URL). """
        unique_key = item.get("photo", item.get("titre", ""))
        return hashlib.sha256(unique_key.encode("utf-8")).hexdigest()





    
