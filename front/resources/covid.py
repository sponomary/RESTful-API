from cmath import log
from inspect import BoundArguments
from flask import Blueprint, request, flash, redirect, render_template, session, url_for
from back.resources.covid import delete_covid
from front.models.api import get_all_covid, get_covid_by_id, get_multiple_info, add_covid, update_covid, delete_covid
from front.resources.user import login_required

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
        data_resp = api_resp # résultat de la requête
        if len(data_resp) > 0:
            return render_template('data.html',output_data=data_resp, many=True)
        else:
            flash("Aucune donnée ne correspond à votre recherche")
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


# Afficher les données par paquet
@covid.route('/data/search',methods=('GET', 'POST'))
def data_seperation():    
    if request.method == 'POST':
        # 🐽🐽🐽🐽🐽🐽🐽🐽🐽🐽🐽🐽🐽🐽🐽🐽🐽🐽🐽🐽🐽🐽🐽🐽🐽🐽🐽🐽🐽🐽🐽🐽🐽🐽
        # concrètement j'ai plagié ton code magnifique
        # 🐽🐽🐽🐽🐽🐽🐽🐽🐽🐽🐽🐽🐽🐽🐽🐽🐽🐽🐽🐽🐽🐽🐽🐽🐽🐽🐽🐽🐽🐽🐽🐽🐽🐽
        body_data = request.form.to_dict() # récupère toutes les champs du formulaire
        # Récupération des champs pour lesquels une valeur est saisie uniquement
        # + Mise en forme au format de requête HTML
        # Exemple : {'libelle_commune': 'ANTONY', 'population_carto':14810}
        #          --> libelle_commune=ANTONY&population_carto=14810
        print(body_data)
        html_params = ""
        for k,v in body_data.items():
            if v != '':
                if html_params != '':
                    html_params += "&"
                html_params += k + "=" + v
        print("URL:",html_params)
        api_resp = get_all_covid(html_params) #retourne toutes les données covid par défaut
        code_resp = api_resp[0] # status code
        data_resp = api_resp[1] # les données covid au format json
        total_data_nb = api_resp[2] # 🐽🐽🐽🐽🐽🐽🐽 nombre total des données dans BD, comment affciher ça sur notre page ? 🐽🐽🐽🐽🐽🐽🐽
        return render_template('all.html', output_data=data_resp, nb=total_data_nb, many=True)
    
    elif request.method == 'GET':
        return render_template('all.html')

# Créer une nouvelle donnée
@covid.route('/data/new',methods=('GET', 'POST'))
@login_required
def add_data(token):
    if request.method == 'POST':
        data_json = request.form.to_dict()
        api_resp = add_covid(token,data=data_json)
        code_resp = api_resp[0] # status code
        data_resp = api_resp[1] # une donnée covid à ajoutée au format json
        if code_resp not in [200, 201]:
            flash('Veuillez vous connecter.')
            return redirect(url_for('users.login'))
        # 🐽🐽🐽🐽🐽🐽🐽🐽🐽🐽🐽🐽🐽🐽🐽🐽🐽🐽🐽🐽🐽🐽🐽🐽🐽
        # si on veut écrire des trucs
        #flash("Donnée ajoutée")
        #flash("Impossible de créer une donnée à partir de votre saisie")
        #(on pourrait aussi mettre des conditions sur les champs du formulaire pour pas que l'utilisateur saisisse n'importe quoi)
        return render_template('add_data.html', output_data=data_resp)
    elif request.method == 'GET':
        return render_template('add_data.html')

# Modifier une donnée
@covid.route('/data/update',methods=('GET', 'POST'))
@login_required
def update_data(token):
    if request.method == 'POST':
        if 'id_data_to_update' in request.form:
            id = request.form.get('id_data_to_update')
            api_resp = get_covid_by_id(id)
            code_resp = api_resp[0]
            data_resp = api_resp[1]
            if data_resp == {}:
                flash("Error: Il n'existe pas de donnée d'identifiant "+str(id))
                return render_template('update_data.html')
            return render_template('update_data.html', output_data=data_resp, id=str(id))
        else:
            data_json = request.form.to_dict()
            id = request.form.get('id')
            api_resp = update_covid(token,id,data=data_json)
            code_resp = api_resp[0] # status code
            data_resp = api_resp[1] # une donnée covid à ajoutée au format json
            if code_resp not in [200, 201]:
                flash('Veuillez vous connecter.')
                return redirect(url_for('users.login'))
            # 🐽🐽🐽🐽🐽🐽🐽🐽🐽🐽🐽🐽🐽🐽🐽🐽🐽🐽🐽🐽🐽🐽🐽🐽🐽
            # si on veut écrire des trucs
            #flash("Donnée modifiée")
            #flash("Impossible de modifier la donnée à partir de votre saisie")
            #(on pourrait aussi mettre des conditions sur les champs du formulaire pour pas que l'utilisateur saisisse n'importe quoi)
            return render_template('update_data.html', output_data=data_resp, id_updated=id)
    elif request.method == 'GET':
        return render_template('update_data.html')

# Supprimer une donnée
@covid.route('/data/delete',methods=('GET', 'POST'))
@login_required
def delete_data(token):
    if request.method == 'POST':
        if 'id_data_to_delete' in request.form:
            id = request.form.get('id_data_to_delete')
            api_resp = get_covid_by_id(id)
            code_resp = api_resp[0]
            data_resp = api_resp[1]
            if data_resp == {}:
                flash("Error: Il n'existe pas de donnée d'identifiant "+str(id))
                return render_template('delete_data.html')
            return render_template('delete_data.html', output_data=data_resp, id=str(id))
        else:
            id = request.form.get("id")
            api_resp = delete_covid(token,id)
            code_resp = api_resp[0] # status code
            data_resp = api_resp[1] # une donnée covid supprimée au format json
            if code_resp not in [200, 201]:
                flash('Veuillez vous connecter.')
                return redirect(url_for('users.login'))
            return render_template('delete_data.html', output_data=data_resp, id_deleted=id)
    elif request.method == 'GET':
        return render_template('delete_data.html')