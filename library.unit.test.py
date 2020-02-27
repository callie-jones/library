#!/usr/bin/python
import threading
import json
import unittest
from libraryRoutes import app

class LibraryTest(unittest.TestCase):
    def setUp(self):
        self.test_app = app.test_client()

    # receives a valid response
    # def testAddActionValid(self):
    #     data = json.dumps({'action': 'jump', 'time': 10})
    #     res = self.test_app.post('/add-action', data=data, content_type='application/json')
    #     self.assertEqual(res.status_code, 200)

    # receives a 500 HTTP error
    # def testAddActionInvalid(self):
    #     data = json.dumps({})
    #     res = self.test_app.post('/add-action', data=data, content_type='application/json')
    #     self.assertEqual(res.status_code, 500)

    # receives a valid response
    def testGetStatsValid(self):
        res = self.test_app.get('/get-stats')
        self.assertEqual(res.status_code, 200)

    # receives a 500 HTTP error
    # def testGetStatsInvalid(self):
    #     res = self.test_app.get('/get-stats', data="test", content_type='')
    #     self.assertEqual(res.status_code, 200)

if(__name__ == '__main__'):
    unittest.main()