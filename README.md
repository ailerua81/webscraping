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

### Installation des packages nécessaires

```
pip install -r requirements.txt
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
## Lancer le dashboard 

- cloner le repository github
  ```
  git clone https://github.com/ailerua81/webscraping webscraping
  ```

- Avoir Docker et Docker compose sur sa machine
- Construire les conteneurs à l'aide de la commande (cela peut prendre un peu de temps) :
```
docker-compose build
docker-compose up -d
```

Construire l’image de l'application.

```
docker-compose up --build
```

Vous pourrez ensuite accéder au dashboard Dash via http://localhost:8050.

