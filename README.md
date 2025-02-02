# PROJET DATA ENGINEERING

Ce projet est une application web qui permet de présenter les données scrappées sur le site de vente de livres d'occasion 
 " L'occasion de lire" : https://www.loccasiondelire.fr/

 Nous vous proposons un dashboard qui permet de visualiser les données sauvegardées dans une base MongoDB préalablement récupérées




### Environnement virtuel du projet

Pour activer l'environnement virtuel, lancer la commande suivante :
```
$ pipenv shell
```

Pour vérifier que le chemin de l'éxecutable python est bien celui de l'environnement virtuel :
```
$ which python
```

Pour désactiver l'environnement virtuel : 
```
$ exit
```



### Scraping


```
$ scrapy startproject bookshop
$ cd bookshop
$ scrapy genspider bookshop loccasiondelire.fr
$ scrapy crawl bookshop -o books.csv
```


### Base MongoDB

Pour vérifier les données de la base (MongoDb shell)

```
db.books.find().pretty()
```



