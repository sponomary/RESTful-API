from flask import Blueprint
from flask_login import logout_user
from flask import request, jsonify, make_response
from werkzeug.security import generate_password_hash, check_password_hash
import jwt
from datetime import datetime, timedelta
import functools
from flask import (Blueprint, flash, g, redirect, render_template, request, session, url_for)

from front.models.api import login_api,create_client


users = Blueprint('users', __name__)

@users.route('/register', methods=('GET', 'POST'))
def register():
    if request.method == 'POST':
        data_json = request.form.to_dict()
        # on obtient : data_json = {'name':name, 'email':email, 'password':password}
        api_resp = create_client(data_json)
        code_resp = api_resp['status']
        data_response = api_resp['message']

        if code_resp != 201 :
            # déjà un compte ---> login
            flash("error: %s"%code_resp)
            return redirect(url_for("users.login"))
        else:
            flash("Successfully registered: %s"%code_resp)
            return redirect(url_for("users.login"))
            # CHANGER ICI
            # renvoyer vers une page qui dit ok bien inscrit + faire en sorte que l'utilisateur soit connecté
            # Erreur "no secret key was set" à résoudre
    return render_template('register.html') #GET --> page d'inscription


@users.route('/login', methods=('GET', 'POST'))
def login():
    data_response = {}
    if request.method == 'POST':
        data_json = request.form.to_dict()
        # on obtient : data_json = {'email':email, 'password':password}
        api_resp = login_api(data_json)
        code_resp = api_resp['status']
        data_response = api_resp['message']

        if code_resp in [200, 201]:
            """
            session.clear()
            session['user_id'] = data_response['data']['id']
            session['token'] = data_response['token']
            session['client'] = data_response['data']
            g.client = data_response['data']
            return redirect(url_for('contributions.index'))
            """
            print("connection réussie")
            return redirect(url_for('home'))
            # CHANGER ICI
            # faire en sorte que l'utilisateur soit connecté
        else:
            print("error")
            """
            message_login = data_response['message']
            return render_template('authcepty/login.html', api_error=True, 
                                    api_message=message_login)
            """

    elif request.method == 'GET':
        return render_template('login.html', api_error=False)
    else: flash(error)



