# Takes in a collection of game board options and scores each result for computations

import numpy as np

def generate_board_scores ( health, food, move_options ):

    # Construct all possible futures
    all_options = generate_options( move_options, 0 )

    # This also needs to be different, but here for now
    best = 0
    move = "L"

    # Process and Score each one
    for option in all_options:
        _board, encoded_option = generate_board( health, food, move_options, option)
        _deaths = process_board( _board )
        _scores = score_board( _board, _deaths )

        if sum(_scores) > best:
            best = sum(_scores)
            move = encoded_option[0]

        # Debug for now
        print( encoded_option, _scores )

    return move


def generate_board ( health, food, move_options, future ):

    _results = [health]
    _encoding = []
    
    # Generate the given board for the future predictor
    for i in range(len(move_options)):
        _next = future % 10
        _results.append( move_options[i][_next][0] )
        _encoding.append( move_options[i][_next][1] )
        future //= 10

    _results.append( food )

    return np.stack( _results ).copy(), _encoding

def generate_options ( move_options, i):

    # How far are we
    depth = len(move_options)
    
    # If we have finished a generation return
    if i == depth: return [0]

    # If we still have options to consider, generate them
    else:
        results = []
        next_options = generate_options( move_options, i + 1)
        for index in range(len(move_options[i])):
            this_option = ((10 ** i) * index)
            for next in next_options:
                results.append( this_option + next )
        return results
             
# Takes a board and computes player-to-player interactions
# And if any food is eaten
def process_board ( board ):    
    
    players = board.shape[0] - 2
    deaths = [0] * players

    # Did anyone collide?
    for p1 in range( players ):
        for p2 in range( players ):
            if p1 != p2:
                _intersect = board[p1+1] * board[p2+1]
                if np.any(_intersect):
                    print(f"Player {p1} & {p2} collide")
                    
                    x,y = np.where(_intersect)
                    p1_ishead = board[p1+1][x[0], y[0]] == 1
                    p2_ishead = board[p2+1][x[0], y[0]] == 1

                    # p1 hits p2's body
                    if p1_ishead and not p2_ishead:
                        deaths[p1] = 1
                    # p2 hits p1's body
                    elif not p1_ishead and p2_ishead:
                        deaths[p2] = 1
                    # head-on-head, p1 is bigger
                    elif board[0,p1,1] > board[0,p2,1]:
                        deaths[p2] = 1
                    # head-on-head, p2 is bigger
                    elif board[0,p1,1] < board[0,p2,1]:
                        deaths[p1] = 1
                    # both die
                    else:
                        deaths[p1] = 1
                        deaths[p2] = 1

    # Did anyone get food?
    for p1 in range( players ):
        _intersect = board[p1 + 1] * board[-1]

        # Give the food to the snake, remove it from board
        if np.any(_intersect):
            print(f"Player {p1} hit food")
            board[-1][np.where(_intersect)] = 0
            board[0,p1,0] = 100
            board[0,p1,1] += 1

    # Anyone starve?
    starved = np.where(board[0,:,0] <= 0)
    for i in starved:
        if i[0] < players:
            print(f"Player {i[0]} starved")
            deaths[i[0]] = 1

    return deaths


# Scores a board for each player, give each a score
# If you are dead you get a bad score haha
def score_board ( board, deaths):

    players = board.shape[0] - 2
    scores = []

    for p1 in range( players ):
        if deaths[p1] != 0:
            scores.append( - np.inf )
        else:
            scores.append( score_player( board, p1 ))

    return scores

# How did a given player perform?
def score_player ( board, player ):

    # For now, this metric will just be health
    # This is not a good overall metric, but this is what can be tweeked later
    # Consider doing something more advance here

    return board[0,player,0]
