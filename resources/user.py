from flask import Blueprint
from models.user import User
from flask_login import logout_user
from flask import request, jsonify, make_response
from werkzeug.security import generate_password_hash, check_password_hash
import jwt
from datetime import datetime, timedelta


users = Blueprint('users', __name__)


# 🐽🐽🐽🐽🐽🐽🐽🐽🐽🐽🐽🐽🐽🐽🐽🐽🐽🐽🐽🐽🐽🐽🐽🐽🐽
# REFAIRE TOUS LES RETURN SANS LE FRONT ✅
# ET FINIR TRUC DU TOKEN ✅
# 🐽🐽🐽🐽🐽🐽🐽🐽🐽🐽🐽🐽🐽🐽🐽🐽🐽🐽🐽🐽🐽🐽🐽🐽🐽

"""
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
        User.save_user(new_user)

        # Log in and authenticate user after adding details to database.
        login_user(new_user)
        return "RETURN CREATION DE COMPTE + LOGIN A FAIRE" # 🐽🐽🐽🐽🐽
        return redirect(url_for("secrets"))

    return "RETURN CREATION DE COMPTE + LOGIN A FAIRE" # 🐽🐽🐽🐽🐽
    return render_template("register.html", logged_in=current_user.is_authenticated)
"""
"""
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
"""

# Création d'un compte
@users.route('/register', methods =['POST'])
def register():
    # creates a dictionary of the form data
    data = request.form
    # gets name, email and password
    name, email = data.get('name'), data.get('email')
    password = data.get('password')

    # checking for existing user
    user = User.query.filter_by(email = email).first()
    if not user:
        # database ORM object
        user = User(
            email=email,
            name=name,
            password=generate_password_hash(password)
        )
        # insert user in db
        user.save_user()
        return make_response('Successfully registered.', 201)
    else:
        # returns 202 if user already exists
        return make_response('User already exists. Please Log in.', 202)


# Connexion
@users.route('/login', methods =['POST'])
def login():
    # creates dictionary of form data
    auth = request.form
    if not auth or not auth.get('email') or not auth.get('password'):
        # returns 401 if any email or / and password is missing
        return make_response(
            'Could not verify',
            401,
            {'WWW-Authenticate' : 'Basic realm ="Login required !!"'}
        )
    user = User.query.filter_by(email = auth.get('email')).first()
    if not user:
        # returns 401 if user does not exist
        return make_response(
            'Could not verify',
            401,
            {'WWW-Authenticate' : 'Basic realm ="User does not exist !!"'}
        )

    if check_password_hash(user.password, auth.get('password')):
        # generates the JWT Token
        token = jwt.encode({
            'email': user.email,
            'exp' : datetime.utcnow() + timedelta(minutes = 30)
        }, "secret_key_data_covid")

        return make_response(jsonify({'token' : token.decode('UTF-8')}), 201)
    # returns 403 if password is wrong
    return make_response(
        'Could not verify',
        403,
        {'WWW-Authenticate' : 'Basic realm ="Wrong Password !!"'}
    )



# Déconnexion
@users.route('/logout')
def logout():
    logout_user()
    return "RETURN LOGOUT A FAIRE" # 🐽🐽🐽🐽🐽