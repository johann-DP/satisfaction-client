from elasticsearch import Elasticsearch


# Configuration Elasticsearch
ELASTIC_ADDRESS = "http://localhost:9200"
ELASTIC_INDEX = "reviews"


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


# Instanciation du client elasticsearch
es = Elasticsearch(hosts = ELASTIC_ADDRESS)

# Contrôle de l'existence de l'index
indexAvailable = indexExists(ELASTIC_INDEX, es)
print("Contrôle de l'existence de l'index {} : {}".format(
    ELASTIC_INDEX,
    indexAvailable
))

if indexAvailable:
    print("Suppression de l'index {} ...".format(ELASTIC_INDEX))
    resp = es.indices.delete(
    index=ELASTIC_INDEX,
    )
    print(resp)
else:
    print("Pas d'action")