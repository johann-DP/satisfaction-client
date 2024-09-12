#! /usr/bin/python
import os
import elasticManagement as elt
import kibanaManagement as kbn


# ========== MAIN ==========

if __name__ == "__main__":

    # Si l'index existe, on le supprime et le recrée pour purger la base
    if elt.indexExists(elt.ELASTIC_INDEX, elt.es):
        print("Suppression de l'index {} ...".format(elt.ELASTIC_INDEX), end="")
        resp = elt.es.indices.delete(index=elt.ELASTIC_INDEX)
        print(resp["acknowledged"])
    elt.createIndex(elt.ELASTIC_INDEX, elt.es)

    # Import des fichiers spécifiés dans la base Elasticsearch
    source_folder = os.getcwd() + "/" + elt.DATAFOLDER
    print("Dossier des fichiers de reviews à importer : ", source_folder)
    for filename in os.listdir(source_folder):
        elt.bulk_json(os.path.join(source_folder, filename), elt.ELASTIC_INDEX, elt.es)

    # Recréation du DataView 'reviews' (id = 'reviews-dv')
    kbn.create_dataView("reviews-dv")

    # Recréation du DataView 'reviews' (id = 'reviews-dv')
    kbn.create_dashBoards()

    # Fermeture de la connection Elasticsearch
    elt.es.transport.close()
