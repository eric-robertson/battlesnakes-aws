'''
Generic starter code for battlesnakes
'''

from os import system
import sys
import json
from flask import Flask, request
import Snake
import logging
import mood

log = logging.getLogger('werkzeug')
log.disabled = True

app = Flask(__name__)
_id = 0

@app.route('/<_mood>/')
def hello(_mood):
    global _id

    print(_mood)

    # Load snake metadata
    f = open('snake_data.json')
    data = json.load( f )
    f.close() 

    # Return data
    print("Fielded /")
    data['hello_response']['apiversion'] = _mood
    data['hello_response']['author'] = _mood
    _id += 1
    return data['hello_response']

@app.route('/<_mood>/start', methods=['POST'])
def start (_mood):

    # Get request body
    data = request.get_json()
    print("Fielded /start")

    # Trigger handler
    start_response = Snake.start( data )

    # Return data
    return start_response

@app.route('/<_mood>/move', methods=['POST'])
def move (_mood):

    # Get request body
    data = request.get_json()
    print("Fielded /move")

    # Trigger handler
    mood.set_mood(_mood)
    move_response = Snake.move( data )

    # Return data
    return {"move":move_response}

app.run(host="localhost", port=sys.argv[1])