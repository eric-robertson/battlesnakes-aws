import numpy as np

global mood

def set_mood ( newMood):
    global mood
    mood = newMood

def score_board (board_state, snake ):

    if board_state.getDead(snake): return -np.inf

    if mood == 'center':
        return center( board_state, snake )

    if mood == 'close':
        return close( board_state, snake )

    if mood == 'hungry':
        return hungry( board_state, snake )

    return center( board_state, snake )

def center ( board_state, snake ):
    _, xs, ys = board_state.getHeads()
    center_ness = 20/abs(5.5-xs[snake]) + 20/abs(5.5-ys[snake])
    return (board_state.getLength(snake))*40 + center_ness

def close ( board_state, snake ):
    _, xs, ys = board_state.getHeads()
    close_ness = 20/( abs(xs[0]-xs[1] + 0.15) + abs(ys[0]-ys[1] + 0.15 ) )
    return close_ness

def hungry ( board_state, snake ):
    return board_state.getLength(snake)