# Projet Satisfaction Client - Monitoring Dockerisation

Ce répertoire contient l'ensemble des sources nécessaires pour lancer le monitoring avec Prometheus/Grafana de la base de données ElasticSearch


## Prérequis

- Docker
- Docker-compose


## Installation

1. Installer Docker et Docker-compose
2. Cloner le dépôt sur la machine locale



## Structure du projet

En partant de la racine du projet :


- `src/prometheus-grafana/docker-compose.yml` : Fichier de configuration Docker Compose qui permet de lancer les conteneurs de :
	- l'exporter de metrics d'ElasticSearch,
	- le service prometheus
	- le service grafana
	
- `src/prometheus-grafana/prometheus` : dossier qui contient les fichiers de configuration de prometheus
- `src/prometheus-grafana/grafana` : dossier qui contient les fichiers de configuration de grafana (notamment les dahsboards et le fichier des identifiants du service)




## Utilisation et Commandes Docker

Pour lancer le monitoring de la base Elastic Search avec prometheus/grafana:
- Dans un premier temps, il faut lancer le docker-compose de la base ElasticSearch ( normalement le docker-compose.yml du dossier `<racine_projet>/src/airflow` )


- Puis se placer dans ce répertoire (`<racine_projet>/src/prometheus-grafana`)
- lancer la commande de lancement du conteneur Docker

  	`docker-compose up`

	
Cette dernière va déployer les services suivants dans des conteneurs:
-  L'exporter de metrics de la base ElasticSearch sur le port 9114
-  Prometheus sur le port  9090
-  Grafana sur le port 3000


RQ: Les identifiants de Grafana sont paramétrables dans le fichier `<racine_projet>/src/prometheus-grafana/grafana/config.monitoring`

