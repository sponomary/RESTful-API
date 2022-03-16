#!/usr/bin/python3
# coding: utf-8

from __future__ import unicode_literals

"""
    M2 TAL, INGÉNIERIE MULTILINGUE : TECHNIQUES WEB (REST API)
    -------------------------------------------
    Ce module lance l'API. 
    :copyright: © 2022 by Élise & Lufei & Alexandra.
"""

__version__ = "0.3"

from flask import Flask, render_template, request, url_for, redirect, flash, send_from_directory, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_login import UserMixin, login_user, LoginManager, login_required, current_user, logout_user
from datetime import datetime

app = Flask(__name__)

app.config['SECRET_KEY'] = 'any-secret-key-you-choose'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///DataViewer.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
ma = Marshmallow(app)

login_manager = LoginManager()
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


# CREATE TABLE IN DB
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(500))
    name = db.Column(db.String(1000))


# Line below only required once, when creating DB.
# db.create_all()

# /!\ /!\ les types ne correspondent pas à ceux dans la bdd /!\ /!\
class DATA_COVID(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date_reference = db.Column(db.String, nullable=False)  # db.Column(db.Date, nullable=False)
    semaine_injection = db.Column(db.String, nullable=False)
    commune_residence = db.Column(db.Integer, nullable=False)
    libelle_commune = db.Column(db.String(100), nullable=False)
    population_carto = db.Column(db.Integer, nullable=False)
    classe_age = db.Column(db.String(100), nullable=False)
    libelle_classe_age = db.Column(db.String(100), nullable=False)
    effectif_1_inj = db.Column(db.Integer)
    effectif_termine = db.Column(db.Integer)
    effectif_cumu_1_inj = db.Column(db.Integer)
    effectif_cumu_termine = db.Column(db.Integer)
    taux_1_inj = db.Column(db.Float)
    taux_termine = db.Column(db.Float)
    taux_cumu_1_inj = db.Column(db.Float)
    taux_cumu_termine = db.Column(db.Float)
    date = db.Column(db.String(100))  # db.Column(db.DateTime, default=datetime.utcnow)


class DataCovidSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = DATA_COVID

    def __repr__(self):
        return '<Data %r>' % self.id

    """
    python3
    >>> from app import db
    >>> db.create_all()
    >>> exit()
    flask run
    """

    def __repr__(self):
        return '<Data %r>' % self.id


# Page d'accueil
@app.route('/')
def home():
    # Every render_template has a logged_in variable set.
    return render_template("index.html", logged_in=current_user.is_authenticated)


#
@app.route('/register', methods=["GET", "POST"])
def register():
    if request.method == "POST":

        if User.query.filter_by(email=request.form.get("email")).first():
            # User already exists
            flash("You've already signed up with that email, log in instead!")
            return redirect(url_for('login'))

        # Avant de stocker le mot de pass  dans la BDD, on applique le hashage `generate_password_hash()`
        # Docs : https://werkzeug.palletsprojects.com/en/1.0.x/utils/#module-werkzeug.security
        hash_and_salted_password = generate_password_hash(
            request.form.get('password'),
            method='pbkdf2:sha256',
            salt_length=8
        )
        new_user = User(
            email=request.form.get('email'),
            name=request.form.get('name'),
            password=hash_and_salted_password
        )
        db.session.add(new_user)
        db.session.commit()

        # Log in and authenticate user after adding details to database.
        login_user(new_user)
        return redirect(url_for("secrets"))

    return render_template("register.html", logged_in=current_user.is_authenticated)


# Connexion
@app.route('/login', methods=["GET", "POST"])
def login():
    if request.method == "POST":

        # Récupération de l'email et du mot de passe saisis par l'utilisateur        
        email = request.form.get('email')
        password = request.form.get('password')

        # Recherche de l'utilisateur dans la table USER de la base de données à partir de l'email saisi
        user = User.query.filter_by(email=email).first()

        # Si l'email ne figure pas dans la base de données : échec de l'authentification. Renvoie la page login
        if not user:
            flash("Identifiant incorrect.")
            return redirect(url_for("login"))

        # Si l'email figure dans la base de données mais le mot de passe est incorrect : échec de l'authentification. Renvoie la page login
        # check_password_hash compare le stored password hash et le entered password hashed
        elif not check_password_hash(user.password, password):
            flash("Mot de passe incorrect.")
            return redirect(url_for("login"))

        # Sinon (email existant et mot de passe correct) : authentification réussie. Renvoie la page secrets
        else:
            login_user(user)
            return redirect(url_for('secrets'))

    return render_template("login.html", logged_in=current_user.is_authenticated)


# Page de bienvenue, affichée une fois que l'utilisateur est connecté
@app.route('/secrets')
@login_required
def secrets():
    print(current_user.name)
    return render_template("secrets.html", name=current_user.name, logged_in=True)


# Déconnexion, renvoie la page d'accueil
@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('home'))


# Michael Scott
@app.route('/download')
@login_required
def download():
    return send_from_directory('static', filename="files/giphy.gif")


# Page qui affiche la base de données
@app.route('/data', methods=["GET", "POST"])
def data():
    # ESSAI AJOUT D'UNE REQUETE
    if request.method == "POST":
        # Récupération de la requête de l'utilisateur
        # PREMIER TEST SUR LA COMMUNE UNIQUEMENT
        commune = request.form.get('commune')

        # Recherche des données correspondantes dans la table DATA_COVID de la base de données
        output_data = DATA_COVID.query.filter_by(libelle_commune=commune).all()
        print(output_data)
        return render_template("data.html", output_data=output_data)

    output_data = DATA_COVID.query.all()
    print(output_data)
    return render_template("data.html", output_data=output_data)


# TODO: AJOUT DU 16 MARS, A TESTER

# Route qui permet de retourner toutes les données covid ✅
@app.route('/covid/', methods=["GET"])
def get_all_covid():
    result = DATA_COVID.query.all()
    data_covid_schema = DataCovidSchema(many=True)
    return jsonify(data_covid_schema.dump(result))


# Route qui permet de retourner une donnée covid ✅
@app.route('/covid/<int:id>/', methods=['GET'])
def get_covid_by_id(id):
    result = DATA_COVID.query.get(id)
    data_covid_schema = DataCovidSchema()
    return data_covid_schema.jsonify(result)


# TODO: Comment afficher toutes les communes uniques ?
"""SELECT DISTINCT libelle_commune FROM DATA_COVID;"""
# Route qui permet de retourner toutes les communes 🐽 MARCHE PAS
@app.route('/covid/getCommune/', methods=["GET"])
def get_commune():
    result = DATA_COVID.query.all()
    data_covid_schema = DataCovidSchema(many=True)
    return jsonify(data_covid_schema.dump(result))


# Route qui affiche les données pour une commune ✅
@app.route('/covid/getCovidByCommune/<string:libelle_commune>/', methods=["GET"])
def get_covid_by_commune(libelle_commune):
    # Récupération de la requête de l'utilisateur
    # PREMIER TEST SUR LA COMMUNE UNIQUEMENT
    commune = request.form.get('commune')

    # Recherche des données correspondantes dans la table DATA_COVID de la base de données
    result = DATA_COVID.query.filter_by(libelle_commune=commune).all()
    data_covid_schema = DataCovidSchema(many=True)
    return jsonify(data_covid_schema.dump(result))


# Route qui crée une nouvelle donnée covid ✅
@app.route('/covid/', methods=['POST'])
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

    data = DATA_COVID(date_reference=date_reference, semaine_injection=semaine_injection,
                      commune_residence=commune_residence,
                      libelle_commune=libelle_commune, population_carto=population_carto, classe_age=classe_age,
                      libelle_classe_age=libelle_classe_age, effectif_1_inj=effectif_1_inj,
                      effectif_termine=effectif_termine,
                      effectif_cumu_1_inj=effectif_cumu_1_inj, effectif_cumu_termine=effectif_cumu_termine,
                      taux_1_inj=taux_1_inj, taux_termine=taux_termine, taux_cumu_1_inj=taux_cumu_1_inj,
                      taux_cumu_termine=taux_cumu_termine, date=date)

    db.session.add(data)
    db.session.commit()
    data_covid_schema = DataCovidSchema()
    return data_covid_schema.jsonify(data)


# Route qui met à jour une donnée covid ✅
@app.route('/covid/<int:id>/', methods=["PATCH"])
def update_covid(id):
    data_covid = DATA_COVID.query.get(id)
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
    db.session.add(data_covid)
    db.session.commit()
    data_covid_schema = DataCovidSchema()
    return data_covid_schema.jsonify(data_covid)


# Route qui supprimer une donnée covid ✅
@app.route('/covid/<int:id>/', methods=["DELETE"])
def delete_covid(id):
    data_covid = DATA_COVID.query.get(id)
    db.session.delete(data_covid)
    db.session.commit()
    data_covid_schema = DataCovidSchema()
    return data_covid_schema.jsonify(data_covid)


if __name__ == "__main__":
    # si jamais le port bugge, connecter àun autre
    # app.run(host='127.0.0.1', port=5001)
    app.run(debug=True)