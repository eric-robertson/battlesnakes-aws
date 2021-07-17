import Converter, Node, Tree

import numpy as np
import time

MIN_SEARCH_TIME = 430 # milliseconds

def start ( request_data ):
    return ""

def move ( request_data):
    
    start = time.time() * 1000

    # Construct the game board object, this is a 2D-array for storing metadata
    game_board = Converter.json_to_board( request_data )
    root = Tree.register_root(game_board)

    # Start tree search
    while True:

        Tree.compute_branches( 2 )
        
        now = time.time() * 1000
        if ( now - start > MIN_SEARCH_TIME ): break
        
    # Finished, lets get our best board
    move, transient, _ = root.report()
    move_name = ['left', 'right', 'up', 'down'][move]

    print(move_name, 'predicting score', transient)

    return move_name