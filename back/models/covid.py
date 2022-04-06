from .db import db, ma
from datetime import datetime


class DataCovidModel(db.Model):
    __tablename__ = 'DATA_COVID'

    id = db.Column(db.Integer, primary_key=True)
    date_reference = db.Column(db.Date)  # %Y-%m-%d
    semaine_injection = db.Column(db.String(100))
    commune_residence = db.Column(db.Integer)
    libelle_commune = db.Column(db.String(100))
    population_carto = db.Column(db.Integer)
    classe_age = db.Column(db.String(100))
    libelle_classe_age = db.Column(db.String(100))
    effectif_1_inj = db.Column(db.Integer)
    effectif_termine = db.Column(db.Integer)
    effectif_cumu_1_inj = db.Column(db.Integer)
    effectif_cumu_termine = db.Column(db.Integer)
    taux_1_inj = db.Column(db.Float)
    taux_termine = db.Column(db.Float)
    taux_cumu_1_inj = db.Column(db.Float)
    taux_cumu_termine = db.Column(db.Float)
    date = db.Column(db.Date, default=datetime.utcnow)  # %Y-%m-%d

    def __init__(self, date_reference, semaine_injection, commune_residence, libelle_commune, population_carto,
                 classe_age, libelle_classe_age, effectif_1_inj, effectif_termine, effectif_cumu_1_inj,
                 effectif_cumu_termine, taux_1_inj, taux_termine, taux_cumu_1_inj, taux_cumu_termine, date):
        self.date_reference = date_reference
        self.semaine_injection = semaine_injection
        self.commune_residence = commune_residence
        self.libelle_commune = libelle_commune
        self.population_carto = population_carto
        self.classe_age = classe_age
        self.libelle_classe_age = libelle_classe_age
        self.effectif_1_inj = effectif_1_inj
        self.effectif_termine = effectif_termine
        self.effectif_cumu_1_inj = effectif_cumu_1_inj
        self.effectif_cumu_termine = effectif_cumu_termine
        self.taux_1_inj = taux_1_inj
        self.taux_termine = taux_termine
        self.taux_cumu_1_inj = taux_cumu_1_inj
        self.taux_cumu_termine = taux_cumu_termine
        self.date = date


    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()

    def to_dict(self):
        return {c.name: str(getattr(self, c.name)) for c in self.__table__.columns}


class DataCovidSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = DataCovidModel

    def __repr__(self):
        return '<Data %r>' % self.id
