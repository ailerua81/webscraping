FROM python:3.9-slim

# Définir le dossier de travail
WORKDIR /app

# Copier les fichiers du projet
COPY . .

# Copier le fichier requirements.txt et installer les dépendances
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Exposer le port 8050 pour Dash
EXPOSE 8050

# Lancer le dashboard
CMD ["python", "app.py"]





