# Conversion between internal representation and the JSON blob provided by the server
# Assuming all boards have 2 snakes and 11 size

import json
from BoardState import *
import numpy as np

# Create a board from a json blob
def from_json (json_blob):

    width = json_blob['board']['width']
    height = json_blob['board']['height']
    snakes = json_blob['board']['snakes']

    # two layers for information, the rest for snakes
    data = np.zeros((SNAKES_IDX + len(snakes), width, height), dtype=np.int32)

    # Load body into arrays
    for s,snake in enumerate(snakes):

        # Load body
        for i,body in enumerate(snake['body']):
            if data[SNAKES_IDX+s][body['x'], body['y']] == 0:
                data[SNAKES_IDX+s][body['x'], body['y']] = i+1

        # Set health & length info
        data[INFO_LAYER, s, HEALTH_IDX] = snake['health']
        data[INFO_LAYER, s, LENGTH_IDX] = snake['length']

    # Load food
    for food in json_blob['board']['food']:
        data[FOOD_LAYER, food['x'], food['y']] = 1
    for hazard in json_blob['board']['hazards']:
        data[HAZARD_LAYER, hazard['x'], hazard['y']] = 1

    # Construct
    return BoardState( data )

def find_me(json_blob):
    my_id = json_blob['you']['id']
    snakes = json_blob['board']['snakes']
    for s,snake in enumerate(snakes):
        if snake['id'] == my_id:
            return s

