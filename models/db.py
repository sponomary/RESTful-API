from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow

db = SQLAlchemy()
ma = Marshmallow()

# fonctions appelées par app.py pour initialser la base de données

def initialize_db(app):
    db.init_app(app)

def initialize_marshmallow(app):
    ma.init_app(app)
