#!/usr/bin/python3
# coding: utf-8

"""
    M2 TAL, INGÉNIERIE MULTILINGUE : TECHNIQUES WEB (REST API)
    -------------------------------------------
    Ce module regroupe les fonctions utilitaires de l'API. 
    :copyright: © 2022 by Élise & Lufei & Alexandra.
"""

from flask import request, jsonify, abort
import jwt
from functools import wraps


# Décorateur de vérification du JWT = JSON Web Token
def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        # Récupération du token depuis le header
        if 'x-access-token' in request.headers:
            token = request.headers['x-access-token']
        # Code 401, token manquant
        if not token:
            return jsonify({'message': 'Token is missing !!'}), 401
        try:
            # Décodage du payload
            data = jwt.decode(token, "secret_key_data_covid")
        except:
            return jsonify({
                'message': 'Token is invalid !!'
            }), 401
        # Renvoie les informations accessibles aux utilisateurs connectés
        return f(*args, **kwargs)

    return decorated
