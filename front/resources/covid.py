from inspect import BoundArguments
from flask import Blueprint, request, flash, redirect, render_template, session, url_for
from front.models.api import get_all_covid, get_covid_by_id, get_multiple_info, add_covid

covid = Blueprint('covid', __name__)


# Afficher et rechercher des données
@covid.route('/data',methods=('GET', 'POST'))
def data():
    if request.method == 'POST':
        body_data = request.form.to_dict() # récupère toutes les champs du formulaire
        # Récupération des champs pour lesquels une valeur est saisie uniquement
        # + Mise en forme au format de requête HTML
        # Exemple : {'libelle_commune': 'ANTONY', 'population_carto':14810}
        #          --> libelle_commune=ANTONY&population_carto=14810
        html_params = ""
        for k,v in body_data.items():
            if v != '':
                if html_params != '':
                    html_params += "&"
                html_params += k + "=" + v
        api_resp = get_multiple_info(html_params)
        #code_resp = api_resp[0] # status code
        data_resp = api_resp # données covid au format json
        if len(data_resp) > 0:
            return render_template('data.html',output_data=data_resp, many=True)
        else:
            flash("Aucune donnée ne correspond à votre recherche")
            #flash("Aucune donnée ne correspond à votre recherche : %s"%status_code)
            return render_template('data.html')
        
    elif request.method == 'GET':
        """ 
        # 🐽🐽🐽🐽🐽🐽🐽🐽🐽🐽🐽🐽🐽🐽🐽🐽🐽🐽🐽🐽🐽🐽🐽🐽🐽🐽🐽🐽🐽🐽🐽🐽🐽🐽
        # POUR RECUPERER TOUTES LES DONNEES (ce qu'on devrait mettre par défaut) : 
        # ----> FREEZE LE PC :( peut-être voir si il existe un truc pour envoyer les données par paquets plutôt que tout d'un coup ?
        api_resp = get_all_covid() #retourne toutes les données covid par défaut
        code_resp = api_resp[0] # status code
        data_resp = api_resp[1] # les données covid au format json
        return render_template('data.html', output_data=data_resp, many=True)
        """ 
        # POUR RECUPERER 1 DONNEE A PARTIR DE SON ID : 
        api_resp = get_covid_by_id(str(500)) # TEST DE LA FONCTION SUR LA REQUETE POUR 1 DONNEE SUR l'ID 500
        code_resp = api_resp[0] # status code
        data_resp = api_resp[1] # une donnée covid au format json
        #print("one data",data_resp)
        return render_template('data.html', output_data=data_resp, many=False)

# Créer une nouvelle donnée
@covid.route('/data/new',methods=('GET', 'POST'))
def add_data():
    if request.method == 'POST':
        # 🐽🐽🐽🐽🐽🐽🐽🐽🐽🐽🐽🐽🐽🐽🐽🐽🐽🐽🐽🐽🐽🐽🐽🐽🐽
        # PLAGIER SEIGNEUR ET AJOUTER TOKEN DANS HEADER !!!!!!!!!!!!!!!!!!!!!!!!!!!!
        # SINON RENVOIE 'Token is missing !!'
        data_json = request.form.to_dict()
        api_resp = add_covid(data_json)
        print("API_RESP:" + str(api_resp))

        # 🐽🐽🐽🐽🐽🐽🐽🐽🐽🐽🐽🐽🐽🐽🐽🐽🐽🐽🐽🐽🐽🐽🐽🐽🐽
        # FAIRE UN IF SUR LE STATUS CODE :
        #code_resp = api_resp[0] # status code
        #data_resp = api_resp[1] # une donnée covid au format json
        #flash("Donnée ajoutée")
        #flash("Impossible de créer une donnée à partir de votre saisie")
        #(on pourrait aussi mettre des conditions sur les champs du formulaire)
        return render_template('add_data.html', output_data=api_resp)
    elif request.method == 'GET':
        return render_template('add_data.html')