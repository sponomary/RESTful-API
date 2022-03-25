#!/usr/bin/python3
# coding: utf-8

"""
    M2 TAL, INGÉNIERIE MULTILINGUE : TECHNIQUES WEB (REST API)
    -------------------------------------------
    Ce module lance l'API. 
    :copyright: © 2022 by Élise & Lufei & Alexandra.
"""

__version__ = "1.0"

from flask import Flask, redirect, url_for, render_template
from resources.user import users
from resources.covid import covid
from models.db import initialize_db, initialize_marshmallow
from lib.scheduler import start_scheduler


app = Flask(__name__)

#Blueprint
app.register_blueprint(users)
app.register_blueprint(covid, url_prefix='/covid')

app.config['DEBUG'] = True
app.config['SERVER_NAME'] = 'dataviewer.api.localhost:5000'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data/DataViewer.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config.update({'SCHEDULER_API_ENABLED': True})

initialize_db(app)
initialize_marshmallow(app)
start_scheduler(app)


# Page d'accueil
@app.route('/')
def home():
    return redirect(url_for('readme'))

@app.route('/readme')
def readme():
    return render_template('README.html')
    

if __name__ == "__main__":
    #app.run(host='127.0.0.1', port=5001)
    app.run()
