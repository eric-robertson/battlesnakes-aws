from . import Snake

from flask import Flask, request

import os, sys, logging, json
from os import system
_id = 0

def create_app(test_config=None):
    log = logging.getLogger('hmmoro')
    log.disabled = True
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        # DATABASE=os.path.join(app.instance_path, 'flaskr.sqlite'),
    )

    # if test_config is None:
    #     # load the instance config, if it exists, when not testing
    #     app.config.from_pyfile('config.py', silent=True)
    # else:
    #     # load the test config if passed in
    #     app.config.from_mapping(test_config)

    # # ensure the instance folder exists
    # try:
    #     os.makedirs(app.instance_path)
    # except OSError:
    #     pass

    # a simple page that says hello
    @app.route('/')
    def helloo():
        return 'Hello, Worrld!'
    
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
        print("Fielded /move", _mood)
        # print(data) # for testing

        # Trigger handler
        mood.set_mood(_mood)
        move_response = Snake.move( data )

        # Return data
        return {"move":move_response}


    return app
