'''
Generic starter code for battlesnakes
'''

from os import system
import json
from flask import Flask, request
import Snake
import logging

log = logging.getLogger('werkzeug')
log.disabled = True

app = Flask(__name__)

@app.route('/')
def hello():

    # Load snake metadata
    f = open('snake_data.json')
    data = json.load( f )
    f.close()

    # Return data
    print("Fielded /")
    return data['hello_response']

@app.route('/start', methods=['POST'])
def start ():

    # Get request body
    data = request.get_json()
    print("Fielded /start")

    # Trigger handler
    start_response = Snake.start( data )

    # Return data
    return start_response

@app.route('/move', methods=['POST'])
def move ():

    # Get request body
    data = request.get_json()
    print("Fielded /move")

    # Trigger handler
    move_response = Snake.move( data )

    # Return data
    return {"move":move_response}

if __name__ == '__main__':
    app.run(host='0.0.0.0',port=8080)