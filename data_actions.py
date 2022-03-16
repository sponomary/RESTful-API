from app import db, DATA_COVID


# ajouter des informations dans bdd
def add_one_by_one(data):
    db.session.add(data)
    db.session.commit()

# consulter des donées du bdd
def get_info_by_id(id_user):
    data = DATA_COVID.query.get(id_user)
    all_user_info = {"date_reference": data.date_reference,
                        "semaine_injection":data.semaine_injection,
                        "commune_residence":data.commune_residence,
                        "libelle_commune":data.libelle_commune,
                        "population_carto":data.population_carto,
                        "classe_age":data.classe_age,
                        "libelle_classe_age":data.libelle_classe_age,
                        "effectif_1_inj":data.effectif_1_inj,
                        "effectif_termine":data.effectif_termine,
                        "effectif_cumu_1_inj":data.effectif_cumu_1_inj,
                        "effectif_cumu_termine":data.effectif_cumu_termine,
                        "taux_1_inj":data.taux_1_inj,
                        "taux_termine":data.taux_termine,
                        "taux_cumu_1_inj":data.taux_cumu_1_inj,
                        "taux_cumu_termine":data.taux_cumu_termine,
                        "date":data.date
                    }
    print(all_user_info)

# modifier les informations du bdd
def change_info_by_id(id_user, item_to_change, new_info):
    user = DATA_COVID.query.filter(DATA_COVID.id == id_user).update({item_to_change: new_info})
    db.session.commit()


# supprimer des informations du bdd
def delete_info_by_id(id_user):
    user = DATA_COVID.query.filter(DATA_COVID.id == id_user).delete()
    db.session.commit()


if __name__ == '__main__':
    get_info_by_id(6)
    #change_info_by_id(7, "classe_age", "40-54")
    #delete_info_by_id(25)