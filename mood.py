from BoardState import BoardState, FOOD_LAYER
import numpy as np
moves = [(-1,0,0), (1,0,1), (0,1,2), (0,-1,3)]
import collections


global mood

def set_mood ( newMood):
    global mood
    mood = newMood

def score_board (board_state, snake):

    if board_state.getDead(snake): return float('-inf')

    if mood == 'center':
        return center( board_state, snake )

    if mood == 'close':
        return close( board_state, snake )

    if mood == 'hungry':
        return hungry( board_state, snake )

    if mood == 'rational':
        return rational( board_state, snake )

    return rational( board_state, snake )

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

def old_rational ( board_state, snake ):
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

# helper function - uses voronoi regions to measure control over the board
# can be modified to give a score for every snake without increasing runtime
def voronoi(state: BoardState, snake):
    depth = 0
    food_depth = -1
    q = collections.deque([])
    v = dict()
    counts = [0 for i in range(state.totalSnakes())]

    for i in range(len(counts)):    
        if not state.getDead(i):
            head = state.getHead(i)
            p = (head, i)
            q.append(p)
            v[head] = i
    q.append(None)

    while len(q) > 0:
        p = q.popleft()
        if p is None:
            depth += 1
            q.append(None)
            if q[0] is None:
                break
        else:
            head = p[0]
            idx = p[1]
            
            for point in [(head[0] + moves[m][0], head[1] + moves[m][1]) for m in range(4)]:
                if point in v:
                    other = v[point]
                    if other != -1 and other != idx:
                        counts[other] -= 1
                        v[point] = -1
                elif state.inBounds(point[0], point[1]) and state.isSafe(point[0], point[1], depth):
                    if food_depth == -1 and idx == snake and state.getLayer(FOOD_LAYER)[point]:
                        food_depth = depth
                    counts[idx] += 1
                    v[point] = idx
                    q.append((point, idx))
    
    return counts[snake], food_depth

def closest_food(state, snake):
    foods = state.getLayer(FOOD_LAYER)
    head = state.getHead(snake)
    depth = 0
    q = collections.deque([head])
    v = set(q)
    q.append(None)

    while len(q) > 0:
        current = q.popleft()
        if current is None:
            depth += 1
            q.append(None)
            if q[0] is None:
                break
        else:
            for point in [(current[0] + moves[m][0], current[1] + moves[m][1]) for m in range(4)]:
                if state.inBounds(point[0], point[1]) and state.isSafe(point[0], point[1], depth) and point not in v:
                    v.add(point)
                    if foods[point]:
                        return depth
    return depth

def rational(state, snake):
    score = 0
    
    num_alive = state.numAliveSnakes()
    length = state.getLength(snake)
    free_squares, owned_food_depth = voronoi(state, snake)
    if free_squares <= 5:
        return -1e8
    
    score += 1e4 / num_alive
    # print(f"num alive score = {1e5 / num_alive}")
    if num_alive == 2:
        score += 100 * np.log(free_squares)
    else:
        score += 10 * np.log(free_squares)
    # print(f"free square score = {100 * np.log(free_squares)}")
    if num_alive == 2:
        score += 16 * length
    else:
        score += 64 * length

    food_length = owned_food_depth
    if food_length == -1:
        food_length = closest_food(state, snake)
    if state.getHealth(snake) < food_length:
        return -1e8 # starvation is inevitable
    breathing_room = state.getHealth(snake) - food_length - 1
    score += 150 * np.arctan(0.12 * breathing_room - 0.5)
    if num_alive > 2:
        score -= 8 * food_length
    # print(f"Breathing room = {breathing_room} ({100 * np.arctan(0.12 * breathing_room):.4f})")
    # state.log("  ")
    # AVOID UNFAVORABLE HEAD-ONS
    
    
    return score
    