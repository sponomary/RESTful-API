from flask import Blueprint, request, flash, redirect, render_template, session, url_for

from front.models.api import login_api,create_client

users = Blueprint('users', __name__)

@users.route('/register', methods=('GET', 'POST'))
def register():
    if request.method == 'POST':
        data_json = request.form.to_dict()
        # on obtient : data_json = {'name':name, 'email':email, 'password':password}
        api_resp = create_client(data_json)
        # on obtient : api_resp = {'message':message, 'status':status, 'user':email}
        # + si connexion réussie 'token':token
        status_code = api_resp['status']
        message = api_resp['message']

        if status_code != 201 :
            print("error")
            flash("Error : %s"%message)
            return redirect(url_for("users.login"))
        else:
            flash("Inscription et connexion réussies : %s"%status_code)
            return redirect(url_for("home"))
            # CHANGER ICI
            # renvoyer vers une page qui dit ok bien inscrit + faire en sorte que l'utilisateur soit connecté
            # Erreur "no secret key was set" à résoudre
    return render_template('register.html') #GET --> page d'inscription

@users.route('/login', methods=('GET', 'POST'))
def login():
    if request.method == 'POST':
        data_json = request.form.to_dict()
        # on obtient : data_json = {'email':email, 'password':password}
        api_resp = login_api(data_json)
        # on obtient : api_resp = {'message':message, 'status':status, 'user':email}
        # + si connexion réussie 'token':token
        status_code = api_resp['status']
        message = api_resp['message']
        user = api_resp['user']
        
        if status_code in [200, 201]:
            token = api_resp['token']
            session.clear()
            session['user'] = user
            session['token'] = token
            flash("Connexion réussie : %s"%status_code)
            return redirect(url_for('home')) # CHANGER ICI, faire en sorte que l'utilisateur soit connecté
        else:
            flash("Error : %s"%message)
            return render_template('login.html')

    elif request.method == 'GET':
        return render_template('login.html')
        # logged_in=current_user.is_authenticated)
    else: flash(error) # pas sûre de ce else (????????????????????????????????)

@users.route('/logout')
def logout():
    session.clear()
    print("déconnexion réussie")
    return redirect(url_for('home'))