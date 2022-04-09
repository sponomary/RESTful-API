# coding: utf-8 


"""
    M2 TAL, INGÉNIERIE MULTILINGUE : TECHNIQUES WEB (REST API)
    -------------------------------------------
    Ce module lance l'API. 
    :copyright: © 2022 by Élise & Lufei & Alexandra.
"""

__version__ = "0.1"

import requests
import json
from os import environ

# -----------------------------------------------------------------------

HOST_API = "http://dataviewer.api.localhost:5000/api"
#HOST_API = "http://127.0.0.1:5000/api"
URL_LOGIN = HOST_API+"/login"
URL_USER_POST = HOST_API+"/register"
#URL_ALLDATA_GET = HOST_API+"/covid/" # URL qui retourne toutes les données covid 
URL_ALLDATA_GET = HOST_API+"/covid/?{data_range}" # URL qui retourne toutes les données covid par paquet 
URL_ONEDATA_GET_PATCH_DELETE = HOST_API+"/covid/{data_id}/" # URL qui retourne/met à jour/supprime une donnée covid
URL_ONEDATA_POST = HOST_API+"/covid/" # URL qui crée une nouvelle donnée covid 
URL_UNIQUE_INFO_GET = HOST_API+"/covid/{info}/" # URL qui permet de retourner toutes les données uniques de certains colonnes 
URL_MULTIPLE_INFO_GET = HOST_API+"/covid/search?{info}" # URL qui renvoie les résultats d'une requête (simple ou multiple)

# -----------------------------------------------------------------------

__all__ = ['login_api','create_client','get_all_covid','get_covid_by_id','update_covid','delete_covid','get_multiple_info','add_covid']

# -----------------------------------------------------------------------

def login_api(data):
    resp_api = requests.post(URL_LOGIN, data)
    return resp_api.json()

def create_client(data):
    resp_api = requests.post(URL_USER_POST, data)
    return resp_api.json()

# PB : fait freeze le pc car trop de données :(
def get_all_covid(data_range):
    # il faut que url passé à requests.get ressemble à ca : http://dataviewer.api.localhost:5000/api/covid/?start=1&limit=5
    print("REQUEST : "+URL_ALLDATA_GET.format(data_range = data_range))
    resp_api = requests.get(URL_ALLDATA_GET.format(data_range = data_range))
    print("CODE:",resp_api.status_code)
    print("RESP:",resp_api.json())
    return resp_api.status_code, resp_api.json()
    #resp_api = requests.get(URL_ALLDATA_GET)
    #return resp_api.status_code, resp_api.json()


# (?) peut-être on peut zapper ça car se fait direct dans la recherche si on remplit que le champ id (?) à voir
# Je suis d'accord pour enlever ça, ça rend plus prore ---lulu
def get_covid_by_id(id):
    print("GET COVID ID "+id)
    resp_api = requests.get(URL_ONEDATA_GET_PATCH_DELETE.format(data_id=id))
    print("RESP:",resp_api.json())
    print("code:",resp_api.status_code)
    return resp_api.status_code, resp_api.json()

def update_covid(id):
    print("UPDATE COVID ID "+id)
    resp_api = requests.get(URL_ONEDATA_GET_PATCH_DELETE.format(data_id=id))
    print("RESP:",resp_api.json())
    return resp_api.json()

def delete_covid(id):
    print("DELETE COVID ID "+id)
    resp_api = requests.get(URL_ONEDATA_GET_PATCH_DELETE.format(data_id=id))
    print("RESP:",resp_api.json())
    return resp_api.json()

# URL_ONEDATA_POST ---> créer une nouvelle donnée covid
def add_covid(token,data):
    print("ADD COVID DATA :"+str(data))
    headers = {"x-access-token": token}
    print("TOKEN:",token)
    resp_api = requests.post(URL_ONEDATA_POST,data,headers=headers)
    return resp_api.status_code,resp_api.json()

# URL_MULTIPLE_INFO_GET ---> exploiter le formulaire HTML
def get_multiple_info(search_info):
    print("REQUEST : "+URL_MULTIPLE_INFO_GET.format(info = search_info))
    resp_api = requests.get(URL_MULTIPLE_INFO_GET.format(info = search_info))
    print("RESP:",resp_api.json())
    return resp_api.json()
    #print("CODE",resp_api.status_code)
    #return resp_api.status_code,resp_api.json()


# URL_UNIQUE_INFO_GET ---> faire + tard car implique un nouveau tableau HTML et modifs jinja