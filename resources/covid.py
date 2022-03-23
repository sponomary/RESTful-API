from flask import Blueprint
from models.covid import DataCovidModel, DataCovidSchema
from models.db import db
from flask import request, jsonify
from lib.utils import token_required


covid = Blueprint('covid', __name__)


# 🐽🐽🐽🐽🐽🐽🐽🐽🐽🐽🐽🐽🐽🐽🐽🐽🐽🐽🐽🐽🐽🐽🐽🐽🐽🐽🐽🐽🐽🐽🐽
# RENVOIE UNE ERREUR Maximum response size reached
# Route qui retourne toutes les données covid ✅
@covid.route('/', methods=["GET"])
def get_all_covid():
    result = DataCovidModel.query.all()
    data_covid_schema = DataCovidSchema(many=True)
    return jsonify(data_covid_schema.dump(result))


# 🐽🐽🐽🐽🐽🐽🐽🐽🐽🐽🐽🐽🐽🐽🐽🐽🐽🐽🐽🐽🐽🐽🐽🐽🐽🐽🐽🐽🐽🐽🐽
# pas réussi à faire marcher non plus (???)
# Erreur : sqlalchemy.exc.StatementError: (builtins.TypeError) SQLite Date type only accepts Python date objects as input.
# Route qui met à jour une donnée covid 
@covid.route('/<int:id>/', methods=["PATCH"])
def update_covid(id):
    data_covid = DataCovidModel.query.get(id)
    data_covid.date_reference = request.json.get('date_reference', '')
    data_covid.semaine_injection = request.json.get('semaine_injection', '')
    data_covid.commune_residence = request.json.get('commune_residence', '')
    data_covid.libelle_commune = request.json.get('libelle_commune', '')
    data_covid.population_carto = request.json.get('population_carto', '')
    data_covid.classe_age = request.json.get('classe_age', '')
    data_covid.libelle_classe_age = request.json.get('libelle_classe_age', '')
    data_covid.effectif_1_inj = request.json.get('effectif_1_inj', '')
    data_covid.effectif_termine = request.json.get('effectif_termine', '')
    data_covid.effectif_cumu_1_inj = request.json.get('effectif_cumu_1_inj', '')
    data_covid.effectif_cumu_termine = request.json.get('effectif_cumu_termine', '')
    data_covid.taux_1_inj = request.json.get('taux_1_inj', '')
    data_covid.taux_termine = request.json.get('taux_termine', '')
    data_covid.taux_cumu_1_inj = request.json.get('taux_cumu_1_inj', '')
    data_covid.taux_cumu_termine = request.json.get('taux_cumu_termine', '')
    data_covid.date = request.json.get('date', '')

    data_covid.save_to_db()
    data_covid_schema = DataCovidSchema()
    return data_covid_schema.jsonify(data_covid)


# Route qui supprime une donnée covid ✅
@covid.route('/<int:id>/', methods=["DELETE"])
def delete_covid(id):
    data_covid = DataCovidModel.query.get(id)
    data_covid_schema = DataCovidSchema()
    data_covid.delete_from_db()
    return data_covid_schema.jsonify(data_covid)


# 🐽🐽🐽🐽🐽🐽🐽🐽🐽🐽🐽🐽🐽🐽🐽🐽🐽🐽🐽🐽🐽🐽🐽🐽🐽🐽🐽🐽🐽🐽🐽
# Erreur : sqlalchemy.exc.StatementError: (builtins.TypeError) SQLite Date type only accepts Python date objects as input.
# Route qui crée une nouvelle donnée covid
@covid.route('/edit', methods=['POST'])
def create_covid():
    date_reference = request.json.get('date_reference', '')
    semaine_injection = request.json.get('semaine_injection', '')
    commune_residence = request.json.get('commune_residence', '')
    libelle_commune = request.json.get('libelle_commune', '')
    population_carto = request.json.get('population_carto', '')
    classe_age = request.json.get('classe_age', '')
    libelle_classe_age = request.json.get('libelle_classe_age', '')
    effectif_1_inj = request.json.get('effectif_1_inj', '')
    effectif_termine = request.json.get('effectif_termine', '')
    effectif_cumu_1_inj = request.json.get('effectif_cumu_1_inj', '')
    effectif_cumu_termine = request.json.get('effectif_cumu_termine', '')
    taux_1_inj = request.json.get('taux_1_inj', '')
    taux_termine = request.json.get('taux_termine', '')
    taux_cumu_1_inj = request.json.get('taux_cumu_1_inj', '')
    taux_cumu_termine = request.json.get('taux_cumu_termine', '')
    date = request.json.get('date', '')

    data = DataCovidModel(date_reference=date_reference, semaine_injection=semaine_injection,
                      commune_residence=commune_residence,
                      libelle_commune=libelle_commune, population_carto=population_carto, classe_age=classe_age,
                      libelle_classe_age=libelle_classe_age, effectif_1_inj=effectif_1_inj,
                      effectif_termine=effectif_termine,
                      effectif_cumu_1_inj=effectif_cumu_1_inj, effectif_cumu_termine=effectif_cumu_termine,
                      taux_1_inj=taux_1_inj, taux_termine=taux_termine, taux_cumu_1_inj=taux_cumu_1_inj,
                      taux_cumu_termine=taux_cumu_termine, date=date)

    data.save_to_db()
    data_covid_schema = DataCovidSchema()
    return data_covid_schema.jsonify(data)


# Route qui retourne une donnée covid ✅
@covid.route('/<int:id>/', methods=['GET'])
@token_required
def get_covid_by_id(id):
    result = DataCovidModel.query.get(id)
    data_covid_schema = DataCovidSchema()
    return data_covid_schema.jsonify(result)


# Route qui renvoie les résultats d'une requête (simple ou multiple)
# Exemple : http://127.0.0.1:5000/covid/search?libelle_commune=ANTONY&classe_age=40-54
@covid.route('/search', methods=["GET"])
@token_required
def data_filter():
    query_parameters = request.args
    fields = DataCovidModel.__table__.columns
    results = db.session.query(DataCovidModel)
    for k, v in query_parameters.items():
        if k not in fields:
            return {"error :": "404",
                    "message : ": "page not found"}
        results = results.filter(getattr(DataCovidModel, k) == v)
    results = results.all()
    data_covid_schema = DataCovidSchema(many=True)
    return jsonify(data_covid_schema.dump(results))


# Route qui permet de retourner toutes les données uniques de certains colonnes
@covid.route('/getInfo/<info>', methods=["GET"])
@token_required
def get_info(info):
    info_recherche = '% s' % info
    if info_recherche == "date_reference":
        query = DataCovidModel.query.with_entities(DataCovidModel.libelle_commune).distinct()
        results = [row.libelle_commune for row in query.all()]
    elif info_recherche == "semaine_injection":
        query = DataCovidModel.query.with_entities(DataCovidModel.semaine_injection).distinct()
        results = [row.semaine_injection for row in query.all()]
    elif info_recherche == "commune_residence":
        query = DataCovidModel.query.with_entities(DataCovidModel.commune_residence).distinct()
        results = [row.commune_residence for row in query.all()]
    elif info_recherche == "population_carto":
        query = DataCovidModel.query.with_entities(DataCovidModel.population_carto).distinct()
        results = [row.population_carto for row in query.all()]
    elif info_recherche == "classe_age":
        query = DataCovidModel.query.with_entities(DataCovidModel.classe_age).distinct()
        results = [row.classe_age for row in query.all()]

    return jsonify({info_recherche: results})



# 🐽🐽🐽🐽🐽🐽🐽🐽🐽🐽🐽🐽🐽🐽🐽🐽🐽🐽🐽🐽🐽🐽🐽🐽🐽🐽🐽🐽🐽🐽🐽
# peut-on supprimer cette méthode aussi puisqu'on a la route getInfo qui retourne toutes les données uniques ?
# 🐽🐽🐽🐽🐽🐽🐽🐽🐽🐽🐽🐽🐽🐽🐽🐽🐽🐽🐽🐽🐽🐽🐽🐽🐽🐽🐽🐽🐽🐽🐽
# Route qui permet de retourner toutes les communes uniques ✅
# <=> SELECT DISTINCT libelle_commune FROM DATA_COVID;
@covid.route('/getCommune/', methods=["GET"])
def get_commune():
    query = DataCovidModel.query.with_entities(DataCovidModel.libelle_commune).distinct()
    communes = [row.libelle_commune for row in query.all()]
    return jsonify({"communes": communes})
    """
    result = DATA_COVID.query.all()
    data_covid_schema = DataCovidSchema(many=True)
    return jsonify(data_covid_schema.dump(result))
    """


# 🐽🐽🐽🐽🐽🐽🐽🐽🐽🐽🐽🐽🐽🐽🐽🐽🐽🐽🐽🐽🐽🐽🐽🐽🐽🐽🐽🐽🐽🐽🐽
# peut-on supprimer cette méthode aussi puisqu'on a la route search pour toutes les requêtes ?
# 🐽🐽🐽🐽🐽🐽🐽🐽🐽🐽🐽🐽🐽🐽🐽🐽🐽🐽🐽🐽🐽🐽🐽🐽🐽🐽🐽🐽🐽🐽🐽
# Route qui affiche les données pour une commune ✅
@covid.route('/getCovidByCommune/<string:libelle_commune>/', methods=["GET"])
def get_covid_by_commune(libelle_commune):
    # Récupération de la requête de l'utilisateur
    # PREMIER TEST SUR LA COMMUNE UNIQUEMENT
    commune = request.form.get('commune')

    # Recherche des données correspondantes dans la table DATA_COVID de la base de données
    result = DataCovidModel.query.filter_by(libelle_commune=commune).all()
    data_covid_schema = DataCovidSchema(many=True)
    return jsonify(data_covid_schema.dump(result))