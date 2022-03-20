import json
import requests
import pandas as pd
from sqlalchemy import create_engine
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.jobstores.sqlalchemy import SQLAlchemyJobStore
from datetime import datetime, timedelta
import http.client
import sqlite3
from app import *

# url_datagouv = ("https://www.data.gouv.fr/fr/datasets/r/759b5ec2-a585-477a-9c62-7f74a7bdec3d")
# url_ameli = "https://datavaccin-covid.ameli.fr/api/v2/catalog/datasets/donnees-de-vaccination-par-commune/exports/json?limit=-1&offset=0&timezone=UTC"
covid_json = "data/datacovid.json"
covid_json = "data/datacovid_ameli.json"


def call_api_covid(date_derniere_donnees):
    # Initialisation des différents éléments qui vont constituer notre URL/requête
    AMELI_ENDPOINT = "https://datavaccin-covid.ameli.fr/api/records/1.0/search/?dataset=donnees-de-vaccination-par-commune&q="  # nom du dataset à interroger
    params = "date>2022-03-05&rows=1000"
    AMELI_ENDPOINT = AMELI_ENDPOINT + params
    AMELI_API_KEY = "e9a377dea52545f74ec78efe79513f8466bee6be8fead520c362a5ad"  # api_key pour se connecter à l'API
    headers = {"appid": AMELI_API_KEY}

    response = requests.get(AMELI_ENDPOINT, params=headers)
    response.raise_for_status()
    return response.json()


# Mise à jour des données depuis data gouv
def update_data_covid():
    # TODO : appliquer la requête avec SQLAlchemy pour extraire la dernière date de la BDD pour ensuite télécharger 
    #  les données qui ont été rajoutées dans l'API Ameli 
    date_derniere_donnees = "SELECT MAX(date) FROM DATA_COVID"  # chercher la dernière date dans la base de donnée
    json_covid = call_api_covid(date_derniere_donnees)  # appel de la fonction d'interrogation de l'API
    update_db(json_covid)  # mise à jour de la BD avec le JSON en retour


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
    # TODO adapter la structure de JSON à la structure de l'API : le JSON n'es pas la même tête quand téléchargé 
    #  manuellement et accédé via l'API 😅 Aucune idée pourquoi, déjà dans le cas de l'API il faut descendre plus 
    #  bas dans l'arborescence
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
# scheduler = BackgroundScheduler()
# Ajouter une tâche programmée à l'ordonnanceur (mise à jour des données depuis datagouv + mise à jour de base de données)
# Définition de l'intervalle : tous les jours
# scheduler.add_job(update_data_covid(url_ameli, covid_json), 'interval', days=1)
#  Démarrer le travail du planificateur de tâches programmé 
# scheduler.start()
update_data_covid()

""" 
/!\ POUR L'INSTANT : scheduler renvoie une erreur
Mais les tâches marchent, et la db se met à jour
(YOUPI ! VICTOIRE !!!!)
"""
# new_data = update_data_covid(url_ameli, covid_json)
# update_db(new_data)
