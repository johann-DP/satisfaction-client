#! /usr/bin/python
import json
from elasticsearch import Elasticsearch
from elasticsearch.helpers import bulk


# Configuration Elasticsearch
ELASTIC_ADDRESS = "http://es-container:9200"
ELASTIC_INDEX = "reviews"

# Configuration extraction
DATAFOLDER = "../data/bank/reviews"

# Instanciation du client elasticsearch
es = Elasticsearch(hosts = ELASTIC_ADDRESS)

# Fonctions
def bulk_json(fichier : str, index_name : str, es_client : Elasticsearch):
    '''
    Fonction permettant de lire, traiter et insérer en base Elastic
    le fichier JSON spécifié. 
    
    Paramètres :
        - fichier (str) : le fichier json à traiter
        - index_name (str) : l'index Elasticsearch dans lequel insérer les éléments
        - es_client (Elasticsearch) : le client Elasticsearch
        
    Retours :
        - NA
    '''
    with open(fichier) as json_file:
        json_data = json.load(json_file)
        docs_to_import = []
        identifyingName = json_data[0]["identifyingName"]
        print("Import de {} ... ".format(identifyingName), end="")

        # Récupération de l'identifiant de l'entreprise et 
        # rajout dans l'ensemble des reviews

        cnt_tot = 0
        for doc in json_data[0]["reviews"]:
            doc["identifyingName"] = identifyingName
            docs_to_import.append(doc)
            cnt_tot += 1
        if len(docs_to_import) > 0:
            bulk(es_client, docs_to_import, index=index_name)

        print("{} document(s) de l'entreprise {} importé(s) !"\
            .format(cnt_tot, identifyingName))
        
        del json_data
        del docs_to_import


def indexExists(index: str, es: Elasticsearch) -> bool :
    '''
    Fonction permettant de contrôler l'existence d'un index donné
    dans la base Elastic.

    Paramètres :
        - index (str) : l'index visé
        - es (Elasticsearch) : le client Elasticsearch
        
    Retours :
        - (bool) : true si l'index recherché existe dans la base
    '''
    index_list = list(es.indices.get(index="*").keys())
    return index in index_list


def createIndex(index: str, es: Elasticsearch) :
    '''
    Fonction permettant de créer l'index dans la base Elastic.
    Cette fonction s'appuie sur le fichier de configuration
    disponible sous config/reviews_config.txt.

    Paramètres :
        - index (str) : l'index à créer
        - es (Elasticsearch) : le client Elasticsearch
        
    Retours :
        - NA
    '''
    with open('config/reviews_config.txt', 'r') as file:
        body = file.read()
    resp = es.indices.create(index=index,body=body)
    print("Contrôle de création de l'index : {}".format(resp["acknowledged"]))



# ========== MAIN ==========

if __name__ == "__main__":

    import os

    ELASTIC_ADDRESS = "http://localhost:9200"
    DATAFOLDER = "../../data/bank/reviews"

    # Instanciation du client elasticsearch
    es = Elasticsearch(hosts = ELASTIC_ADDRESS)

    # Contrôle de l'existence de l'index
    reviewsExists = indexExists(ELASTIC_INDEX, es)
    print("Contrôle de l'existence de l'index {} : {}".format(
        ELASTIC_INDEX,
        reviewsExists
    ))


    # Si l'index existe, on le supprime et le recrée pour purger la base
    if reviewsExists:
        print("Suppression de l'index {} ...".format(ELASTIC_INDEX), end="")
        resp = es.indices.delete(index=ELASTIC_INDEX)
        print(resp["acknowledged"])
    createIndex(ELASTIC_INDEX, es)

    # Import des fichiers spécifiés dans la base Elasticsearch
    source_folder = os.getcwd() + "/" + DATAFOLDER
    print("Dossier des fichiers de reviews à importer : ", source_folder)
    for filename in os.listdir(source_folder):
        bulk_json(os.path.join(source_folder, filename), ELASTIC_INDEX, es)