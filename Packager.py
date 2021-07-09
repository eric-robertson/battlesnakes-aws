# Conversion between internal representation and the JSON blob provided by the server
# Assuming all boards have 2 snakes and 11 size

import json
from BoardState import BoardState
import numpy as np

# Create a board from a json blob
def from_json (json_blob):

    data = np.zeros((4,11,11))


    # Load body into arrays
    for s,snake in enumerate(json_blob['board']['snakes']):

        # Load body
        for i,body in enumerate(snake['body']):
            if data[s][body['x'], body['y']] == 0:
                data[s][body['x'], body['y']] = i+1

        # Set health & length info
        data[2,s,0] = snake['health']
        data[2,s,1] = snake['length']

    # Load food
    for food in json_blob['board']['food']:
        data[3, food['x'], food['y']] = 1

    # Construct
    return BoardState( data )

