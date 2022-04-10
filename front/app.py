#!/usr/bin/python3
# coding: utf-8

"""
    M2 TAL, INGÉNIERIE MULTILINGUE : TECHNIQUES WEB (REST API)
    -------------------------------------------
    Ce module lance l'API. 
    :copyright: © 2022 by Élise & Lufei & Alexandra.
"""

__version__ = "1.0"

from flask import Flask, render_template
from flask_bootstrap import Bootstrap
from flask_cors import CORS
from .resources.user import users
from .resources.covid import covid
from flask import Flask, session
from flask_session import Session
import os

__all__ = ['dataviewerFront']

dataviewerFront = Flask(__name__)

# Blueprint
dataviewerFront.register_blueprint(users)
dataviewerFront.register_blueprint(covid, url_prefix='/covid')

dataviewerFront.config['DEBUG'] = True

# Pour la connexion et les sessions des utilisateurs
dataviewerFront.config['SESSION_TYPE'] = 'filesystem'
dataviewerFront.config["PERMANENT_SESSION_LIFETIME"] = 1800
dataviewerFront.config["SECRET_KEY"] = "dataviewerSecretKey2022"
dataviewerFront.config['SERVER_NAME'] = 'dataviewer.localhost:5000'

sess = Session(dataviewerFront)
sess.init_app(dataviewerFront)

dataviewerFront.add_url_rule('/', endpoint='home')

# Page d'accueil
@dataviewerFront.route('/')
def home():
    return render_template("home.html")
