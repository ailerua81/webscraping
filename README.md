# webscraping

Pour activer l'environnement virtuel, lancer la commande suivante :
$ pipenv shell

Pour vérifier que le chemin de l'éxecutable python est bien celui de l'environnement virtuel :
$ which python

Pour désactiver l'environnement virtuel : 
$ exit


commandes pour le scraping d'eureka : 

scrapy startproject eureka_catalogue
scrapy genspider eureka eureka.valdemarne.fr
crapy crawl eureka -o books.json



