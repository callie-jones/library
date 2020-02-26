#!/usr/bin/python
from flask import Flask
import threading
import json
import unittest
from urllib2 import HTTPError
from libraryApp import app

class LibraryTest(unittest.TestCase):
    def setUp(self):
        self.test_app = app.test_client()

    def testAddActionValid(self):
        data = json.dumps({'action': 'jump', 'time': 10})
        res = self.test_app.post('/v1/add-action', data=data, content_type='application/json')
        self.assertEqual(res.status_code, 200)

if(__name__ == '__main__'):
    #threading.Thread(target=test)
    unittest.main()