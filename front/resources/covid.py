from inspect import BoundArguments
from flask import Blueprint, request, flash, redirect, render_template, session, url_for
from front.models.api import get_all_covid, get_covid_by_id, get_multiple_info

covid = Blueprint('covid', __name__)


@covid.route('/data',methods=('GET', 'POST'))
def data():
    if request.method == 'POST':
        print("POST A COMPLETER")
        render_template('data.html')
    elif request.method == 'GET':
        #api_resp = get_all_covid() #retourne toutes les données covid par défaut
        api_resp = get_covid_by_id(str(500)) # TEST DE LA FONCTION SUR LA REQUETE POUR 1 DONNEE
        code_resp = api_resp[0] # status code
        data_response = api_resp[1] # une donnée covid au format json
        print("one data",data_response)
        return render_template('data.html', 
                                    output_data=data_response, many=False)
    

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
