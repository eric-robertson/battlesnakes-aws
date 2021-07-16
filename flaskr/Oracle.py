# This is the predictor that takes in a current game state and produces all the next possible games states
from . import Clippers

import numpy as np
moves = [(-1,0,0), (1,0,1), (0,1,2), (0,-1,3)]

def decode ( i ):
    return (['left', 'right', 'up', 'down'])[i]


# Computes all possible resultant board states
def prophesize ( board_state ):

    results = {}

    # Get heads
    _, xs, ys = board_state.getHeads()

    # Get possible next heads for each snake
    snake_0_moves = compute_next_heads( xs[0], ys[0])
    snake_1_moves = compute_next_heads( xs[1], ys[1])

    # Create board states themselves
    for head0,move0 in snake_0_moves:
        for head1,move1 in snake_1_moves:

            # Create a new board and simulate the state, giving it a score for player 0
            new_board = board_state.clone()
            new_board.do_game_tick( head0, head1 )

            if logging: print( decode(move0), decode(move1))
            if logging: new_board.log()
            board_score = judge( new_board )

            # If the board is even playable, lets check it out
            results[(move0,move1)] = ( new_board, board_score )

    return results

def compute_next_heads ( head_x, head_y ):

    valid_moves = []

    for i,move in enumerate(moves):
        x = head_x + moves[i][0]
        y = head_y + moves[i][1]

        if x >=0 and y >= 0 and x < 11 and y < 11:
            valid_moves.append(((x,y),moves[i][2]))

    return valid_moves

    