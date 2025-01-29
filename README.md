# webscraping

Pour activer l'environnement virtuel, lancer la commande suivante :
$ pipenv shell

Pour vérifier que le chemin de l'éxecutable python est bien celui de l'environnement virtuel :
$ which python

Pour désactiver l'environnement virtuel : 
$ exit


commandes pour le scraping d'eureka : 

$ scrapy startproject eureka_catalogue
$ scrapy genspider eureka eureka.valdemarne.fr
$ scrapy crawl eureka -o books.json


commandes pour le scraping du site "le petit bouquiniste"
$ scrapy startproject petitbouquiniste
$ cd petitbouquiniste
$ scrapy genspider petitbouquiniste lepetitbouquiniste.fr
$ scrapy crawl petitbouquiniste -o books.json




commandes pour le scraping du site "la bourse aux livres"
$ scrapy startproject labourseauxlivres
$ cd labourseauxlivres
$ scrapy genspider bourseauxlivres shop.labourseauxlivres.fr
$ scrapy crawl bourseauxlivres -o books.json




