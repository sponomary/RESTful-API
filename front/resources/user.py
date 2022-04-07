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
        data = dict(request.form)
        api_resp = create_client(data)
        print(api_resp)
        code_resp = api_resp[0]
        data_response = api_resp[1]

        if code_resp != 201 :
            flash("error: %s"%code_resp)
            render_template('user/README.html', api_error=True,
                            api_message=data_response['message'])
        else:
            return ("mettre la page login")
            #return redirect(url_for('authcepty.login'), api_error=False)

    return render_template('user/register.html')


@users.route('/login', methods=('GET', 'POST'))
def login():
    data_response = {}
    if request.method == 'POST':
        username = request.form['email'] 
        password = request.form['password']
        api_resp = login_api(username, password)
        print(api_resp)
        code_resp = api_resp[0]
        data_response = api_resp[1]

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
        else:
            print("error")
            """
            message_login = data_response['message']
            return render_template('authcepty/login.html', api_error=True, 
                                    api_message=message_login)
            """

    elif request.method == 'GET':
        print("une mini étape réussi ! ")
        return render_template('user/README.html', api_error=False)
    else: flash(error)



