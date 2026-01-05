# crypto_scraper
Ce projet a pour objectif de surveiller  la valeur des cryptomonnaies, effectuer des oppérations et de déclencher des alertes à travers un chatbot Discord. Ces actions se feront par l'exploitation d'un portefeuille sur plateforme Coinbase.

## Stack technique 
![Python](https://img.shields.io/badge/Python-3.9-yellow)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-13-blue)
![Docker](https://img.shields.io/badge/Docker-28.3.2-blue)
![Apache Airflow](https://img.shields.io/badge/Apache%20Airflow-3.0.4-greeb)

## Préparation de l'environnement
### Installer Apache Airflow (optionnel : pour dev hors docker)

1. Créer et accéder à un environnement virtuel avec cette commande.   
``` bash
python3 -m venv airflow_venv
source airflow_venv/bin/activate
```

2. Lancer ce script shell depuis l'e.v
```sh
AIRFLOW_VERSION=3.0.4
PYTHON_VERSION=3.9

pip install "apache-airflow==${AIRFLOW_VERSION}" \
  --constraint "https://raw.githubusercontent.com/apache/airflow/constraints-${AIRFLOW_VERSION}/constraints-${PYTHON_VERSION}.txt"
```

3. Verfier si l'installation a bien été effectuée sur l'e.v
 ```bash
 airflow version
 ```

### I - Configurer le projet

Lancer la commande `make secrets` à la racine du projet afin d'initializer les variables d'environnements. Il ne vous reste qu'à affecter les vraies valeurs par la suite.  
Note :   
- La clé API de coinbase doit avoir les permissions View + Trade (Obligatoire) 
- Les Webhooks Discord (Optionnels)

### II - Activer le webserver sur Docker

Il suffira d'executer sur docker depuis la racine du projet la commande : 
```bash
docker-compose up -d
``` 
Puis aller à ce lien http://localhost:8080/home avec les identifiants `airflow:airflow`.  
