import numpy as np

global mood

def set_mood ( newMood):
    global mood
    mood = newMood

def score_board (board_state, snake ):

    if board_state.getDead(snake): return -9999

    if mood == 'center':
        return center( board_state, snake )

    if mood == 'close':
        return close( board_state, snake )

    if mood == 'hungry':
        return hungry( board_state, snake )

    if mood == 'rational':
        return rational( board_state, snake )

    return center( board_state, snake ) * (board_state.getHealth(snake) / 100)

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

def rational ( board_state, snake ):
    score = 0

    if board_state.getLength(snake) > board_state.getLength(1-snake):
        score += 200
    if board_state.getHealth(snake) > board_state.getHealth(1-snake):
        score += 10

    score += board_state.getLength(snake) * 50

    _, xs, ys = board_state.getHeads()
    score += 1000/( abs(xs[0]-xs[1]) + abs(ys[0]-ys[1]) + 0.15 )
    
    if xs[0] > 1 and xs[0] < 9 and ys[0] > 1 and ys[0] < 9:
        score += 100
    
    if ys[1] == 0 or ys[1] == 10 or xs[1] == 0 or xs[1] == 10:
        score += 50

    if board_state.getHealth(snake) < 50: 
        return score * board_state.getHealth(snake)/50

    return score