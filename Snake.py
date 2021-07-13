import numpy as np

import Clippers
from Node import Node
import Oracle
import Packager
import time
import AlphaBeta

MIN_SEARCH_TIME = 450 # milliseconds

def start ( request_data ):
    return ""

def move ( request_data):
    
    start = time.time() * 1000

    # Construct the game board object, this is a 2D-array for storing metadata
    game_board = Packager.from_json( request_data )

    strategy = "AlphaBeta"
    if strategy == "AlphaBeta":
        player = Packager.find_me( request_data )
        max_depth = 2
        if game_board.numAliveSnakes() <= 2:
            max_depth = 2
        move = AlphaBeta.decide_move(game_board, player, max_depth)
        now = time.time() * 1000
        print(f"Latency = {now - start}")
        return ['left', 'right', 'up', 'down'][move]

    game_tree = Node( 0.5, game_board, False, 'root' )

    # Start tree search
    while True:
        
        has_next, target_branch = Clippers.select_brach()
        if not has_next: break

        next_branches = Oracle.prophesize( target_branch.board )
        target_branch.register_childen( next_branches )

        now = time.time() * 1000
        if ( now - start > MIN_SEARCH_TIME ): break
        
    # Finished, lets get our best board
    score, move = game_tree.get_prediction()
    print(['left', 'right', 'up', 'down'][move], 'with score', round(score,2))

    Clippers.clear_job_tree()
    return ['left', 'right', 'up', 'down'][move]