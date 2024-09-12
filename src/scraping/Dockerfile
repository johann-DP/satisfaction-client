# Utiliser une image Python de base
FROM python:3.9-slim-bullseye

# Installation de dépendences et des bibliothèques
RUN pip install --upgrade pip
RUN pip install requests
RUN pip install bs4

#Ajout du script de scraping
ADD scraping_bank_json.py /scraping/scraping_bank_json.py

#Changement du répertoire courant dans le conteneur
WORKDIR /scraping/

#Command pour lancer le script de scraping
CMD python3 scraping_bank_json.py
