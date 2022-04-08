import email
from flask import Blueprint
from ..models.user import User
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
        # Connexion direct, génération du token
        token = jwt.encode(
            {'email': email,
            'exp': datetime.utcnow() + timedelta(minutes=30)}, 
            "secret_key_data_covid")
        return make_response(
            {'message':'Inscription réussie.', 
            'status':201,
            'token': token.decode('UTF-8'), 
            'email':email})
    else:
        # Code 202, un utilisateur avec cet email existe déjà
        return make_response(
            {'message':"L'utilisateur existe déjà. Veuillez vous connecter.", 
            'status':202, 
            'email':email})


# Connexion
@users.route('/login', methods=['POST'])
def login():
    # Création d'un dictionnaire pour stocker les form-data
    auth = request.form
    if not auth or not auth.get('email') or not auth.get('password'):
        # Code 401, email et/ou mot de passe non saisi
        return make_response(
            {'message':'Veuillez vous connecter',
            'status':401,
            'user':auth.get(email)})
    user = User.query.filter_by(email=auth.get('email')).first()
    if not user:
        # Code 401, l'utilisateur n'existe pas dans la BDD
        return make_response(
            {'message':'Utilisateur non trouvé, veuillez vous inscrire',
            'status':401,
            'user':auth.get(email)})
    if check_password_hash(user.password, auth.get('password')):
        # Génération du JWT Token
        token = jwt.encode(
            {'email': user.email,
            'exp': datetime.utcnow() + timedelta(minutes=30)}, 
            "secret_key_data_covid")
        return make_response(
            {'message':'Connexion réussie',
            'status':201,
            'token': token.decode('UTF-8'),
            'user':auth.get(email)})
    # Code 403, mot de passe incorrect
    return make_response(
            {'message':'Mot de passe erroné',
            'status':403,
            'user':auth.get(email)})

