# Library
This provides 2 API endpoints `add-action` and `get-stats` that handle concurrent requests.

### Environment
- python 2.7

### Dependencies
- uWSGI server
- Flask 

### Setup
First clone the repo:  
`git clone https://github.com/callie-jones/library.git`

`cd` into the library directory and execute:  
`pip install flask`  
`pip install wsgi`

To run using WSGI server, from the directory `/library` execute:  
`uwsgi wsgi.ini`

To run using Flask, from the directory `/library` execute:  
`python libraryApp.py`

Once the server is running, to make a request to the server, open a new terminal and execute:  
```
// request get-stats
curl http://localhost:5000/v1/get-stats

// request add-action
curl --header "Content-Type: application/json" -d "{\"action\":\"jump\",\"time\":100}" http://localhost:5000/v1/add-action
```

You can also make requests through Postman using this collection.

[![Run in Postman](https://run.pstmn.io/button.svg)](https://app.getpostman.com/run-collection/9f4837d926a362aa9575)

### Testing
I included a test file in `/library/test` that tests each API endpoint for a successful and unsuccessful response. This also tests making concurrent requests.

These API endpoints can be tested by executing:  
`python /test/library.test.py`

