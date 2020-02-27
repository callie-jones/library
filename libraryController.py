#!/usr/bin/python

import json
import threading
from urllib2 import HTTPError
from multiprocessing import Queue

dataLock = threading.Lock()
data = dict()

def handler(method, data):
    try:
        queue = Queue()
        th = None
        if(data):
            th = threading.Thread(target=method, args=(data, queue))
        else:
            th = threading.Thread(target=method, args=(queue,))
        th.start()
        res = queue.get()
        th.join()
        if(isinstance(res, Exception)):
            raise HTTPError(500, "Internal Server Error")
        return res
    except Exception as err:
        print('LibraryController.handler - Error: ', err)
        return HTTPError(500, "Internal Server Error")

def addAction(action, queue):
    try:
        actObj = json.loads(action)
        dataLock.acquire()
        # check if action does NOT exist in data add action otherwise update action
        if(not actObj['action'] in data.keys()):
            count = 1
            data[actObj['action']] = {'avg': actObj['time'], 'count': count}
        else:
            count = data[actObj['action']]['count'] + 1
            # TODO handle explicit round
            newAvg = (data[actObj['action']]['avg'] + actObj['time']) / count
            data[actObj['action']] = {'avg': newAvg, 'count': count}
        dataLock.release()
        queue.put(json.dumps({'status': 200, 'message': 'Success'}))
    except Exception as err:
        print("LibraryController.addAction - Error: " + str(err))
        queue.put(err)

def getStats(queue):
    try:
        res = []
        # acquire lock before entering critical section
        dataLock.acquire()
        for key in data:
            res.append({'action': key, 'avg': data[key]['avg']})
        queue.put(json.dumps(res))
        dataLock.release()
    except Exception as err:
        print("LibraryController.getStats() - Error: " + str(err))
        queue.put(err)
