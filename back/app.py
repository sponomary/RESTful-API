#!/usr/bin/python3
# coding: utf-8

"""
    M2 TAL, INGÉNIERIE MULTILINGUE : TECHNIQUES WEB (REST API)
    -------------------------------------------
    Ce module lance l'API. 
    :copyright: © 2022 by Élise & Lufei & Alexandra.
"""

__version__ = "1.0"

from flask import Flask
from .resources.user import users
from .resources.covid import covid
from .models.db import initialize_db, initialize_marshmallow
from .lib.scheduler import start_scheduler

dataviewerBack = Flask(__name__)

# Blueprint
dataviewerBack.register_blueprint(users)
dataviewerBack.register_blueprint(covid, url_prefix='/covid')

dataviewerBack.config['DEBUG'] = True
dataviewerBack.config['SERVER_NAME'] = 'dataviewer.api.localhost:5000'
dataviewerBack.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data/DataViewer.db'
dataviewerBack.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
dataviewerBack.config.update({'SCHEDULER_API_ENABLED': True})

initialize_db(dataviewerBack)
initialize_marshmallow(dataviewerBack)
start_scheduler(dataviewerBack)
