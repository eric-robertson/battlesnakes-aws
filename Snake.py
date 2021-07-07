import numpy as np

import GamePackager
import GamePredictor
import ScoreBoard

# Actual logic for the Battlesnake

MOVE_DICT = {"L" : "left", "R" : 'right', "U" : 'up', "D" : "down"}

def start ( request_data ):
    return ""

def move ( request_data):
    
    game_board = GamePackager.parse_board( request_data )
    health, food, futures = GamePredictor.get_next_states( game_board )
    best_move = ScoreBoard.generate_board_scores( health, food, futures )

    return MOVE_DICT[best_move]