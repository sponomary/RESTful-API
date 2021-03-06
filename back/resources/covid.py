#!/usr/bin/python3
# coding: utf-8

"""
    M2 TAL, INGÉNIERIE MULTILINGUE : TECHNIQUES WEB (REST API)
    -------------------------------------------
    Ce module back permet d'ajouter, consulter, supprimer, modifier des données COVID.
    :copyright: © 2022 by Élise & Lufei & Alexandra.
"""

from flask import Blueprint
from ..models.covid import DataCovidModel, DataCovidSchema
from ..models.db import db
from flask import request, jsonify
from ..lib.utils import token_required
from datetime import datetime

covid = Blueprint('covid', __name__)


# Route qui retourne toutes les données covid
# Par défaut, renvoie max 5000 données
@covid.route('/', methods=["GET"])
def get_all_covid(limit=5000):
    results = DataCovidModel.query.limit(limit).all()
    data_covid_schema = DataCovidSchema(many=True)
    return jsonify(data_covid_schema.dump(results))

# Route qui met à jour une donnée covid
@covid.route('/<int:id>/', methods=["PATCH"])
@token_required  # nécessite une connexion
def update_covid(id):
    data_covid = DataCovidModel.query.get(id)
    data_covid.date_reference = datetime.strptime(request.form.get('date_reference', ''), "%Y-%m-%d")
    data_covid.semaine_injection = request.form.get('semaine_injection', '')
    data_covid.commune_residence = request.form.get('commune_residence', '')
    data_covid.libelle_commune = request.form.get('libelle_commune', '')
    data_covid.population_carto = request.form.get('population_carto', '')
    data_covid.classe_age = request.form.get('classe_age', '')
    data_covid.libelle_classe_age = request.form.get('libelle_classe_age', '')
    data_covid.effectif_1_inj = request.form.get('effectif_1_inj', '')
    data_covid.effectif_termine = request.form.get('effectif_termine', '')
    data_covid.effectif_cumu_1_inj = request.form.get('effectif_cumu_1_inj', '')
    data_covid.effectif_cumu_termine = request.form.get('effectif_cumu_termine', '')
    data_covid.taux_1_inj = request.form.get('taux_1_inj', '')
    data_covid.taux_termine = request.form.get('taux_termine', '')
    data_covid.taux_cumu_1_inj = request.form.get('taux_cumu_1_inj', '')
    data_covid.taux_cumu_termine = request.form.get('taux_cumu_termine', '')
    data_covid.date = datetime.utcnow()

    data_covid.save_to_db()
    data_covid_schema = DataCovidSchema()
    return data_covid_schema.jsonify(data_covid)


# Route qui supprime une donnée covid
@covid.route('/<int:id>/', methods=["DELETE"])
@token_required  # nécessite une connexion
def delete_covid(id):
    data_covid = DataCovidModel.query.get(id)
    data_covid_schema = DataCovidSchema()
    data_covid.delete_from_db()
    return data_covid_schema.jsonify(data_covid)


# Route qui crée une nouvelle donnée covid
@covid.route('/', methods=['POST'])
@token_required  # nécessite une connexion
def create_covid():
    date_reference = datetime.strptime(request.form.get('date_reference', ''), "%Y-%m-%d")
    semaine_injection = request.form.get('semaine_injection', '')
    commune_residence = request.form.get('commune_residence', '')
    libelle_commune = request.form.get('libelle_commune', '')
    population_carto = request.form.get('population_carto', '')
    classe_age = request.form.get('classe_age', '')
    libelle_classe_age = request.form.get('libelle_classe_age', '')
    effectif_1_inj = request.form.get('effectif_1_inj', '')
    effectif_termine = request.form.get('effectif_termine', '')
    effectif_cumu_1_inj = request.form.get('effectif_cumu_1_inj', '')
    effectif_cumu_termine = request.form.get('effectif_cumu_termine', '')
    taux_1_inj = request.form.get('taux_1_inj', '')
    taux_termine = request.form.get('taux_termine', '')
    taux_cumu_1_inj = request.form.get('taux_cumu_1_inj', '')
    taux_cumu_termine = request.form.get('taux_cumu_termine', '')

    data = DataCovidModel(date_reference=date_reference, semaine_injection=semaine_injection,
                          commune_residence=commune_residence,
                          libelle_commune=libelle_commune, population_carto=population_carto, classe_age=classe_age,
                          libelle_classe_age=libelle_classe_age, effectif_1_inj=effectif_1_inj,
                          effectif_termine=effectif_termine,
                          effectif_cumu_1_inj=effectif_cumu_1_inj, effectif_cumu_termine=effectif_cumu_termine,
                          taux_1_inj=taux_1_inj, taux_termine=taux_termine, taux_cumu_1_inj=taux_cumu_1_inj,
                          taux_cumu_termine=taux_cumu_termine,
                          date=datetime.utcnow())

    data.save_to_db()
    data_covid_schema = DataCovidSchema()
    return data_covid_schema.jsonify(data)


# Route qui retourne une donnée covid
@covid.route('/<int:id>/', methods=['GET'])
def get_covid_by_id(id):
    result = DataCovidModel.query.get(id)
    data_covid_schema = DataCovidSchema()
    return data_covid_schema.jsonify(result)


# Route qui permet de retourner toutes les données uniques de certains colonnes
@covid.route('/<string:info>/', methods=["GET"])
def get_distinct_value(info):
    info_recherche = '% s' % info
    fields = DataCovidModel.__table__.columns
    if info_recherche not in fields:
        return {"error :": "404",
                "message : ": "page not found"}
    query = DataCovidModel.query.with_entities(getattr(DataCovidModel, info_recherche)).distinct()
    results = [row[0] for row in query.all()]

    return jsonify({info_recherche: results})


# Route qui renvoie les résultats d'une requête (simple ou multiple)
# Par défaut, renvoie max 5000 données
@covid.route('/search', methods=["GET"])
def data_filter(limit=5000):
    query_parameters = request.args
    fields = DataCovidModel.__table__.columns
    results = db.session.query(DataCovidModel)
    for k, v in query_parameters.items():
        if k not in fields:
            return {"error :": "404",
                    "message : ": "page not found"}
        results = results.filter(getattr(DataCovidModel, k) == v)
    results = results.limit(limit).all()
    data_covid_schema = DataCovidSchema(many=True)
    return jsonify(data_covid_schema.dump(results))
