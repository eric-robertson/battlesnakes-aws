import numpy as np

import Clippers
from Node import Node
import Oracle
import Packager
import time

# Actual logic for the Battlesnake

def start ( request_data ):
    return ""

def move ( request_data):
    
    start = time.time() * 1000

    # Construct the game board object, this is a 2D-array for storing metadata
    game_board = Packager.from_json( request_data )
    game_tree = Node( 0.5, game_board, False, 'root' )

    # Start tree search
    while True:
        
        target_branch = Clippers.select_brach()
        next_branches = Oracle.prophesize( target_branch.board )
        target_branch.register_childen( next_branches )

        now = time.time() * 1000
        if ( now - start > 450 ): break
        
    # Finished, lets get our best board
    score, move = game_tree.get_prediction()

    Clippers.clear_job_tree()
    return ['left', 'right', 'up', 'down'][move]