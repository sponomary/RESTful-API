from flask import request, jsonify
import jwt
from functools import wraps
from models.user import User

# decorator for verifying the JWT


def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        # jwt is passed in the request header
        if 'x-access-token' in request.headers:
            token = request.headers['x-access-token']
        # return 401 if token is not passed
        if not token:
            return jsonify({'message': 'Token is missing !!'}), 401
        try:
            # decoding the payload to fetch the stored details
            data = jwt.decode(token, "secret_key_data_covid")
        except:
            return jsonify({
                'message': 'Token is invalid !!'
            }), 401
        # retourner les informations accessibles aux utilisateurs connectés
        return f(*args, **kwargs)

    return decorated
