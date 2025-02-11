FROM python:3.9

WORKDIR /app

COPY . .

RUN pip install --no-cache-dir -r requirements.txt

# Assurer que Scrapy est installé et accessible
ENV PATH="/app/bookshop:${PATH}"

#CMD python app.py

# Définir le point d'entrée
CMD cd bookshop && scrapy crawl bookshop -o ../books.csv && cd .. && python app.py










