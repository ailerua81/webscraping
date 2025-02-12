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

## Commentaire des choix techniques : 

Notre dashboard présente une analyse du site de vente de livres d'occasion "l'occasion de lire". Ce site comprend 12598 livre. Nous avons fait du scrapping en temps réel, en mettant à jour notre tableau toutes les 10 secondes. Or, scrapper tout le site prend beaucoup de temps, c'est pourquoi nous avons choisi de ne pas scrapper tous les livres et de se limiter à 100 livres.    
Nous avons tenté d'implémenter elastiquesearch mais suite à des problèmes avec Docker, nous avons supprimé cette option. Nous avons toutefois laissé en commentaire cette partie pour tenter de la reprendre plus tard. 

## Commentaire du dashborad : 

Dans le premier tableau, nous voyons la liste des 100 livres scrapés avec leur titre, leur auteur, leur date de création, leur date d'édition, leur prix, leur catégorie et leur état. En cas de données absente, la case est vide. Pour pouvoir en savoir plus sur un livre, on peut le selectionner et voir son résumé ainsi que sa couverture. 

Dans le deuxième graphique on voit la répartion des éditeurs, c'est à dire le pourcentage de livre éditer par un éditeur. On voit que les éditeurs sont globalement bien répartis. 

Le troisième graphique est un histogramme de la distribution des prix. On voit que le prix des livres sont distribués entre zéro et 52,2 euros. La majorité des livres sont compris entre 2.5 et 7.4 euros. 

Dans un troisième graphique, on s'intéresse à la distribution des livres par année d'édition. On voit qu'il y a plus de livres édités entre 2000 et 2020 qu'entre 1980 et 2000. Le nombre maximum de livre sur le site ont été édités en 2012. Il y a aussi beaucoup de livres récents. La deuxième années où le plus de livres ont été édités est 2020. On peut donc penser que les gens qui revendent des livres d'occasions les revendent rapidement après les avoir achetés. 

Dans le quatrième graphique, on cherche à savoir quelles sont les auteurs les plus présents. On observe qu'il n'y a pas particulièrement d'auteur plus représentés que les autres. Dans les derniers données scrapés, on peut voir par exemple que Régine Saint-Arnaud, André Bernat et Michel Gleizes sont représentés deux fois. 

Dans un cinquième graphique, on cherche à s'intérésser à la répartition des catégories. La catégorie la plus représentée est Religion et Spiritualité, Esotérisme avec plus de 20% des livres devant Roman divers et Voyages. Toutefois, les catégories correspondent à des tagues concatenées donc certaines catégories peuvent s'entrecouper ce qui peut fausser un peu les résultats. Pax exemple, il y a une catégorie Religion et Spiritualité, Esotérisme et une catégorie Religion et Spiritualité, Esotérisme, Sciences. 

Dans un sixième graphique, on compare les prix des livres par catégorie. Au vu du nombre de catégorie et du peu de livre répertoriés, il est difficile d'interpréter ce graphique. Il faudrait scraper plus de livre et traiter les catégories de manière plus précises pour qu'elles soient indépendantes les unes des autres. 

## Travaux futurs

- implémenter une version fonctionnelles avec elasticsearch pour  améliorer la recherche et le filtrage des livres de manière rapide et efficace. Contrairement à une simple recherche MongoDB qui est limitée aux requêtes exactes, Elasticsearch permet une recherche floue et tolérante aux fautes. De plus, Avec Elasticsearch, tu peux chercher un livre en fonction de plusieurs critères à la fois comme ici le titre, l'auteur, l'éditeur, la catégorie

-scraper plus de livres pour pouvoir intérpréter de manière plus précise les résulats et pouvoir faire des études statistiques.  