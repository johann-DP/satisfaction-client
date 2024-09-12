import requests

# Configuration Kibana
KIBANA_ADDRESS = "http://kb-container:5601"
KIBANA_DATAVIEW_REVIEWS_CONFIG_FILE = "./config/reviews-dv.ndjson"
KIBANA_DASHBOARDS_CONFIG_FILE = "./config/dashboards.ndjson"

def dataView_exists(dataView_id : str) -> bool:
    '''
    Contrôle de l'existence du Data View Kibana dont l'id est passé en paramètre.

    Paramètres :
        - id (str) : l'id du Data View Kibana recherché

    Retours :
        - bool : True si l'id existe
    '''
    req = KIBANA_ADDRESS + "/api/data_views/data_view/" + dataView_id
    res = requests.get(
        url=req,
    )
    statusCode = res.status_code
    res_content = res.json()

    #print("Get DataView id {}, status code = {}".format(dataView_id, statusCode))
    if statusCode == 200:
        if res_content["data_view"]["id"] == dataView_id:
            return True
        else:
            return False
    else:
        return False


def export_dataView(dataView_id : str) -> None:
    '''
    Télécharge la définition du Data View dont l'id est passé en paramètre (s'il existe), puis le
    sauvegarde dans le fichier identifié dans la variable KIBANA_DATAVIEW_REVIEWS_CONFIG_FILE.

    Paramètres :
        - id (str) : l'id du Data View Kibana à exporter

    Retours :
        - NA
    '''
    if dataView_exists(dataView_id):
        data = {'type': 'index-pattern'}
        headers = {'Content-type': 'application/json', 'kbn-xsrf': 'true'}
        req = KIBANA_ADDRESS + "/api/saved_objects/_export"
        #print(req)
        res = requests.post(
                url=req,
                json=data,
                headers=headers
        )
        #print(res.text)
        file_name = KIBANA_DATAVIEW_REVIEWS_CONFIG_FILE
        with open(file_name, 'w') as file:
            #json.dumps(res.json(), file)
            file.write(res.text)
        print("DataView {} exportée dans le fichier {} !".format(dataView_id, file_name))
        #print("Get DataView id {}, status code = {}".format(dataView_id, res.status_code))

    else:
        print("DataView {} inexistant, export non réalisé !")
    

def create_dataView(dataView_id : str) -> None:
    '''
    Crée un Data View Kibana avec l'id passé en paramètres. Si un Data View existe déjà avec
    cet id dans Kibana, celui-ci sera écrasé.

    Paramètres :
        - id (str) : l'id du Data View Kibana à créer

    Retours :
        - NA
    '''
    # Définition des headers
    headers = {'kbn-xsrf': 'true'}
    
    file_name = KIBANA_DATAVIEW_REVIEWS_CONFIG_FILE
    # Récupération du corps de la requête
    with open(file_name, 'r') as file:
        files = {'file': file}
    
        req = KIBANA_ADDRESS + "/api/saved_objects/_import?overwrite=true"
        res = requests.post(
            url=req,
            files=files,
            headers=headers
        )
    #print(res.json())
    print("Post DataView id {}, status code = {}".format(dataView_id, res.status_code))


def export_dashBoards() -> None:
    '''
    Télécharge les définitions des dashboards, puis les sauvegarde dans le fichier identifié 
    dans la variable KIBANA_DASHBOARDS_CONFIG_FILE.

    Paramètres :
        - NA

    Retours :
        - NA
    '''
    data = {'type': 'dashboard'}
    headers = {'Content-type': 'application/json', 'kbn-xsrf': 'true'}
    req = KIBANA_ADDRESS + "/api/saved_objects/_export"
    #print(req)
    res = requests.post(
            url=req,
            json=data,
            headers=headers
    )
    #print(res.text)
    file_name = KIBANA_DASHBOARDS_CONFIG_FILE
    with open(file_name, 'w') as file:
        #json.dumps(res.json(), file)
        file.write(res.text)
    print("DashBoards exportés dans le fichier {} !".format(file_name))


def create_dashBoards() -> None:
    '''
    Crée les dashboards Kibana à partir du fichier de configuration défini dans la
    variable KIBANA_DASHBOARDS_CONFIG_FILE. Si les dashboards existent déjà, ils sont
    écrasés.

    Paramètres :
        - NA

    Retours :
        - NA
    '''
    # Définition des headers
    headers = {'kbn-xsrf': 'true'}
    
    file_name = KIBANA_DASHBOARDS_CONFIG_FILE
    # Récupération du corps de la requête
    with open(file_name, 'r') as file:
        files = {'file': file}
    
        req = KIBANA_ADDRESS + "/api/saved_objects/_import?overwrite=true"
        res = requests.post(
            url=req,
            files=files,
            headers=headers
        )
    # print(res.json())
    print("Post dashboards, status code = {}".format(res.status_code))

# ===== MAIN =====

if __name__ == "__main__":

    KIBANA_ADDRESS = "http://localhost:5601"
    dataView_id = "reviews-dv"
    '''
    # Contrôle de l'existence du Data View
    res = dataView_exists(dataView_id)
    print("DataView '{}' existant : {}".format(dataView_id, res))

    # Extraction du template du Data View de Kibana
    export_dataView(dataView_id)

    # Création du Data View Kibana à partir du template disponible
    create_dataView(dataView_id)
    
    # Export des dashboards pour création des fichiers de configuration
    export_dashBoards()
    '''
    # Création des dashboards Kibana à partir du fichier de configuration disponible
    create_dashBoards()
    