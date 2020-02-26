#!/usr/bin/python

import flask
from flask import request
import json
import threading
from urllib2 import HTTPError

app = flask.Flask(__name__)
application = app

dataLock = threading.Lock()
data = dict()

@app.route('/v1/add-action', methods=['POST'])
def addAction():
    try:
        actObj = json.loads(request.data)
        dataLock.acquire()
        print('before data = ' + json.dumps(data))
        # check if action does NOT exist in data add action otherwise update action
        if(not actObj['action'] in data.keys()):
            count = 1
            data[actObj['action']] = {'avg': actObj['time'], 'count': count}
        else:
            count = data[actObj['action']]['count'] + 1
            # TODO handle explicit round
            newAvg = (data[actObj['action']]['avg'] + actObj['time']) / count
            data[actObj['action']] = {'avg': newAvg, 'count': count}
        print('after data = ' + json.dumps(data))
        dataLock.release()
        return json.dumps({'status': 200, 'message': 'Success'})
    except Exception as err:
        print("Library.addAction - Error: " + str(err))
        raise HTTPError(500, "Internal Server Error")

@app.route('/v1/get-stats', methods=['GET'])
def getStats():
    try:
        res = []
        # acquire lock before entering critical section
        dataLock.acquire()
        print("data = " + json.dumps(data))
        for key in data:
            res.append({'action': key, 'avg': data[key]['avg']})
        dataLock.release()
        return json.dumps(res)
    except Exception as err:
        print("Library.getStats() - Error: " + str(err))
        raise HTTPError(500, "Internal Server Error")
