from flask import Blueprint, request, flash, redirect, render_template, session, url_for

# IMPORTER ICI NOUVELLES FONCTIONS QUI FONT LE LIEN ENTRE FRONT ET BACK
#from front.models.api import 

covid = Blueprint('covid', __name__)

@covid.route('/data',methods=('GET', 'POST'))
def data():
    return render_template('data.html')