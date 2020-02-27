#!/usr/bin/python

import threading
import time
import json
from multiprocessing import Queue
from libraryRoutes import app

numReqs = 200

def evalAvg(datas, finalAvg):
    # compute expected avg
    actions = dict()
    computedAvg = []
    for data in datas:
        actionObj = eval(data)
        if(actionObj['action'] not in actions.keys()):
            actions[actionObj['action']] = {'time': actionObj['time'], 'count': 1}
        else:
            newCount = actions[actionObj['action']]['count'] + 1
            newTime = actions[actionObj['action']]['time'] + actionObj['time']
            actions[actionObj['action']] = {'time': newTime, 'count': newCount}
    for key in  actions.keys():
        actAvg = actions[key]['time'] / actions[key]['count']
        act = {'action': key, 'avg': actAvg}
        computedAvg.append(act)
    return eval(finalAvg) == computedAvg

def sendRequest(data, queue):
    if(data):
        res = app.test_client().post('/add-action', data=data, content_type='application/json')
        queue.put(data)
    else:
        res = app.test_client().get('/get-stats')
        queue.put(res.data)

def main():
    # create thread for each request
    queue = Queue()
    datas = []
    res = []
    threads = []
    for i in range(numReqs):
        if(i == numReqs-1):
            th = threading.Thread(target=sendRequest, args=(None, queue))
        elif((i+1) % 2 == 0):
            data = json.dumps({'action': 'jump', 'time': i+1})
            datas.append(data)
            th = threading.Thread(target=sendRequest, args=(data,queue))
        elif((i+1) % 5 == 0):
            data = json.dumps({'action': 'swim', 'time': i+1})
            datas.append(data)
            th = threading.Thread(target=sendRequest, args=(data,queue))
        else:
            th = threading.Thread(target=sendRequest, args=(None, queue))
        th.start()
        res.append(queue.get())
    # need queue delay when numReqs is small
    if(numReqs < 10): time.sleep(0.1)
    queue.close()
    queue.join_thread()
    for t in threads:
        t.join()
    # evaluate res
    if(evalAvg(datas, res[len(res)-1])):
        print 'Success'
    else:
        print 'Failed'

if(__name__ == '__main__'):
    main()
