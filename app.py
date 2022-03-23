#!/usr/bin/python3
# coding: utf-8

"""
    M2 TAL, INGÉNIERIE MULTILINGUE : TECHNIQUES WEB (REST API)
    -------------------------------------------
    Ce module lance l'API. 
    :copyright: © 2022 by Élise & Lufei & Alexandra.
"""

__version__ = "0.6"

from flask import Flask
from flask_login import LoginManager
from flask_apscheduler import APScheduler #ajouter dans les requirements
# 🐽🐽🐽 importer ici le nouveau script de synchro
from resources.user import users
from resources.covid import covid
from models.db import initialize_db, initialize_marshmallow

app = Flask(__name__)

#Blueprint
app.register_blueprint(users)
app.register_blueprint(covid, url_prefix='/covid')

app.config['SECRET_KEY'] = 'any-secret-key-you-choose'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data/DataViewer.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config.update({'SCHEDULER_API_ENABLED': True})

initialize_db(app)
initialize_marshmallow(app)

"""
# 🐽🐽🐽🐽🐽🐽🐽🐽🐽🐽🐽🐽🐽🐽🐽🐽🐽🐽🐽🐽🐽🐽🐽🐽🐽🐽🐽🐽🐽🐽🐽
# PARTIE SCHEDULER -> changer la fonction job pour mettre la v4 si on passe par API

# Créer un objet Scheduler pour une tâche programmée
scheduler=APScheduler()
scheduler.init_app(app)

# Ajouter une tâche programmée à l'ordonnanceur (mise à jour des données depuis datagouv + mise à jour de base de données)
@scheduler.task('interval', id='do_job', days=1)
def job():
    print("Synchronisation...")
    synchro.update_db(synchro.update_data_covid("https://datavaccin-covid.ameli.fr/api/v2/catalog/datasets/donnees-de-vaccination-par-commune/exports/json?limit=-1&offset=0&timezone=UTC", "data/donnees-de-vaccination-par-commune.json")) #update_db(update_data_covid(url_ameli, covid_json))
    print("...synchronisation terminée")

# Démarrer le travail du planificateur de tâches programmé 
scheduler.start()
"""

# 🐽🐽🐽🐽🐽🐽🐽🐽🐽🐽🐽🐽🐽🐽🐽🐽🐽🐽🐽🐽🐽🐽🐽🐽🐽🐽🐽🐽🐽🐽🐽
# juste copié Noélie pour la route de base
# 🐽🐽🐽🐽🐽🐽🐽🐽🐽🐽🐽🐽🐽🐽🐽🐽🐽🐽🐽🐽🐽🐽🐽🐽🐽🐽🐽🐽🐽🐽🐽
# Page d'accueil
@app.route('/')
def home():
    return "<h1>Groupe 1 : Alexandra PONOMAREVA, Lufei LIU, Elise LINCKER</h1>"


"""
PAS ENCORE D'IDEE QUOI FAIRE AVEC CE BOUT DE CODE
# 🐽🐽🐽🐽🐽🐽🐽🐽🐽🐽🐽🐽🐽🐽🐽🐽🐽🐽🐽🐽🐽🐽🐽🐽🐽🐽🐽🐽🐽🐽🐽
login_manager = LoginManager()
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))
# 🐽🐽🐽🐽🐽🐽🐽🐽🐽🐽🐽🐽🐽🐽🐽🐽🐽🐽🐽🐽🐽🐽🐽🐽🐽🐽🐽🐽🐽🐽🐽
"""

if __name__ == "__main__":
    # app.run(host='127.0.0.1', port=5001)
    app.run(debug=True)
