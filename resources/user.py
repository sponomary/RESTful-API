from flask import Blueprint
from models.user import User
from flask import Flask, render_template, request, url_for, redirect, flash, send_from_directory, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, current_user, logout_user


users = Blueprint('users', __name__)


# 🐽🐽🐽🐽🐽🐽🐽🐽🐽🐽🐽🐽🐽🐽🐽🐽🐽🐽🐽🐽🐽🐽🐽🐽🐽
# REFAIRE TOUS LES RETURN SANS LE FRONT
# ET FINIR TRUC DU TOKEN
# 🐽🐽🐽🐽🐽🐽🐽🐽🐽🐽🐽🐽🐽🐽🐽🐽🐽🐽🐽🐽🐽🐽🐽🐽🐽


# Création d'un compte
@users.route('/register', methods=["GET", "POST"])
def register():
    if request.method == "POST":

        if User.query.filter_by(email=request.form.get("email")).first():
            # User already exists
            return "RETURN REGISTER A FAIRE" # 🐽🐽🐽🐽🐽
            flash("Vous avez déjà créé un compte avec cette adresse mail, connectez-vous !")
            return redirect(url_for('login'))

        # Avant de stocker le mot de passe dans la base de données, on applique le hashtag "generate_password_hash()"
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
        User.save_to_db(new_user)

        # Log in and authenticate user after adding details to database.
        login_user(new_user)
        return "RETURN CREATION DE COMPTE + LOGIN A FAIRE" # 🐽🐽🐽🐽🐽
        return redirect(url_for("secrets"))

    return "RETURN CREATION DE COMPTE + LOGIN A FAIRE" # 🐽🐽🐽🐽🐽
    return render_template("register.html", logged_in=current_user.is_authenticated)


# Connexion
# 🐽🐽🐽🐽🐽🐽🐽🐽🐽🐽🐽🐽🐽🐽🐽🐽🐽🐽🐽🐽🐽🐽🐽🐽🐽🐽🐽🐽🐽🐽🐽
# ---> EST CE QU'ON PEUT FAIRE APPARAITRE "quel user est connecté" DANS L'URL comme a fait seigneur ? 🐽 genre login/?user=xxx
@users.route('/login', methods=["GET", "POST"])
def login():
    if request.method == "POST":

        # Récupération de l'email et du mot de passe saisis par l'utilisateur
        email = request.form.get('email')
        password = request.form.get('password')

        # Recherche de l'utilisateur dans la table USER de la base de données à partir de l'email saisi
        user = User.query.filter_by(email=email).first()

        # Si l'email ne figure pas dans la base de données : échec de l'authentification. Renvoie la page login
        if not user:
            return "RETURN LOGIN A FAIRE" # 🐽🐽🐽🐽🐽
            flash("Identifiant incorrect.")
            return redirect(url_for("login"))

        # Si l'email figure dans la base de données mais le mot de passe est incorrect : échec de l'authentification. Renvoie la page login
        # check_password_hash compare le stored password hash et le entered password hashed
        elif not check_password_hash(user.password, password):
            return "RETURN LOGIN A FAIRE" # 🐽🐽🐽🐽🐽
            flash("Mot de passe incorrect.")
            return redirect(url_for("login"))

        # Sinon (email existant et mot de passe correct) : authentification réussie. Renvoie la page secrets
        else:
            login_user(user)
            return "RETURN LOGIN A FAIRE" # 🐽🐽🐽🐽🐽

    return render_template("login.html", logged_in=current_user.is_authenticated)


# Déconnexion
@users.route('/logout')
def logout():
    logout_user()
    return "RETURN LOGOUT A FAIRE" # 🐽🐽🐽🐽🐽