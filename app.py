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
# lib.utils / app : relier synchro et apscheduler (@Lufei début de solu)
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
from flask_apscheduler import APScheduler
# import lib.synchronisation as synchro
from resources.user import users
from resources.covid import covid
from models.db import initialize_db, initialize_marshmallow, login_manager

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

"""
# On peut peut-être déplacer cette partie dans le fichier utils.py ? 
# PAS REUSSI A CAUSE DE LA LIGNE : scheduler.init_app(app)

+

RENVOIE UNE ERREUR lors de l'importation du script synchronisation
🐽🐽🐽🐽🐽🐽🐽🐽🐽🐽🐽🐽🐽🐽🐽🐽🐽🐽🐽🐽🐽🐽🐽🐽🐽🐽
"""
# Créer un objet Scheduler pour une tâche programmée
scheduler = APScheduler()
scheduler.init_app(app)


# Ajouter une tâche programmée à l'ordonnanceur (mise à jour des données depuis datagouv + mise à jour de base de données)
# @scheduler.task('interval', id='do_job', days=1)
def job():
    print("Synchronisation...")
    # Si la BDD est vide 🐽🐽🐽🐽🐽🐽
    # synchro.init_full_bdd()
    # Pour mettre à jour la base existante
    # synchro.differ_maj_bdd()
    print("...synchronisation terminée")


# Démarrer le travail du planificateur de tâches programmé
scheduler.start()


# 🐽🐽🐽🐽🐽🐽🐽🐽🐽🐽🐽🐽🐽🐽🐽🐽🐽🐽🐽🐽🐽🐽🐽🐽🐽🐽🐽🐽🐽🐽🐽
# juste copié Noélie pour la route de base
# 🐽🐽🐽🐽🐽🐽🐽🐽🐽🐽🐽🐽🐽🐽🐽🐽🐽🐽🐽🐽🐽🐽🐽🐽🐽🐽🐽🐽🐽🐽🐽
# Page d'accueil
@app.route('/')
def home():
    return "<h1>Groupe 1 : Alexandra PONOMAREVA, Lufei LIU, Elise LINCKER</h1>"


if __name__ == "__main__":
    # app.run(host='127.0.0.1', port=5001)
    app.run()
