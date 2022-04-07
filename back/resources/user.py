from flask import Blueprint
from ..models.user import User
from flask_login import logout_user
from flask import request, jsonify, make_response
from werkzeug.security import generate_password_hash, check_password_hash
import jwt
from datetime import datetime, timedelta

users = Blueprint('users', __name__)


# Création d'un compte
@users.route('/register', methods=['POST'])
def register():
    # Création d'un dictionnaire pour stocker les form-data
    data = request.form
    # Récupération des valeurs saisies : name, email et password
    name, email = data.get('name'), data.get('email')
    password = data.get('password')

    # Recherche dans la BDD si un utilisateur avec cet email est déjà enregistré
    user = User.query.filter_by(email=email).first()
    if not user:
        # Création d'un objet User
        user = User(
            email=email,
            name=name,
            password=generate_password_hash(password)
        )
        # Code 201, insertion de l'utilisateur dans la BDD
        user.save_user()
        return make_response({'message':'Successfully registered.', 'status':201})
    else:
        # Code 202, un utilisateur avec cet email existe déjà
        return make_response({'message':'User already exists. Please Log in.', 'status':202})


# Connexion
@users.route('/login', methods=['POST'])
def login():
    print("ON EST BIEN DANS LOGIN")
    # Création d'un dictionnaire pour stocker les form-data
    auth = request.form
    if not auth or not auth.get('email') or not auth.get('password'):
        # Code 401, email et/ou mot de passe non saisi
        return make_response(
            {'message':'Could not verify',
            'status':401})
        """🐽🐽🐽🐽🐽🐽🐽🐽🐽🐽🐽🐽🐽🐽🐽🐽🐽🐽 QUE FAIRE DE CA ?
        {'WWW-Authenticate': 'Basic realm ="Login required !!"'}"""
    user = User.query.filter_by(email=auth.get('email')).first()
    if not user:
        # Code 401, l'utilisateur n'existe pas dans la BDD
        return make_response(
            {'message':'Could not verify',
            'status':401})
        """🐽🐽🐽🐽🐽🐽🐽🐽🐽🐽🐽🐽🐽🐽🐽🐽🐽🐽 QUE FAIRE DE CA ?
        {'WWW-Authenticate': 'Basic realm ="User does not exist !!"'}"""

    if check_password_hash(user.password, auth.get('password')):
        # Génération du JWT Token
        token = jwt.encode({
            'email': user.email,
            'exp': datetime.utcnow() + timedelta(minutes=30)
        }, "secret_key_data_covid")
        return make_response(jsonify({'token': token.decode('UTF-8'), 'status':201, 'message':'Successfully logged in'}))
    # Code 403, mot de passe incorrect
    return make_response(
            {'message':'Could not verify',
            'status':403})
    """🐽🐽🐽🐽🐽🐽🐽🐽🐽🐽🐽🐽🐽🐽🐽🐽🐽🐽 QUE FAIRE DE CA ?
    {'WWW-Authenticate': 'Basic realm ="Wrong Password !!"'}"""
