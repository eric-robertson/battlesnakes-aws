# Conversion between internal representation and the JSON blob provided by the server

import json
import numpy as np

# Create a board from a json blob of a given board
# (s+2, w+2, w+2)
def json_to_board (json_blob):

    json_blob = json_blob['board']

    snakes = json_blob['snakes']
    width = json_blob['width']
    foods = json_blob['food']

    raw_board = np.zeros((len(snakes) + 2, width + 2, width + 2)).astype('int8')

    # Encode everything in better representations
    _create_foods( foods, raw_board)
    for i,s in enumerate(snakes): 
        _create_snake( s, i, raw_board )

    return raw_board

def _create_foods ( foods, board ):
    for f in foods:
        board[ 0, f['x'] + 1, f['y'] + 1 ] = 1

def _create_snake ( snake, id, board ):

    length = len(snake['body'])
    realized_length = 0
    health = snake['health']
    head = snake['head']['x'] + 1, snake['head']['y'] + 1

    for i,body in enumerate( snake['body'] ):
        pos = body['x'] + 1, body['y'] + 1 
        if board[ 2+id, pos[0], pos[1] ] == 0:
            realized_length += 1
            board[ 2+id, pos[0], pos[1] ] = length - i


    board[ 1, id, 0 ] = head[0]
    board[ 1, id, 1 ] = head[1]
    board[ 1, id, 2 ] = length
    board[ 1, id, 3 ] = realized_length
    board[ 1, id, 4 ] = health
