#!/usr/bin/python3
# coding: utf-8 

from __future__ import unicode_literals

"""
    ERTIM - INALCO :  TECHNIQUES WEB (REST API)
    ------------------------------------------
    
    This module test all functionalities of API.
    
    :copyright: © 2020 by Elvis.
    :license: Creative Commons, see LICENSE for more details.
"""


__version__ = "0.1"


import unittest
from pathlib import Path
from flask import Response
from flask_restful import Api
import json


class TestURLs(unittest.TestCase):
    """ TestCase for back.resources module """
    
    def test_login(self):
        from front.models.api import login_api
        from front.app import dataviewerFront as frontend
        from back.app import dataviewerBack as backend

        tester = backend.test_client(self)
        response = tester.post('/register', data={'email':'abc@163.com', 'password':'1234'})
        self.assertEqual(response.status_code, 200)
    

if __name__ == '__main__':
    unittest.main(verbosity=8)