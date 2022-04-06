#!/usr/bin/python3
# coding: utf-8

from .db import db
from flask_login import UserMixin


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(500))
    name = db.Column(db.String(1000))

    def __init__(self,email, name, password):
        self.email = email
        self.name = name
        self.password = password

    def save_user(self):
        """
        Ajout de l'objet User à la BDD
        """
        db.session.add(self)
        db.session.commit()

    def delete_user(self):
        """
        Suppression de l'objet User de la BDD
        """
        db.session.delete(self)
        db.session.commit()
