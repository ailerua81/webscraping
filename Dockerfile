FROM python:3.9

# Définir le dossier de travail
WORKDIR /app

# Copier les fichiers du projet
COPY . .

# # installer les dépendances
# RUN pip install --no-cache-dir -r requirements.txt

# # Vérifier que scrapy.cfg est bien présent
# RUN ls -l /app/bookshop

# WORKDIR /app/bookshop  # Aller dans le dossier contenant scrapy.cfg

# # Vérifier que Scrapy reconnaît le projet
# RUN scrapy list

# # Exposer le port 8050 pour Dash
# #EXPOSE 8050

# # Lancer Scrapy en arrière-plan puis démarrer le Dashboard
# CMD scrapy crawl bookshop & python /app/app.py

# FROM python:3.9

# WORKDIR /app

# COPY . .

# RUN pip install --no-cache-dir -r requirements.txt

# # Définir Scrapy dans le PATH
# ENV PATH="/app/bookshop:${PATH}"

# CMD python app.py

FROM python:3.9

WORKDIR /app

COPY . .

RUN pip install --no-cache-dir -r requirements.txt

# Assurer que Scrapy est installé et accessible
ENV PATH="/app/bookshop:${PATH}"

CMD python app.py












