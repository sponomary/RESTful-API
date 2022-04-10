#!/usr/bin/python3
# coding: utf-8 

from __future__ import unicode_literals

"""
    M2 TAL, INGÉNIERIE MULTILINGUE : TECHNIQUES WEB (REST API)
    ------------------------------------------
    Ce module teste les fonctionnalités de l'API.
    :copyright: © 2022 by Élise & Lufei & Alexandra.
"""


__version__ = "0.1"


import unittest


class TestURLs(unittest.TestCase):
    """ TestCase for back.resources module """
    
    def test_login(self):
        from front.models.api import login_api
        from front.app import dataviewerFront as frontend
        from back.app import dataviewerBack as backend

        tester = backend.test_client(self)
        response = tester.post('/login', data={'email':'abc@163.com', 'password':'1234'})
        self.assertEqual(response.status_code, 200)
    
    def test_register(self):
        from back.app import dataviewerBack as backend

        tester = backend.test_client(self)
        response = tester.post('/register', data={'name':'Toto', 'email':'toto@163.com', 'password':'1234'})
        self.assertEqual(response.status_code, 200)
    
    def test_get_all_data(self):
        from back.app import dataviewerBack as backend

        tester = backend.test_client(self)
        response = tester.get('/covid/')
        self.assertEqual(response.status_code, 200)
    
    def test_create_data(self):
        from back.app import dataviewerBack as backend

        tester = backend.test_client(self)
        #token = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJlbWFpbCI6ImFiY2RAMTYzLmNvbSIsImV4cCI6MTY0OTYzMDczMX0.JnuHTGTlYWAjq2p0SLso97Vm6kT-rt5KAGGcjo6iTYk"
        #headers = {"x-access-token": token}
        response = tester.post('/covid/',
        #AJOUTER UN HEADERS ? POUR LE TOKEN ?
        data={
            "classe_age": "65-74",
            "commune_residence": 444,
            "date_reference": "2022-03-22",
            "effectif_1_inj": 0,
            "effectif_cumu_1_inj": 1750,
            "effectif_cumu_termine": 1730,
            "effectif_termine": 0,
            "libelle_classe_age": "de 65 à 74 ans",
            "libelle_commune": "SASHAVILLE",
            "population_carto": 680,
            "semaine_injection": "2021-44",
            "taux_1_inj": 0.018,
            "taux_cumu_1_inj": 0.747,
            "taux_cumu_termine": 0.823,
            "taux_termine": 0.010
        })
        #self.assertEqual(response.status_code, 200)
        self.assertNotEqual(response.status_code, 200)

    def test_get_one_data_from_id(self):
        from back.app import dataviewerBack as backend

        tester = backend.test_client(self)
        response = tester.get('/covid/512/')
        self.assertEqual(response.status_code, 200)

if __name__ == '__main__':
    unittest.main(verbosity=8)