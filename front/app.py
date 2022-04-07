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

__all__ = ['dataviewerFront']

dataviewerFront = Flask(__name__)

# Blueprint
dataviewerFront.register_blueprint(users)
dataviewerFront.register_blueprint(covid, url_prefix='/covid')

dataviewerFront.config['DEBUG'] = True

#dataviewerFront.add_url_rule('/', endpoint='contributions.index')


# Page d'accueil
@dataviewerFront.route('/')
def home():
    return render_template("base.html")
