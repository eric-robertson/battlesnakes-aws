# Conversion between internal representation and the JSON blob provided by the server

import numpy as np

def parse_board ( json_game_state ):

    all_snakes = json_game_state["board"]["snakes"]
    total_snakes = len( all_snakes )
    shape = json_game_state["board"]["height"]
    you_id = json_game_state["you"]["id"]

    # Create a np array for the board to speed up computations
    # 2 extra layers ( 1 for food, 1 for metadata )
    board = np.zeros( (total_snakes + 2, shape, shape))

    # Assign yourself as snake #1, reserve index 0 for game perams
    load_snake( board, 1, json_game_state["you"])

    # Load the food on layer -1
    load_food( board, -1, json_game_state["board"]["food"])

    # Load all the other snakes to the remaining layers
    i = 2
    for snake in json_game_state["board"]["snakes"]:
        if snake["id"] != you_id:
            load_snake( board, i, snake )
            i += 1

    # Game is now loaded into a single Numpy Matrix
    return board

def load_snake ( board, index, json_snake ):
    
    # Load each body peice into the matrix
    for i,p in enumerate(json_snake["body"]):
        board[index][p["x"], p["y"]] = i+1

    # Set health & length
    board[0,index-1,0] = json_snake['health']
    board[0,index-1,1] = len(json_snake['body'])


def load_food ( board, index, food ):

    # Load each food peice into a layer
    for p in food:
        board[index][p["x"], p["y"]] = 1
