#!/usr/bin/python3
# coding: utf-8 

"""
    M2 TAL, INGÉNIERIE MULTILINGUE : TECHNIQUES WEB (REST API)
    -------------------------------------------
    Ce module lance l'API. 
    :copyright: © 2022 by Élise & Lufei & Alexandra.
"""

__version__ = "1.0"

from flask import Flask
from werkzeug.middleware.dispatcher import DispatcherMiddleware

# importer applications backend et frontend
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

dataviewer_app = Flask(__name__)
dataviewer_app.wsgi_app = application
dataviewer_app.config['DEBUG'] = True
dataviewer_app.config['SERVER_NAME'] = 'dataviewer.localhost:5000'

# ------------------------------------------------------------------

if __name__ == '__main__':
    dataviewer_app.run(use_evalex=True, use_reloader=True, use_debugger=True)
