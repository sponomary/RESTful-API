#!/usr/bin/python3
# coding: utf-8

"""
    M2 TAL, INGÉNIERIE MULTILINGUE : TECHNIQUES WEB (REST API)
    -------------------------------------------
    Ce module front permet d'inscrire et connecter des utilisateurs.
    :copyright: © 2022 by Élise & Lufei & Alexandra.
"""

from flask import Blueprint, request, flash, redirect, render_template, session, url_for
from front.models.api import login_api,create_client
import functools

users = Blueprint('users', __name__)

# Inscription
@users.route('/register', methods=('GET', 'POST'))
def register():
    # POST: récupère les informations du formulaire
    if request.method == 'POST':
        data_json = request.form.to_dict()
        # on obtient : data_json = {'name':name, 'email':email, 'password':password}
        api_resp = create_client(data_json)
        # on obtient : api_resp = {'message':message, 'status':status, 'email':email}
        # + si connexion réussie 'token':token
        status_code = api_resp['status']
        message = api_resp['message']

        if status_code != 201 :
            # L'utilisateur a déjà un compte --> renvoie la page de connexion
            print("error")
            flash("Error : %s"%message)
            return redirect(url_for("users.login"))
        else:
            # Création du nouvel utilisateur + connexion automatique
            token = api_resp['token']
            user = api_resp['email']
            session.clear()
            session['user'] = user
            session['token'] = token
            flash("Inscription et connexion réussies : %s"%status_code)
            return redirect(url_for("home"))
    # GET: renvoie la page d'inscription
    return render_template('register.html')

# Connexion
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
            return redirect(url_for('home'))
        else:
            flash("Error : %s"%message)
            return render_template('login.html')

    elif request.method == 'GET':
        return render_template('login.html')


# Déconnexion
@users.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('home'))

# Token
def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if 'user' not in session:
            session.clear()
            return redirect(url_for('users.login'))
        return view(session['token'], **kwargs)
    return wrapped_view