## A - Fichiers Impliqués

1. **Dockerfile**
   Définit l’image Docker pour le service FastAPI.

2. **docker-compose.yml**
   Définit la configuration du service Docker FastAPI.

3. **main.py**
   Contient le code principal de l’application FastAPI pour l’analyse de sentiment.

4. **requirements.txt**
   Liste des dépendances Python nécessaires pour l’application.

5. **data/bank/reviews**
   Dossier contenant les fichiers de revues à importer dans Elasticsearch.

## B - Commandes Impliquées

1. **Construire et Lancer le Conteneur Elasticsearch et Kibana**

    ```sh
    cd /path/to/elastic
    docker-compose build
    docker-compose up -d
    ```

2. **Construire et Lancer le Conteneur FastAPI**

    ```sh
    cd /path/to/fast-api
    docker-compose build
    docker-compose up -d
    ```

3. **Importer les Données dans Elasticsearch Configurer Kibana/Elasticsearch**

    Lancement du service de chargement de la base Elastic + configuration Kibana (dans dossier elastic normalement déjà fait)

    ```sh
    echo Chargement de la base Elastic + configuration Kibana ...
    sudo docker container run --rm \
    --volume $data_folder:/data \
    --network elastic_es-net \
    elastic_loading:latest
    ```

4. **Tester l’API FastAPI**

    - **Vérifier l’état de l’API**

        ```sh
        curl -X GET "http://127.0.0.1:8000/"
        ```

    - **Vérifier l’état d’Elasticsearch**

        ```sh
        curl -X GET "http://127.0.0.1:8000/es_health"
        ```

    - **Obtenir des prédictions sur les reviews**

        ```sh
        curl -X POST "http://127.0.0.1:8000/predict" -H "Content-Type: application/json" -d '{"limit": 5}'
        ```

    limit: nombre de prédictions 

    **Pour Envoyer une Requête de Prédiction Sans Limite**

    Vous pouvez envoyer une requête POST à l’endpoint `/predict` sans spécifier de limite, ce qui fera en sorte que toutes les entrées dans l’index Elasticsearch seront traitées.
    Utilisez la commande curl suivante pour faire une prédiction pour toute la base:

    ```sh
    curl -X POST "http://127.0.0.1:8000/predict" -H "Content-Type: application/json" -d '{}'
    ```

    **Attention**, cela peut prendre énormément de temps !

    - **Tester une prédiction avec un texte donné**

        ```sh
        curl -X POST "http://127.0.0.1:8000/test" -H "Content-Type: application/json" -d '{"text": "Ceci est un test de prédiction."}'
        ```

5. **Accéder à Kibana pour Visualiser les Prédictions**

    - Ouvrir Kibana dans un navigateur web à l’adresse [http://localhost:5601](http://localhost:5601)
    - Créer un Data View pour l’index reviews
    - Utiliser Discover pour rechercher les documents contenant des prédictions.

## C - Explication du code main.py

Ce code implémente une API FastAPI pour l’analyse de sentiment basée sur un modèle SparkML. L’API interagit avec Elasticsearch pour obtenir des données de révision et mettre à jour les prédictions. Voici une explication détaillée des différentes parties du code :

1. **Importations et Configuration du Logging** :
   Le code importe les bibliothèques nécessaires et configure le logging pour surveiller l’activité de l’application.
 
2. **Initialisation de FastAPI** :
   Un objet FastAPI est créé pour définir les routes et gérer les requêtes.
 
3. **Configuration d’Elasticsearch** :
   Les variables d’environnement sont utilisées pour obtenir l’adresse d’Elasticsearch et le chemin du modèle de prédiction.
   Une session Spark est créée et configurée avec les paramètres nécessaires.
   Le modèle de prédiction est chargé à partir du chemin spécifié.
 
4. **Initialisation du Client Elasticsearch** :
   Le code tente de se connecter à Elasticsearch et de vérifier la connexion.
 
5. **Définition des Modèles de Requête** :
   Deux classes Pydantic sont définies pour les requêtes : PredictionRequest pour les prédictions et TestRequest pour les tests de prédiction sur un texte donné.
 
6. **Routes de l’API** :
    - **Route de page d'accueil (GET /)** :
      Retourne un message de bienvenue.
 
    - **Route de Prédiction (POST /predict)** :
      Reçoit une requête avec une limite optionnelle pour le nombre de prédictions.
      Interroge Elasticsearch pour obtenir les revues.
      Transforme les revues en DataFrame Spark, effectue des prédictions, et met à jour Elasticsearch avec les résultats.
      Enregistre les prédictions dans un fichier texte.
 
    - **Route de Test de Modèle (POST /test)** :
      Reçoit un texte et effectue une prédiction en utilisant le modèle chargé.
      Retourne la prédiction pour le texte donné.
 
    - **Route de Santé Elasticsearch (GET /es_health)** :
      Vérifie l’état du cluster Elasticsearch et retourne le statut.

## D - Utilisations Possibles

1. **Vérifier l’état de l’API** :
   
    - Requête : GET /
    - Réponse : {"message": "Welcome to the Sentiment Analysis API"}

2. **Vérifier l’état d’Elasticsearch** :
   
    - Requête : GET /es_health
    - Réponse : {"status": "green"} ou autre statut selon l’état du cluster Elasticsearch.

3. **Obtenir des prédictions sur les revues** :
   
    - Requête : POST /predict avec un JSON contenant { "limit": 5 }
    - Réponse : Un message indiquant où les prédictions sont enregistrées et combien de prédictions ont été faites.
