# Orchestration de Pipeline avec Airflow et Docker Compose

Ce projet utilise Apache Airflow pour orchestrer des pipelines de données dans un environnement Dockerisé. La configuration inclut des services pour PostgreSQL, Redis, et plusieurs composants Airflow.

## Prérequis

- Docker
- Docker Compose

## Installation

1. Clonez ce dépôt GitHub.
2. Naviguez dans le répertoire du projet.

## Configuration des Services

Les services configurés sont les suivants :

- **PostgreSQL** : Utilisé comme base de données pour Airflow. Les données sont persistées grâce à un volume Docker nommé `postgres-db-volume` monté sur `/var/lib/postgresql/data` dans le conteneur.
- **Redis** : Utilisé comme broker pour la file d'attente des tâches.
- **Airflow Scheduler** : Composant Airflow qui planifie les tâches.
- **Airflow Webserver** : Interface utilisateur Web pour Airflow, exposée sur le port 8080.
- **Airflow Worker** : Exécute les tâches définies dans les DAGs.
- **Airflow Init** : Service pour initialiser la base de données Airflow.
- **Airflow Triggerer** : Utilisé pour gérer les triggers dans Airflow.
- **mlflow_service** : Service pour le serveur MLflow.
- **Flower** : Interface utilisateur pour monitorer les workers Celery, exposée sur le port 5555.
- **Elasticsearch** : Utilisé pour le stockage et la recherche des logs.
- **Kibana** : Interface pour visualiser les données d'Elasticsearch, exposée sur le port 5601.
- **FastAPI** : Service pour l'API FastAPI.
- **Airflow CLI** : Interface en ligne de commande pour Airflow.

Les services sont connectés via un réseau Docker personnalisé `es-net` utilisant le pilote `bridge`. Le volume `postgres-db-volume` est utilisé pour persister les données PostgreSQL.

## Commandes de Lancement

Pour démarrer les services, utilisez la commande suivante :

```sh
docker compose up -d
```
Pour arrêter les services, utilisez la commande suivante :

```sh
docker compose down
```

## Définition des DAGs

Les DAGs (Directed Acyclic Graphs) sont définis pour orchestrer les différentes tâches. Voici les principales configurations utilisées :

- **Arguments par défaut** : Définit les paramètres par défaut pour les tâches telles que le propriétaire (`owner`), la date de début (`start_date`), les tentatives de réexécution (`retries`), les délais entre les tentatives (`retry_delay`), etc.
- **Tâches** : Les tâches incluent l'utilisation de `DockerOperator` pour exécuter des scripts Python dans des conteneurs Docker, de `BashOperator` pour exécuter des commandes Bash, et de `curl` pour faire des requêtes HTTP.

### Exemple de Configuration de DAG

Un DAG typique pour ce projet inclut les tâches suivantes :

- **Tâche de Scraping** : Utilise `DockerOperator` pour exécuter un script de scraping dans un conteneur Docker. Le script est exécuté via une commande Bash à l'intérieur du conteneur.
- **Tâche PostgreSQL** : Utilise `DockerOperator` pour exécuter un script Python de chargement des données dans PostgreSQL.
- **Tâche FastAPI** : Utilise `DockerOperator` pour envoyer une requête POST à un service FastAPI.
- **Tâche MLflow** : Utilise `BashOperator` pour exécuter des scripts d'extraction de caractéristiques et d'expérimentation dans un conteneur Docker.
- **Tâche ElasticSearch/Kibana** : Utilise `DockerOperator` pour exécuter un script de chargement des données dans ElasticSearch.

Les DAGs sont planifiés pour s'exécuter à des intervalles réguliers et définis, et les tâches sont orchestrées selon les dépendances spécifiées dans le DAG.

### Dépendances des Tâches

Les dépendances entre les tâches sont définies comme suit :

- La tâche de scraping est exécutée en premier.
- Après la tâche de scraping, les tâches PostgreSQL, ElasticSearch/Kibana, et MLflow sont exécutées en parallèle.
- La tâche ElasticSearch/Kibana doit se terminer avant que la tâche FastAPI puisse être exécutée.

```
scraping_task
├── postgre_task
├── elastic_task
│   └── fastpai_task
└── mlflow_task
```

## Permissions Docker

Pour permettre à Docker et PostgreSQL de fonctionner correctement avec Airflow, vous devez modifier les permissions des sockets Docker et PostgreSQL. Exécutez les commandes suivantes :

```sh
sudo chmod 666 /var/run/docker.sock
sudo chmod 666 /var/run/postgresql/.s.PGSQL.5432
```

Ces commandes ajustent les permissions pour permettre aux services Docker et PostgreSQL de fonctionner sans restrictions liées aux permissions.
