import json
import requests
import pandas as pd
from sqlalchemy import create_engine
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.jobstores.sqlalchemy import SQLAlchemyJobStore
from datetime import datetime, timedelta
import sqlite3
from app import *

# url_datagouv = ("https://www.data.gouv.fr/fr/datasets/r/759b5ec2-a585-477a-9c62-7f74a7bdec3d")
url_ameli = "https://datavaccin-covid.ameli.fr/api/v2/catalog/datasets/donnees-de-vaccination-par-commune/exports/json?limit=-1&offset=0&timezone=UTC"
covid_json = "data/datacovid.json"
covid_json = "data/datacovid_ameli.json"


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
        # Comparaison des dates de chaque entrée avec la dernière date de màj (la veille puisque ce programme est lancé 1 fois par jour) et stockage des nouvelles données
        # 🐽🐽🐽 Une autre solution est de prendre la dernière date d'ajout de l'ancien json ou dans la db (mais si on prend dans la db -> risque d'entrer en conflit avec l'utilisateur) 🐽🐽🐽
        old_date = datetime.today() - timedelta(days=1)
        # 🐽🐽🐽🐽🐽🐽🐽🐽🐽🐽🐽🐽
        # 🐽🐽🐽 TEST MANUEL 🐽🐽🐽
        # old_date = datetime.strptime("2022-02-20", "%Y-%m-%d")
        for entry in data:
            if datetime.strptime(entry["date"], "%Y-%m-%d") > old_date:
                new_data.append(entry)
    except FileNotFoundError:
        # Stockage de toutes les données
        for entry in data:
            new_data.append(entry)
    # Ecrasement du fichier json
    with open(jsonpath, 'w', encoding='utf8') as jsonfile:
        json.dump(data, jsonfile, indent=4)

    return new_data


def update_db(data):
    """ 🐽🐽🐽 méthode avec create_engine : échec 
    /!\ car CONFLIT SQLAlchemy / Pandas (même avec la version 1.4.32 de sqlalchemy installée)
    # Create A DataFrame From the JSON Data
    df = pd.DataFrame(data)
    #Conversion en une db
    engine = create_engine("sqlite:///DataViewer.db")
    df.to_sql("test_table_covid",engine)"""
    # ETAPE SUIVANTE = AJOUT DES NOUVELLES DONNEES DANS LA DB
    # en procédant de cette manière, n'influe pas sur les ajouts/suppressions/modifications des users
    # conn = sqlite3.connect(db)
    # c = conn.cursor()
    for dic in data:
        date_reference = dic["date_reference"]
        semaine_injection = dic["semaine_injection"]
        commune_residence = dic["commune_residence"]
        libelle_commune = dic["libelle_commune"]
        population_carto = dic["population_carto"]
        classe_age = dic["classe_age"]
        libelle_classe_age = dic["libelle_classe_age"]
        effectif_1_inj = dic["effectif_1_inj"]
        effectif_termine = dic["effectif_termine"]
        effectif_cumu_1_inj = dic["effectif_cumu_1_inj"]
        effectif_cumu_termine = dic["effectif_cumu_termine"]
        taux_1_inj = dic["taux_1_inj"]
        taux_termine = dic["taux_termine"]
        taux_cumu_1_inj = dic["taux_cumu_1_inj"]
        taux_cumu_termine = dic["taux_cumu_termine"]
        date = dic["date"]

        data = DATA_COVID(date_reference=date_reference,
                          semaine_injection=semaine_injection,
                          commune_residence=commune_residence,
                          libelle_commune=libelle_commune, population_carto=population_carto, classe_age=classe_age,
                          libelle_classe_age=libelle_classe_age, effectif_1_inj=effectif_1_inj,
                          effectif_termine=effectif_termine,
                          effectif_cumu_1_inj=effectif_cumu_1_inj, effectif_cumu_termine=effectif_cumu_termine,
                          taux_1_inj=taux_1_inj, taux_termine=taux_termine, taux_cumu_1_inj=taux_cumu_1_inj,
                          taux_cumu_termine=taux_cumu_termine,
                          date=date)

        db.session.add(data)
        db.session.commit()


# SYNCHRONISATION
# Créer un objet Scheduler pour une tâche programmée
scheduler = BackgroundScheduler()
# Ajouter une tâche programmée à l'ordonnanceur (mise à jour des données depuis datagouv + mise à jour de base de données)
# Définition de l'intervalle : tous les jours
scheduler.add_job(update_db(update_data_covid(url_ameli, covid_json)), 'interval', days=1)
#  Démarrer le travail du planificateur de tâches programmé 
scheduler.start()

""" 
/!\ POUR L'INSTANT : scheduler renvoie une erreur
Mais les tâches marchent, et la db se met à jour
(YOUPI ! VICTOIRE !!!!)
"""
# new_data = update_data_covid(url_ameli, covid_json)
# update_db(new_data)
