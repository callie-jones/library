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

To run using Flask, from the directory `/library` 
You will need to add the following to `libraryRoutes.py`:  
```
if(__name__ == '__main__'):
    app.run()
```
Then you can execute:  
`python libraryRoutes.py`

Once the server is running, to make a request to the server, open a new terminal and execute:  
```
// request get-stats
curl http://localhost:5000/v1/get-stats

// request add-action
curl --header "Content-Type: application/json" -d "{\"action\":\"jump\",\"time\":100}" http://localhost:5000/add-action

curl --header "Content-Type: application/json" -d "{\"action\":\"jump\",\"time\":100}" http://localhost:5000/add-action

curl --header "Content-Type: application/json" -d "{\"action\":\"run\",\"time\":10}" http://localhost:5000/add-action

curl --header "Content-Type: application/json" -d "{\"action\":\"walk\",\"time\":100}" http://localhost:5000/add-action

curl --header "Content-Type: application/json" -d "{\"action\":\"swim\",\"time\":100}" http://localhost:5000/add-action

curl http://localhost:5000/get-stats
```

To test concurrent requests through the terminal, you can use tmux.
install tmux  
`sudo apt install tmux`

split terminal vertically  
`ctrl` + `b` then `shift` + `%`

split the terminal horizontally  
`ctrl` + `b` then `shift` + `''`

then use `ctrl` + `b` and arrow keys to switch panes

then enter a curl request into each pane
then to execute each pane concurrently:  
`ctrl` + `b` then `:setw synchronize-panes on`

You can also make requests through Postman using this collection.

[![Run in Postman](https://run.pstmn.io/button.svg)](https://app.getpostman.com/run-collection/9f4837d926a362aa9575)

### Testing
I included 2 test files in that tests each API endpoint for a successful and unsuccessful response and also tests making concurrent requests.

These API endpoints can be tested by executing:  
`python library.unit.test.py`
`python library.concurrent.test.py`

Additionally the var `numReqs` in `library.concurrent.test.py` can be adjusted. I tested up to 200.

