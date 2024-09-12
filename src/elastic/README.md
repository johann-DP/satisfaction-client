# Projet Satisfaction Client - ElasticSearch Dockerisation

Ce répertoire contient l'ensemble des sources Python nécessaires pour configurer et charger les solutions Elastic :
- la base ElasticSearch
- la solution de DataViz' Kibana

## Prérequis

- Docker
- Docker-compose
- `pip` pour installer les dépendances Python

## Installation

1. Installer Docker et Docker-compose
2. Cloner le dépôt sur la machine locale
3. Installer les dépendances Python nécessaires :
    `pip` install docker docker-compose

## Commandes Docker

### 1. Construction de l'image

Construisez l'image du service de configuration/chargement des solutions Elastic :

- se placer dans ce répertoire (`<racine_projet>/src/elastic`)
- lancer la commande de build de l'image :
    `docker image build . -t bost67dst/elastic_loading:latest`

### 2. Démarrage des services Elastic

Le lancement des services Elastic (ElasticSearch, Kibana) se réalise en lançant le docker-compose disponible ici :

- se placer dans ce répertoire (`<racine_projet>/src/elastic`)
- lancer les services Elastic :
    `docker-compose up -d`

### 3. Lancement du service de configuration/chargement

Pour exécuter les configurations/chargements des services Elastic, il suffit de lancer l'image du service construite précédemment.
Au lancement, il est nécessaire :

- de lancer le conteneur sur le même network que les services Elastic : `elastic_es-net` (cf docker-compose)
- de monter le répertoire `<racine_projet>/data` sur le volume `/data` du conteneur

    `docker container run --volume <racine_projet>/data:/data --network elastic_es-net bost67dst/elastic_loading:latest`

### 4. Arrêt des services Elastic

Pour stopper les services Elastic, exécutez la commande suivante :

- se placer dans ce répertoire (`<racine_projet>/src/elastic`)
- stopper les services Elastic :
    `docker-compose down`

## Utilisation

Ce répertoire vise principalement à mettre à disposition les ressources nécessaires pour construire l'image du service de configuration/chargement des solutions Elastic. Le docker-compose, fourni ici pour lancer les services Elastic, est mis à disposition pour des tests standalone et pour pouvoir réaliser des tests unitaires dans la pipeline CI.

Pour réaliser un test :
    
1. Lancer les services Elastic
2. Contrôler l'état opérationnel des services Elastic (e.g. chargement de la page GUI Kibana, disponible sur le port 5601, cette opération peut prendre quelques dizaines de secondes)
3. Lancer l'image de configuration/chargement
4. Contrôler les traces du service de chargement
5. Stopper les services Elastic

## Structure du projet

En partant de la racine du projet :

- `src/elastic/Dockerfile` : Définit l'image Docker pour le service de configuration/chargement Elastic
- `src/elastic/docker-compose.yml` : Fichier de configuration Docker Compose pour les services Elastic (ElasticSearch, Kibana)
- `src/elastic/ElasticManagement.py` : Script de fonctions spécifiques à la configuration et au chargement de la base ElasticSearch
- `src/elastic/KibanaManagement.py` : Script de fonctions spécifiques à la configuration du service de DataViz' Kibana
- `src/elastic/main.py` : Script principal d'exécution du service, appelé comme point d'entrée de l'image Docker
- `data/` : répertoire-parent, contenant le dossier dans lequel les fichiers JSON de reviews sont générés lors du scraping (/data/bank/reviews)
    
## Remarque

- Pour une utilisation standalone, il est possible de déposer manuellement des fichiers JSON de reviews dans le répertoire <racine_projet>/data/bank/reviews

[Docker](https://docs.docker.com/)
