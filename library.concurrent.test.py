#!/usr/bin/python

import threading
import time
import json
from multiprocessing import Queue
from libraryRoutes import app

numReqs = 8

def evalAvg(res):
    # compute expected avg
    count = 0
    # offset by 1 since res[0] = []
    total = 1
    for val in res:
        if(val != 'success'):
            obj = eval(val)
            print 'obj = ', obj
            avg = obj[0]['avg'] if obj != [] else 0
            total += avg
            count += 1
    finalObj = res[len(res)-2] if len(res) % 2 == 0 else res[len(res)-1]
    finalAvg = eval(finalObj)[0]['avg']
    # TODO add round
    computedAvg = total / count
    print 'computed avg = ', computedAvg
    #print 'final avg = ', finalAvg

def sendRequest(data, queue):
    #print('data = ', data);
    if(data):
        print('CALL - addAction')
        res = app.test_client().post('/add-action', data=data, content_type='application/json')
        queue.put('success')
    else:
        print('CALL - getStats')
        res = app.test_client().get('/get-stats')
        queue.put(res.data)

def main():
    #create thread for each request
    queue = Queue()
    res = []
    threads = []
    for i in range(numReqs):
        if((i+1) % 2 == 0):
            data = json.dumps({'action': 'jump', 'time': i+1})
            th = threading.Thread(target=sendRequest, args=(data,queue))
        elif((i+1) % 5 == 0):
            data = json.dumps({'action': 'swim', 'time': i+1})
            th = threading.Thread(target=sendRequest, args=(data,queue))
        else:
            th = threading.Thread(target=sendRequest, args=(None, queue))
        th.start()
        res.append(queue.get())
    time.sleep(0.1)
    queue.close()
    queue.join_thread()
    for t in threads:
        t.join()
    print 'res = ', res
    # evaluate res
    #evalAvg(res)

if(__name__ == '__main__'):
    main()
