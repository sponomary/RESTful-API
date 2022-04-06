#!/usr/bin/python3
# coding: utf-8

"""
    M2 TAL, INGÉNIERIE MULTILINGUE : TECHNIQUES WEB (REST API)
    -------------------------------------------
    Ce module lance la synchronisation journalière des données. 
    :copyright: © 2022 by Élise & Lufei & Alexandra.
"""

from flask_apscheduler import APScheduler
from .synchronisation import init_full_bdd, differ_maj_bdd
from models.covid import DataCovidModel
from models.db import db

scheduler = APScheduler()  # créer un objet Scheduler pour une tâche programmée


# Ajouter une tâche programmée à l'ordonnanceur (mise à jour des données depuis datagouv + mise à jour de la BDD)
def start_scheduler(app):
    scheduler.init_app(app)

    @scheduler.task('interval', id='do_job', days=1)
    def job():
        print("Synchronisation...")
        with app.app_context():
            # Si la table DATA_COVID de la BDD est vide, initialisation des données
            if db.session.query(DataCovidModel).first() is None:
                init_full_bdd()
            # Sinon, mise à jour de la base existante
            else:
                differ_maj_bdd()
        print("...synchronisation terminée")

    scheduler.start()
