# Projet Satisfaction Client - Scraping Dockerisation

Ce répertoire contient l'ensemble des sources Python nécessaires pour le scraping des informations générales et des commentaires français des entreprises de la catégorie banque du site trustpilot. 


## Prérequis

- Docker
- Docker-compose
- `pip` pour installer les dépendances Python

## Installation

1. Installer Docker et Docker-compose
2. Cloner le dépôt sur la machine locale
3. Installer les dépendances Python nécessaires :
    `pip` install docker docker-compose


## Structure du projet

En partant de la racine du projet :

- `src/scraping/Dockerfile` : Définit l'image Docker pour le service de scraping
- `src/scraping/docker-compose.yml` : Fichier de configuration Docker Compose pour la construction de l'image et le lancement du conteneur de scraping
- `src/scraping/scraping_bank_json.py` : Script de scraping utilisé dans le conteneur
- `data/` : répertoire-parent, contenant le dossier dans lequel les fichiers JSON de reviews sont générés lors du scraping (/data/bank/reviews) et le JSON des informations générales des entreprises (/data/bank/companies)


## Utilisation et Commandes Docker

Pour lancer le scraping:

- se placer dans ce répertoire (`<racine_projet>/src/scraping`)
- lancer la commande de lancement du conteneur Docker

  	`docker-compose up`


Cette dernière va construire (build) l'image et lancer un conteneur qui va exécuter le script scraping_bank_json.py 
Il est à noter que ce script va extraire plusieurs fichier JSON:
- un fichier JSON bank.json contenant les informations générales des entreprises de la catégories banque du site trustpilot stocké dans le répertoire (<racine_projet>/data/bank/companies)
- des fichier JSON de reviews (1  par entreprise)	contenant les commentaires concernant l'entreprise. Ces fichiers sont stockés dans le répertoire (<racine_projet>/data/bank/reviews)


	ou

- se placer dans ce répertoire (`<racine_projet>/src/scraping`)
- lancer la commande de build de l'image Docker

  	`docker image build . -t scraping:latest`
  
-  lancer la commande de lancement du conteneur Docker

	`docker container run --rm -v <racine projet>/data:/scraping/data --network my_network  --name my_scraping scraping:latest`

	Pensez bien à remplacer  `<racine du projet>` par le path de la racine du dossier git cloné dans la commande précédente


## Informations à propos du fichier du script de scraping scraping_bank_json.py
### 1. Informations générales
Ce script en python nommé « scraping_bank_json.py » permet à l’aide des bibliothèques beautifulsoup et request d’extraire à partir des 2 types de pages HTML du site trustpilot les informations générales des entreprises de la catégorie banque dans un fichier bank.json et les commentaires par entreprise dans plusieurs
fichiers json de reviews.

En résumé, il  commence par parcourir les pages de types informations générales pour récupérer la liste de toutes les entreprises et écrire dans un fichier bank.json qui sera stocké dans
 le dossier data/companies
Puis il boucle sur la liste des entreprises récupérée à partir du premier fichier json, en  parcourant toutes les pages de type commentaires pour l’entreprise en cours afin d’en extraire son fichier de reviews.json 
et le stocker dans le dossier data/reviews.

/!\ Si la structure du site truspilot change il se peut que le script ne fonctionne plus et doivent être réadapté à la nouvelle structure.

### 2.  Détails

Pour fonctionner le script s'appuie sur différentes fonctions définies au sein du fichier "scraping_bank_json.py". Voici une bèvre description de ces fonctions:
1. get_soup_object_from_url(url):
	- Définition : Cette fonction prend une url en entrée et envoie un objet beautifulsoup à partir de cette url
	- paramètres d'entrée:
		- url : l'adresse url d'un site
		
	- paramètre de sortie:
		- soup: objet beautifulsoup créer à partir de l'url
		
	
	
2. fetch_reviews_data_from_page(url):
	- Définition : Cette fonction extrait le json de review de la page précisée par le paramètre url en entrée
	- paramètres d'entrée:
		- url : l'adresse url d'un site
		
	- paramètre de sortie:
		- reviews_json: objet json de review de la page définie par l'url

    - Remarques: cette fonction utilise	la fonction get_soup_object_from_url
	

3. fetch_reviews_data_for_company(company_name_id , output_directory = "data/bank"):
	- Définition : Cette fonction extrait les reviews de toutes les pages de commentaires pour une entreprise et écrit un fichier json dans le output_directory
	- paramètres d'entrée:
		- company_name_id : identifiant unique de l'entreprise définie sur le site trustpilot
		- output_directory : dossier dans lequel sera écrit le fichier json de reviews (commentaires) pour l'entreprise
		
	- paramètre de sortie:
		- None

    - Remarques: cette fonction utilise	la fonction fetch_reviews_data_from_page


4. fetch_reviews_data_for_all_companies_from_json(companies_json_filename = "data/bank/bank.json", output_directory = "data/bank")
	- Définition : Cette fonction permet d'extraire les reviews de toutes les pages de commentaires de toutes les entreprises et écrit un fichier json par entreprise dans le output_directory
	- paramètres d'entrée:
		- companies_json_filename : nom du fichier json des informations générales des entreprises obtenu à l'aide de la fonction "fetch_companies_data_from_category" 
		- output_directory : dossier dans lequel sera écrit les fichier jsons de reviews (commentaires) des entreprises présentes dans le fichier companies_json_filename
		
	- paramètre de sortie:
		- None

    - Remarques: cette fonction utilise	la fonction fetch_reviews_data_for_company et nécessite d'avoir utilisé au préalable la fonction fetch_companies_data_from_category pour avoir le fichier json des informations générales des entreprises
	
	
5. fetch_company_data_from_page(url)
	- Définition : Cette fonction extrait le json des informations générales des entreprises de la page précisée par le paramètre url en entrée
	- paramètres d'entrée:
		- url : l'adresse url d'un site
		
	- paramètre de sortie:
		- companies_json: objet json contenant les informations générales des entreprises de la page définie par l'url

    - Remarques: cette fonction utilise	la fonction get_soup_object_from_url


6.  fetch_companies_data_from_category(category ="bank",output_json_filename = "data/bank/bank.json")
	- Définition : Cette fonction permet d'extraire les informations générales de toutes les pages d'information générales des entreprises d'une catégorie du site trustpilot et de les enregristrer dans un fichier json bank.json

	- paramètres d'entrée:
		- category : nom de la catégorie d'entreprises du site trustpilot 
		- output_json_filename : Nom du fichier JSON d'informations générales de toutes les entreprises de la catégorie
		
	- paramètre de sortie:
		- None

    - Remarques: cette fonction utilise	la fonction fetch_company_data_from_page

 
 





