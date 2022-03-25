#!/usr/bin/python3
# coding: utf-8

import json
from datetime import datetime
import requests
from app import *
from sqlalchemy import desc
from models.covid import DataCovidModel, DataCovidSchema
from models.db import db, ma #on utilise ma ici ? 🐽
from resources.user import * #? 🐽
from resources.covid import * #? 🐽


# URL permanent pour import total dans une BDD vide
URL_PERMANENT = "https://www.data.gouv.fr/fr/datasets/r/759b5ec2-a585-477a-9c62-7f74a7bdec3d"
# Dataset à interroger pour la synchronisation
ENDPOINT_API_AMELI = "https://datavaccin-covid.ameli.fr/api/records/1.0/search/?dataset=donnees-de-vaccination-par-commune&q="


# ============ Initialisation ============
def init_via_url_permanente():
    """
    Récupération des données à partir du lien permanent du site de data.gouv.fr pour l'initialisation complète de la BDD.
    :return: les données au format JSON
    """
    # Connexion à l'URL data.gouv
    print("Connection à l'URL data.gouv.fr en cours...")
    response = requests.get(URL_PERMANENT)
    print(response.status_code)  # 200 si succès

    # Récupération des données
    data_text = response.text

    # Conversion des données au format json
    return json.loads(data_text)


def init_full_bdd():
    """
    Initialisation complète de la BDD à partir des données récupérées via lien permanent du site de data.gouv.fr.
    """
    json_covid = init_via_url_permanente()

    try:
        print("Initialisation complète en cours...")
        read_json_url_data_gouv(json_covid)  # initialisation de la BDD avec le JSON
    except Exception as e:
        print(e)
        pass


def read_json_url_data_gouv(donnees):
    """
        Enregistrement d'un JSON en BDD au format récupéré du lien permanent.
        :param donnees: les données en format JSON pour insérer dans la BDD
    """
    for dic_data in donnees:
        # Utilisation d'un `defaultdict` pour éviter les `KeyError` si le champs est manquant dans le JSON
        update_db(dic_data["fields"])


# ============ MISE A JOUR ============
def differ_api_ameli(date_voulue):
    """
    Appel différentiel de l'API AMELI pour récupérer seulement les nouvelles données en utilisant le critère de date.
    URL : https://datavaccin-covid.ameli.fr/explore/dataset/donnees-de-vaccination-par-commune/api/
    Génération de la clé API : https://data.opendatasoft.com/
    :param date_voulue: la date à partir de laquelle on veut de mettre à jour la BDD
    :return: les données au format JSON
    """
    # Initialisation des différents éléments qui vont constituer notre URL/requête
    requete = "date>" + str(date_voulue) + "&rows=5000"  # ajout d'un paramètre sur la date
    AMELI_URL = ENDPOINT_API_AMELI + requete
    AMELI_API_KEY = "e9a377dea52545f74ec78efe79513f8466bee6be8fead520c362a5ad"  # clé API pour se connecter à l'API
    headers = {"appid": AMELI_API_KEY}

    print("Appel de l'API AMELI en cours...")
    response = requests.get(AMELI_URL, params=headers)  # appel de l'API
    response.raise_for_status()
    return response.json()


def differ_maj_bdd():
    """
    Interrogation de l'API pour récupérer seulement les nouvelles données (flux différentiel) pour mettre à jour la BDD.
    """
    # Récupération de la dernière date dans la BDD à partir de laquelle on veut mettre à jour
    last_data = DataCovidModel.query.order_by(desc(DataCovidModel.date)).first()
    json_covid = differ_api_ameli(last_data.date)  # appel de l'API pour récupérer les nouvelles données

    try:
        print("Mise à jour en cours...")
        read_json_api_ameli(json_covid)  # Mise à jour de la BDD avec le JSON
    except Exception as e:
        print(e)
        pass


def read_json_api_ameli(donnees):
    """
    Enregistrement d'un JSON en BDD au format de l'API AMELI.
    """
    for dic_data in donnees["records"]:
        update_db(dic_data["fields"])


def get_champs_date(dic, champs):
    """
    L'envoi de la valeur None pour les données de dates manquantes.
    :param dic: les données à tester
    :param champs: les colonnes à tester
    :return: valeur pour une case prête à être insérée
    """
    if champs in dic:
        return datetime.strptime(dic[champs], "%Y-%m-%d").date()
    else:
        return None


def get_champs(dic, champs):
    """
    L'envoi de la valeur None pour les données manquantes.
    :param dic: les données à tester
    :param champs: les colonnes à tester
    :return: valeur pour une case prête à être insérée
    """
    if champs in dic:
        return dic[champs]
    else:
        return None


def update_db(dic):
    """
    Mise à jour de la BDD avec le dictionnaire.
    :param dic: les données à insérer
    """
    date_reference = get_champs_date(dic, "date_reference")
    semaine_injection = get_champs(dic, "semaine_injection")
    commune_residence = get_champs(dic, "commune_residence")
    libelle_commune = get_champs(dic, "libelle_commune")
    population_carto = get_champs(dic, "population_carto")
    classe_age = get_champs(dic, "classe_age")
    libelle_classe_age = get_champs(dic, "libelle_classe_age")
    effectif_1_inj = get_champs(dic, "effectif_1_inj")
    effectif_termine = get_champs(dic, "effectif_termine")
    effectif_cumu_1_inj = get_champs(dic, "effectif_cumu_1_inj")
    effectif_cumu_termine = get_champs(dic, "effectif_cumu_termine")
    taux_1_inj = get_champs(dic, "taux_1_inj")
    taux_termine = get_champs(dic, "taux_termine")
    taux_cumu_1_inj = get_champs(dic, "taux_cumu_1_inj")
    taux_cumu_termine = get_champs(dic, "taux_cumu_termine")
    date = get_champs_date(dic, "date")

    data = DataCovidModel(date_reference=date_reference,
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


# ============ SYNCHRONISATION ============
# MIS DANS LE SCHEDULER DANS APP.PY (à compléter pour la condition)
# Si la BDD est vide
# init_full_bdd()

# Pour mettre à jour la base existante
differ_maj_bdd()