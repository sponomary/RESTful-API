from flask import Blueprint, request, flash, redirect, render_template, session, url_for

from front.models.api import get_all_covid, get_covid_by_id

covid = Blueprint('covid', __name__)

@covid.route('/data',methods=('GET', 'POST'))
def data():
    if request.method == 'POST':
        print("POST A COMPLETER")
        render_template('data.html')
    elif request.method == 'GET':
        #api_resp = get_all_covid() #retourne toutes les données covid par défaut
        api_resp = get_covid_by_id(str(500)) # TEST DE LA FONCTION SUR LA REQUETE POUR 1 DONNEE
        return render_template('data.html',output_data=api_resp, many=False)