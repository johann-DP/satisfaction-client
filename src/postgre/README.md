# PostgreSQL : Dockerisation

Cette partie du projet contient des scripts Python pour créer et interroger une base de données PostgreSQL avec Docker. Voici les commandes essentielles et leurs utilisations pour gérer cette partie.

## Prérequis

- Python 3.9
- Docker
- Docker Compose
- `pip` pour installer les dépendances Python

## Installation

1. Installez Docker et Docker Compose si ce n'est pas déjà fait.
2. Clonez ce dépôt sur votre machine locale.
3. Installez les dépendances Python nécessaires :
    ```sh
    pip install docker docker-compose
    ```
4. Installez DBeaver pour gérer graphiquement votre base de données PostgreSQL :
    ```sh
    wget https://dbeaver.io/files/dbeaver-ce-latest-stable.x86_64.rpm
    sudo dnf config-manager --set-disabled dbeaver
    sudo dnf install ./dbeaver-ce-latest-stable.x86_64.rpm -y
    ```

## Commandes Docker

### 1. Construction des conteneurs

Construisez les images Docker pour PostgreSQL et l'application :
```sh
docker compose -f src/postgre/docker-compose.yml build
```

### 2. Démarrage des conteneurs

Démarrez les conteneurs PostgreSQL et l'application :
```sh
docker compose -f src/postgre/docker-compose.yml up
```

Cette commande lance à la fois le conteneur PostgreSQL et le conteneur de l'application qui initialise la base de données avec les données fournies dans `bank.json`.

### 3. Exécution de scripts dans le conteneur

Pour exécuter des scripts Python spécifiques, comme `query.py`, utilisez la commande suivante :
```sh
docker compose -f src/postgre/docker-compose.yml run postgre_app python src/postgre/query.py
```

### 4. Arrêt et suppression des conteneurs

Pour arrêter les conteneurs et nettoyer les ressources Docker associées, utilisez :
```sh
docker compose -f src/postgre/docker-compose.yml down
```

## Utilisation

### Initialisation de la base de données

Après avoir démarré les conteneurs avec `docker-compose up`, le script `CreatePostgre.py` sera automatiquement exécuté pour créer les tables et insérer les données dans PostgreSQL.

### Exécution de requêtes

Utilisez `query.py` pour exécuter des requêtes sur la base de données. Assurez-vous que les conteneurs sont en cours d'exécution avant d'exécuter ce script.

### Exemples de commandes

- Pour exécuter une requête spécifique :
    ```sh
    docker-compose -f src/postgre/docker-compose.yml run postgre_app python src/postgre/query.py
    ```

- Pour arrêter tous les conteneurs :
    ```sh
    docker-compose -f src/postgre/docker-compose.yml down
    ```

## Structure du projet

- `src/postgre/Dockerfile`: Définit l'image Docker pour l'application PostgreSQL.
- `src/postgre/docker-compose.yml`: Fichier de configuration Docker Compose pour orchestrer les conteneurs.
- `src/postgre/CreatePostgre.py`: Script Python pour créer les tables et insérer les données dans PostgreSQL.
- `src/postgre/query.py`: Script Python pour exécuter des requêtes sur la base de données.
- `data/bank/companies/bank.json`: Fichier JSON contenant les données initiales à insérer dans la base de données.

## Remarques

- Assurez-vous que les variables d'environnement dans le fichier `docker-compose.yml` sont correctement configurées pour votre environnement.
- Si vous rencontrez des problèmes, vérifiez les logs des conteneurs pour diagnostiquer les erreurs potentielles.
