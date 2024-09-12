# Utiliser une image Python de base
FROM python:3.9-slim

# Définir le répertoire de travail
WORKDIR /app

# Copier les fichiers de dépendances
COPY requirements.txt .

# Installer les dépendances Python
RUN pip install --no-cache-dir -r requirements.txt

# Copier le reste des fichiers de l'application
COPY ./src/postgre/* .

# Commande par défaut pour exécuter le script CreatePostgre.py
CMD ["python", "CreatePostgre.py"]
