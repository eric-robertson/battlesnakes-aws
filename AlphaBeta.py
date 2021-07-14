# alpha-beta pruning search
from BoardState import *
import numpy as np
import mood
from Oracle import decode
import collections

moves = [(-1,0,0), (1,0,1), (0,1,2), (0,-1,3)]

def decide_move(state, player, max_depth):
    head_avoiding_moves = check_for_head_on(state, player)
    print(head_avoiding_moves)
    if len(head_avoiding_moves) == 1:
        print("move (AVOIDING HEAD-ON) =", decode(head_avoiding_moves[0]))
        return head_avoiding_moves[0]
    
    traps = check_for_trap(state, player)
    trap_avoiding_moves = np.where(traps > 15)[0]
    print(traps)
    if trap_avoiding_moves.shape[0] <= 1:
        move = np.argmax(traps)
        print("move (AVOIDING TRAP) =", decode(move))
        return move
    
    next_heads = default_next_heads(state)
    alpha = float('-inf')
    beta = float('inf')
    score, move = alphabeta(state, player, 0, alpha, beta, 0, max_depth + 1, player, next_heads)
    # state.log()
    print("score =", score)
    print("move =", decode(move))
    return move

def default_next_heads(state):
    next_heads = np.zeros((state.totalSnakes(), 2), dtype=np.int8)
    n_snakes = state.totalSnakes()
    for s in range(n_snakes):
        if not state.getDead(s):
            x, y = state.getHead(s)
            next_heads[s][0] = x
            next_heads[s][1] = y
    return next_heads
        

def check_for_head_on(state, player):
    opponent = get_opponent(state, player, player)
    available_moves = []
    opp_x, opp_y = state.getHead(opponent)
    # print(f"OPPONENT AT: {opp_x, opp_y}")
    if state.getLength(opponent) >= state.getLength(player):
        my_x, my_y = state.getHead(player)
        if abs(my_x - opp_x) + abs(my_y - opp_y) <= 2:
            for m in range(4):
                next_x = my_x + moves[m][0]
                next_y = my_y + moves[m][1]
                if state.inBounds(next_x, next_y) and state.isSafe(next_x, next_y, 1) and abs(next_x - opp_x) + abs(next_y - opp_y) > 1:
                    available_moves.append(m)
    return available_moves

def check_for_trap(state, player): # a simple bfs to ensure access to the board is not restricted
    next_heads = default_next_heads(state)
    opponent = get_opponent(state, player, player)
    my_x, my_y = state.getHead(player)
    available_moves = np.zeros(4)
    for m in range(4):
        next_x = my_x + moves[m][0]
        next_y = my_y + moves[m][1]

        if state.inBounds(next_x, next_y) and state.isSafe(next_x, next_y, 1):
            next_heads[player][0] = next_x
            next_heads[player][1] = next_y
            state = state.clone()
            state.do_game_tick(next_heads)
            available_moves[m] = total_space(state, player)
    
    next_heads[player][0] = my_x
    next_heads[player][1] = my_y
    return available_moves

def total_space(state, snake):
    count = 0
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
                    q.append(point)
                    count += 1
    return count



def score_board ( board_state, snake, player ):
    if snake == player:
        return mood.score_board( board_state, snake )
    # we don't know strategy of other snakes, but it's probably something like this
    if board_state.getDead(snake):
        return -1e8
    return 0

def closest_snake(state, snake):
    head = state.getHead(snake)
    snakes = state.data[SNAKES_IDX:]
    heads_only = 1 - np.abs(np.sign(snakes - 1))
    head_map = np.sum(heads_only, axis=0)

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
                if state.inBounds(point[0], point[1]) and point not in v:
                    if head_map[point[0], point[1]]:
                        closest = np.where(heads_only[:,point[0], point[1]])[0][0]
                        return closest
                    v.add(point)
    return depth


def get_opponent(state, snake, player):
    n_snakes = state.numAliveSnakes()
    if snake != player:
        return player
    if n_snakes == 2:
        for s in range(1, n_snakes):
            if not state.getDead((snake + s) % n_snakes):
                return (snake + s) % n_snakes
        return (snake + 1) % n_snakes
    else:
        # find closest snake
        return closest_snake(state, snake)
        


# next_heads is np array of shape (n_snakes, 2)
def alphabeta(state: BoardState, snake, move: int, alpha, beta, depth, max_depth, player, next_heads, indent=""):
    # if max_depth == 3 and depth <= 1 and time.time() * 1000 - start_time > 400:
    #     max_depth = 2

    next_opponent = get_opponent(state, snake, player)
    # print(F"{indent}SNAKE {snake}, depth = {depth}/{max_depth}")
    if snake == player:
        # print(f"{indent}this is us! incrementing depth")
        if depth > 0:
            # perform game tick before evaluation and recursive calls
            state = state.clone()
            state.do_game_tick(next_heads)
            # state.log(indent+"  ")

        depth += 1
        if depth >= max_depth:
            # print(f"{indent}reached max depth! scoring board as... ", end = "")
            score = score_board(state, snake, player)
            # print(score)
            return score, move
        elif state.getDead(snake):
            # print(f"{indent}we are DEAD here")
            return -1e8, move
        elif state.numAliveSnakes() == 1:
            # print(f"{indent}we are VICTORIOUS here")
            return 1e8, move

        x, y = state.getHead(snake)

        best_score = -1e8
        best_move = 0
        total_scores = []

        # iterate over possible moves
        for m in range(4):
            next_x = x + moves[m][0]
            next_y = y + moves[m][1]
            if state.inBounds(next_x, next_y) and state.isSafe(next_x, next_y, depth):
                # print(f"{indent}trying move {decode(m)} to ({next_x}, {next_y})")
                next_heads[snake][0] = next_x
                next_heads[snake][1] = next_y
                result_score, result_move = alphabeta(state, next_opponent, m, alpha, beta, depth, max_depth, player, next_heads, indent+"    ")
                total_scores.append(result_score)
                # print(f"{indent}move {decode(m)} will result in {result_score}")
                if result_score > best_score:
                    best_score = result_score
                    best_move = m
                alpha = max(alpha, best_score)
                if beta <= alpha:
                    # print(f"{indent}PRUNED! {beta} <= {alpha}")
                    break
        
        next_heads[snake][0] = x
        next_heads[snake][1] = y
        # print(f"{indent}choosing move {decode(best_move)}")
        return best_score, best_move

    else: # opponent snake (min node)
        if state.getDead(snake):
            # print(f"{indent} snake {snake} is dead, moving on...")
            return alphabeta(state, next_opponent, move, alpha, beta, depth, max_depth, player, next_heads, indent+"    ")
        x, y = state.getHead(snake)
        
        worst_score = 1e8
        worst_move = 0
        total_scores = []
        for m in range(4):
            next_x = x + moves[m][0]
            next_y = y + moves[m][1]
            if state.inBounds(next_x, next_y) and state.isSafe(next_x, next_y, depth):
                # print(f"{indent}trying move {decode(m)} to ({next_x}, {next_y})")
                next_heads[snake][0] = next_x
                next_heads[snake][1] = next_y
                result_score, result_move = alphabeta(state, next_opponent, m, alpha, beta, depth, max_depth, player, next_heads, indent+"    ")
                # print(f"{indent}move {decode(m)} will result in {result_score}")
                total_scores.append(result_score)
                if result_score < worst_score:
                    worst_score = result_score
                    worst_move = m
                
                beta = min(beta, worst_score)
                if beta <= alpha:
                    # print(f"{indent}PRUNED! {beta} <= {alpha}")
                    break
        
        next_heads[snake][0] = x
        next_heads[snake][1] = y
        # print(f"{indent} choosing move {decode(worst_move)}")
        return (sum(total_scores) + 5 * worst_score) / (5 + len(total_scores)), worst_move

    

        
