from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_login import LoginManager

db = SQLAlchemy()
ma = Marshmallow()
lm = LoginManager()


# fonctions appelées par app.py pour initialser la base de données

def initialize_db(app):
    db.init_app(app)


def initialize_marshmallow(app):
    ma.init_app(app)

def login_manager(app):
    login_manager.init_app(app)