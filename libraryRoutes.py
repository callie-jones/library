#!/usr/bin/python

import flask
from flask import request
import json
import threading
from urllib2 import HTTPError
from libraryController import addAction, getStats, handler

app = flask.Flask(__name__)
application = app

dataLock = threading.Lock()
data = dict()

@app.route('/add-action', methods=['POST'])
def addActionRoute():
    if(not request.get_json().keys()):
        raise HTTPError(400, 'Bad Request')
    else:
        return handler(addAction, request.data)

@app.route('/get-stats', methods=['GET'])
def getStatsRoute():
    res = handler(getStats, None)
    #print('res.data = ', json.dumps(res))
    return res

@app.errorhandler(Exception)
def errHandler(err):
    print('LibraryRoutes.errHandler - Error: ', err)
    return {'message': str(err)}, getattr(err, 'code', 500)
