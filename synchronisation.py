import json
import requests
import pandas as pd
from sqlalchemy import create_engine
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.jobstores.sqlalchemy import SQLAlchemyJobStore
from datetime import datetime

# On utilise le lien data gouv plutôt que le lien de l'API ameli
# car on peut comparer plus facilement avec la clé "recordid"
# (L'API ameli ne renvoie que les champs et leur valeur)
url_datagouv = ("https://www.data.gouv.fr/fr/datasets/r/759b5ec2-a585-477a-9c62-7f74a7bdec3d")
# url_ameli = "https://datavaccin-covid.ameli.fr/api/v2/catalog/datasets/donnees-de-vaccination-par-commune/exports/json?limit=-1&offset=0&timezone=UTC"
covid_json = "data/datacovid.json"


# Mise à jour des données depuis data gouv
def update_data_covid(url, jsonpath):
    # Connexion à l'URL data gouv
    response = requests.get(url)
    # print(response.status_code)
    # Récupération des données
    data_text = response.text
    # Conversion des données au format json
    data = json.loads(data_text)
    # Comparaison des nouvelles données avec les données téléchargées la veille :
    new_data = []
    try:
        # Téléchargement du fichier json de la veille
        with open(jsonpath) as jsonfile:
            old_data = json.load(jsonfile)
        # Comparaison des id de chaque entrée avec les entrées du fichier de la veille et stockage des nouvelles données
        old_recordids = [entry["recordid"] for entry in old_data]
        for entry in data:
            if entry["recordid"] not in old_recordids:
                print(entry)
                new_data.append(entry["fields"])
        print(new_data)
    except FileNotFoundError:
        # Stockage de toutes les données
        for entry in data:
            new_data.append(entry["fields"])
    # Ecrasement du fichier json
    with open(jsonpath, 'w', encoding='utf8') as jsonfile:
        json.dump(data, jsonfile, indent=4)

    return new_data


def update_db(new_data):
    # ETAPE SUIVANTE = AJOUT DES NOUVELLES DONNEES DANS LA DB
    # en procédant de cette manière, n'influe pas sur les ajouts/suppressions/modifications des users
    """ ******************************************************************
    /!\ PAS REUSSI CAR CONFLIT SQLAlchemy / Pandas (même avec la version 1.4.32 de sqlalchemy installée ---> peut-être que ça marche chez vous
    # Create A DataFrame From the JSON Data
    df = pd.DataFrame(data)
    #Conversion en une db
    engine = create_engine("sqlite:///data/DataViewer.db")
    df.to_sql("test_table_covid",engine)"""
    pass


# Créer un objet Scheduler pour une tâche programmée
scheduler = BackgroundScheduler()
# Ajouter une tâche programmée à l'ordonnanceur (mise à jour des données depuis datagouv + mise à jour de base de données)
# Définition de l'intervalle : tous les jours
scheduler.add_job(update_db(update_data_covid(url_datagouv, covid_json)), 'interval', days=1)
#  Démarrer le travail du planificateur de tâches programmé 
scheduler.start()
