from inspect import BoundArguments
from flask import Blueprint, request, flash, redirect, render_template, session, url_for
from front.models.api import get_all_covid, get_covid_by_id, get_multiple_info
import json
import re

covid = Blueprint('covid', __name__)


@covid.route('/data',methods=('GET', 'POST'))
def data():
    if request.method == 'POST':
        body_data = request.form.to_dict() # récupère toutes les champs du formulaire
        print("RES DU FORMULAIRE :",body_data)
        infos = {} # récupération des champs pour lesquels une valeur est saisie uniquement
        # Mise en forme au format de requête HTML
        # Exemple : {'libelle_commune': 'ANTONY', 'population_carto':14810}
        #          --> libelle_commune=ANTONY&population_carto=14810
        html_params = ""
        for k,v in body_data.items():
            if v != '':
                if html_params != '':
                    html_params += "&"
                html_params += k + "=" + v
        print("NETTOYE :", infos)
        print("STRING HTML :", html_params)
        
        #ERREUR QUELQUE PART CI DESSOUS
        api_resp = get_multiple_info(html_params)
        code_resp = api_resp[0] # status code
        data_response = api_resp[1] # une donnée covid au format json
        print("searching result : ",data_response)
        render_template('data.html',output_data=data_response, many=False)
        
    elif request.method == 'GET':
        """ 
        # POUR RECUPERER 1 DONNEE A PARTIR DE SON ID : 
        # ----> FREEZE LE PC :( peut-être voir si il existe un truc pour envoyer les données par paquets plutôt que tout d'un coup ?
        api_resp = get_all_covid() #retourne toutes les données covid par défaut
        code_resp = api_resp[0] # status code
        data_response = api_resp[1] # les données covid au format json
        return render_template('data.html', output_data=data_response, many=True)
        """ 
        # POUR RECUPERER 1 DONNEE A PARTIR DE SON ID : 
        api_resp = get_covid_by_id(str(500)) # TEST DE LA FONCTION SUR LA REQUETE POUR 1 DONNEE SUR l'ID 500
        code_resp = api_resp[0] # status code
        data_response = api_resp[1] # une donnée covid au format json
        #print("one data",data_response)
        return render_template('data.html', output_data=data_response, many=False)

@covid.route('/data/filter',methods=('GET', 'POST'))
def data_filter():
    if request.method == 'POST':
        print("chercher infos par filtrage")
        body_data = dict(request.form) # retour : {'libelle_commune': 'ANTONY'}
        # faut formuler une string comme ca pour passer à la fonction get_multiple_info: 
        # libelle_commune=ANTONY&population_carto=14810
        print(body_data)
        # info = quelque chose comme libelle_commune=ANTONY&population_carto=14810
        api_resp = get_multiple_info(info) # TEST DE LA FONCTION SUR LA REQUETE POUR 1 DONNEE
        code_resp = api_resp[0] # status code
        data_response = api_resp[1] # une donnée covid au format json
        print("searching result : ",data_response)
        render_template('data.html',output_data=data_response, many=False)

    elif request.method == 'GET':
        pass
        # toujours besoin de méthode GET ici ? 
