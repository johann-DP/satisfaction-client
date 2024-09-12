# Préalable : à lancer à partir du répertoire "elastic" --> s'y positionner

# Build de l'image du service de chargement de la base
sudo docker image build . -t elastic_loading:latest

# Lancement des services ElasticSeach et Kibana via le docker-compose
sudo docker-compose up -d

# Temporisation, le temps que les services soient initialisés
echo Temporisation pour le démarrage des services ...
sleep 60

# Enregistrement du path absolu du répertoire "elastic"
elastic_folder=$(pwd)

# Recherche du path absolu du répertoire de data (structure système du projet)
cd ../../data
data_folder=$(pwd)

# Repositionnement dans le répertoire elastic
cd $elastic_folder

# Lancement du service de chargement de la base Elastic + configuration Kibana
echo Chargement de la base Elastic + configuration Kibana ...
sudo docker container run --rm \
--volume $data_folder:/data \
--network elastic_es-net \
elastic_loading:latest