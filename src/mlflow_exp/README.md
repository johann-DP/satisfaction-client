## Modélisation

### A - Fichiers Impliqués

- `Dockerfile.experiment` : Définit l’image Docker pour le service d’expérimentation.
- `Dockerfile.extraction` : Définit l’image Docker pour le service d’extraction de fonctionnalités.
- `Dockerfile.mlflow` : Définit l’image Docker pour le service MLflow.
- `Experiment.py` : Contient le code principal de l’expérimentation Spark et MLflow pour l’analyse de sentiment.
- `Extraction_features.py` : Contient le code d’extraction des fonctionnalités des fichiers JSON.
- `Start_experiment.sh` : Script pour démarrer l’expérimentation en vérifiant la disponibilité du serveur MLflow.
- `run_extraction.sh` : Script pour exécuter l’extraction des fonctionnalités.
- `requirements.txt` : Liste des dépendances Python nécessaires pour les différentes applications.
- `data/bank/reviews` : Dossier contenant les fichiers de revues à importer pour l’extraction de fonctionnalités.

### B - Commandes Impliquées

#### Construire et Lancer les Conteneurs

1. **Construire et Lancer le Conteneur d’Extraction**

    ```sh
    cd /path/to/deckerfiles
    docker build -t extraction -f Dockerfile.extraction .
    docker run --rm extraction
    ```

2. **Construire et Lancer le Conteneur d’Expérimentation**

    ```sh
    cd /path/to/deckerfiles
    docker build -t experiment -f Dockerfile.experiment .
    docker run --rm experiment
    ```

3. **Construire et Lancer le Conteneur MLflow**

    ```sh
    cd /path/to/deckerfiles
    docker build -t mlflow_server -f Dockerfile.mlflow .
    docker run -p 8080:8080 --rm mlflow_server
    ```

4. **Lancer l’Extraction des Données**

    ```sh
    docker run --rm extraction /app/run_extraction.sh
    ```

5. **Démarrer l’Expérimentation**

    ```sh
    docker run --rm experiment /app/start_experiment.sh
    ```

### C - Tester les Services

#### Vérifier l’État du Serveur MLflow

Accédez à `http://127.0.0.1:8080` dans votre navigateur pour vérifier l’interface MLflow.

#### Vérifier les Logs de l’Expérimentation

Les logs de l’expérimentation peuvent être consultés pour vérifier les étapes et les résultats de l’expérimentation.

#### Tester les Scripts

1. **Tester le Script d’Extraction**

    ```sh
    docker run --rm extraction python /app/scripts/extraction_features.py
    ```

2. **Tester le Script d’Expérimentation**

    ```sh
    docker run --rm experiment python /app/scripts/experiment.py --port 8080
    ```

### D - Explication du Code

#### experiment.py

1. **Importations et Configuration de argparse** :
   Le code importe les bibliothèques nécessaires et configure argparse pour accepter le port pour le serveur MLflow.

2. **Initialisation de Spark et MLflow** :
   Création d’une session Spark et configuration de l’URI de suivi MLflow en utilisant le nom de service Docker.

3. **Lecture et Préparation des Données** :
   Les données CSV sont lues avec un schéma défini manuellement, les valeurs nulles sont remplacées, et les données sont divisées en ensembles d’entraînement, de validation et de test.

4. **Pipeline de Traitement du Texte et Modèle** :
   Création d’un pipeline Spark ML avec Tokenizer, StopWordsRemover, HashingTF, et LogisticRegression.

5. **Entraînement et Validation du Modèle** :
   Le modèle est entraîné, validé, et enregistré avec MLflow. Les métriques de performance sont loguées, et le modèle est promu en production si les critères de validation sont remplis.

#### extraction_features.py

1. **Extraction des Données des Fichiers JSON** :
   Parcours des fichiers JSON dans le dossier spécifié, extraction des informations nécessaires, et stockage dans une liste.

2. **Écriture des Données dans un Fichier CSV** :
   Les données extraites sont écrites dans un fichier CSV avec des points-virgules comme délimiteur.

### E - Utilisations Possibles

#### Vérifier l’état de l’API

**Requête**

```sh
curl -X GET "http://127.0.0.1:8080/"
```

### Vérifier l’état de l’API

**Réponse**

```json
{
  "message": "Welcome to the Sentiment Analysis API"
}
```

### Vérifier l’état de MLflow

**Requête**

```sh
curl -X GET "http://127.0.0.1:8080/"
```

**Réponse**

```json
{
  "message": "MLflow Tracking Server is up and running"
}
```

### Lancer une Expérimentation

**Requête**

```sh
docker run --rm experiment python /app/scripts/experiment.py --port 8080
```

**Réponse**

Les métriques de performance sont loguées dans MLflow et le modèle est enregistré et promu en production si les critères de validation sont remplis. Les résultats peuvent être visualisés dans l’interface MLflow.

### Extraire des Données

**Requête**

```sh
docker run --rm extraction python /app/scripts/extraction_features.py
```

**Réponse**

Les données sont extraites des fichiers JSON et enregistrées dans un fichier CSV pour une utilisation ultérieure dans l’expérimentation.
