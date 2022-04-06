#!/usr/bin/python3
# coding: utf-8 

"""
    M2 TAL, INGÉNIERIE MULTILINGUE : TECHNIQUES WEB (REST API)
    -------------------------------------------
    Ce module lance l'API. 
    :copyright: © 2022 by Élise & Lufei & Alexandra.
"""

"""
🐽🐽🐽🐽🐽🐽🐽🐽🐽🐽🐽🐽🐽🐽🐽🐽🐽🐽🐽🐽🐽🐽🐽🐽🐽🐽🐽🐽🐽🐽🐽🐽🐽🐽🐽🐽🐽🐽🐽🐽🐽🐽🐽🐽🐽🐽
1 . ce programme permet de relier front & back, inspiré de code seigneur et de ce lien:
# https://www.peterspython.com/en/blog/two-flask-apps-frontend-and-admin-on-one-domain-using-dispatchermiddleware
2. j'ai donc changé le nom de notre app back en dataviewerBack
3. il faudrait peut etre réorganiser notre dossier avec une structure comme ca (notre RESTful-API --> backend)
├── projet_techniques_web
│   ├── backend
│   │   └── tous ce qu'on a dans le dossier RESTful-API
│   ├── frontend
│   │   ├── app.py
│   │   ├── models
│   │   ├── ressources
│   │   ├── static
│   │   ├── templates
│   ├── start_app.py
│   └── test.py (seigneur demande de faire des tests unitaires)
4. 
🐽🐽🐽🐽🐽🐽🐽🐽🐽🐽🐽🐽🐽🐽🐽🐽🐽🐽🐽🐽🐽🐽🐽🐽🐽🐽🐽🐽🐽🐽🐽🐽🐽🐽🐽🐽🐽🐽🐽🐽🐽🐽🐽🐽🐽🐽
"""
__version__ = "0.1"

from flask import Flask
from werkzeug.middleware.dispatcher import DispatcherMiddleware

# importer application backend et frontend
from front.app import dataviewerFront as frontend
from back.app import dataviewerBack as backend

# ------------------------------------------------------------------
# relier back & front dans une seule application avec WSGI 
# url pour accéder au front :127.0.0.1/
# url pour accéder au back : 
#   user : 127.0.0.1/api/
#   covid : 127.0.0.1/api/covid
application = DispatcherMiddleware(frontend, {
    '/api': backend
})

dataviwer_app = Flask(__name__)
dataviwer_app.wsgi_app = application

# ------------------------------------------------------------------

if __name__ == '__main__':
    dataviwer_app.run(host='127.0.0.1', port='5000', use_evalex=True,
                  use_reloader=True, use_debugger=True)