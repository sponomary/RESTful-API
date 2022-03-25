#!/usr/bin/python3
# coding: utf-8

"""
    M2 TAL, INGÉNIERIE MULTILINGUE : TECHNIQUES WEB (REST API)
    -------------------------------------------
    Ce module lance l'API. 
    :copyright: © 2022 by Élise & Lufei & Alexandra.
"""

# TODO :
# models : ok ✅
# resources.user : ok sauf logout --> toujours nécessaire ?
# resources.covid : tout marche ✅ 
# + semaine_injection (on laisse en string ou on change ce champ ?)
# nom du serveur ✅
# relier synchro et scheduler ✅ (initialisation ok si la table existe mais est vide / vérifier que ça synchro bien ?)
# Heroku (@sasha)
# que faire de ce code ?
"""
login_manager(app)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))
"""
# doc de notre code
# doc postman (✅ si ça vous va)
# readme
# equipe.txt
# page d'accueil, on met un truc comme les filles ?  peut être ajouter un lien vers la doc ou quoi ?
# vérifier les requirements
# quelque chose d'autre ?

__version__ = "0.6"

from flask import Flask
from resources.user import users
from resources.covid import covid
from models.db import initialize_db, initialize_marshmallow
from lib.scheduler import start_scheduler

app = Flask(__name__)

# Blueprint
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
    return "<h1>Groupe 1 : Elise LINCKER, Lufei LIU, Alexandra PONOMAREVA</h1>" \
           "<a href='https://documenter.getpostman.com/view/16846441/UVyn1JaA'>Lire la Documentation</a>"


if __name__ == "__main__":
    # app.run(host='127.0.0.1', port=5000)
    app.run()
