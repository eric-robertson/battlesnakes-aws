from BoardState import BoardState, FOOD_LAYER
import numpy as np

global mood

def set_mood ( newMood):
    global mood
    mood = newMood

def score_board (board_state, snake ):

    if board_state.getDead(snake): return float('-inf')

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

# helper function - uses voronoi regions to measure control over the board
# can be modified to give a score for every snake without increasing runtime
def voronoi(state: BoardState, snake):
    depth = 0
    food_depth = -1
    q = [] # TODO: change to dequeue
    v = dict()
    counts = [0 for i in range(state.totalSnakes())]

    for i in range(len(counts)):    
        if not state.getDead(i):
            head = state.getHead(i)
            print("head = ", head)
            p = (head, i)
            q.append(p)
            v[head] = i
    q.append(None)

    while len(q) > 0:
        p = q.pop(0) # very inefficient
        if p is None:
            depth += 1
            q.append(None)
            if q[0] is None:
                break
        else:
            head = p[0]
            idx = p[1]
            
            for point in state.neighbors(head):
                if point in v:
                    other = v[point]
                    if other != -1 and other != idx:
                        counts[other] -= 1
                        v[point] = -1
                elif state.inBounds(point) and state.isSafe(point, depth):
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
    q = [head]
    v = set(q)
    q.append(None)

    while len(q) > 0:
        current = q.pop(0)
        if current is None:
            depth += 1
            q.append(None)
            if q[0] is None:
                break
        else:
            for point in state.neighbors(current):
                if state.inBounds(point[0], point[1]) and state.isSafe(point, depth) and point not in v:
                    v.add(point)
                    if foods[point]:
                        return depth
    return depth

def rational2(state, snake):
    score = 0
    
    num_alive = state.numAliveSnakes()
    length = state.getLength(snake)
    free_squares, owned_food_depth = voronoi(state, snake)
    if free_squares == 0:
        return float('-inf')
    
    score += 1e5 / num_alive
    score += 10 * free_squares
    score += 0.8 / length

    food_length = owned_food_depth
    if food_length == -1:
        food_length = closest_food(state, snake)
    if state.getHealth(snake) < food_length:
        return float('-inf') # starvation is inevitable
    breathing_room = snake.health - food_length
    score += 100 * np.tanh(0.15 * breathing_room)
    
    return score
    