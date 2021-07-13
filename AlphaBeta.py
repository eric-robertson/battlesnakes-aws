# alpha-beta pruning search
from BoardState import BoardState
import numpy as np
import mood
from Oracle import decode

moves = [(-1,0,0), (1,0,1), (0,1,2), (0,-1,3)]

def decide_move(state, player, max_depth):
    next_heads = np.zeros((state.totalSnakes(), 2), dtype=np.int8)
    alpha = float('-inf')
    beta = float('inf')
    score, move = alphabeta(state, player, 0, alpha, beta, 0, max_depth + 1, player, next_heads)
    state.log()
    print("score =", score)
    return move

def score_board ( board_state, snake, player ):
    if snake == player:
        return mood.score_board( board_state, snake )
    # we don't know strategy of other snakes, but it's probably something like this
    if board_state.getDead(snake):
        return float('-inf')
    return 0

# next_heads is np array of shape (n_snakes, 2)
def alphabeta(state: BoardState, snake, move: int, alpha, beta, depth, max_depth, player, next_heads, indent=""):
    x, y = state.getHead(snake)
    next_opponent = (snake + 1) % state.totalSnakes()

    if snake == player:
        print(F"{indent}SNAKE {snake}")
        print(f"{indent}this is us! incrementing depth")
        if depth > 0:
            # perform game tick before evaluation and recursive calls
            state = state.clone()
            state.do_game_tick(next_heads)
            state.log(indent+"  ")
        
        depth += 1
        if depth == max_depth:
            print(f"{indent}reached max depth! scoring board as... ", end = "")
            score = score_board(state, snake, player)
            print(score)
            return score, move
        elif state.getDead(snake):
            print(f"{indent}we are DEAD here")
            return float('-inf'), move
        elif state.numAliveSnakes() == 1:
            print(f"{indent}we are VICTORIOUS here")
            return float('inf'), move

        best_score = float('-inf')
        best_move = 0

        # iterate over possible moves
        for m in range(4):
            next_x = x + moves[m][0]
            next_y = y + moves[m][1]
            print(f"{indent}trying move {decode(m)} to ({next_x}, {next_y})")
            if state.inBounds(next_x, next_y) and state.isSafe(next_x, next_y, depth):
                # print(f"{indent}trying move {decode(m)}")
                next_heads[snake][0] = next_x
                next_heads[snake][1] = next_y
                result_score, result_move = alphabeta(state, next_opponent, m, alpha, beta, depth, max_depth, player, next_heads, indent+"    ")
                print(f"{indent}move {decode(m)} has the best score of {result_score}")
                if result_score > best_score:
                    best_score = result_score
                    best_move = m
                
                alpha = max(alpha, best_score)
                if beta <= alpha:
                    print(f"{indent}PRUNED! {beta} <= {alpha}")
                    break
        
        next_heads[snake][0] = x
        next_heads[snake][1] = y
        print(f"{indent}best score here is {best_score} if I move {decode(best_move)}")
        return best_score, best_move

    else: # opponent snake (min node)
        print(F"{indent}SNAKE {snake}")
        if state.getDead(snake):
            print(f"{indent} snake {snake} is dead, moving on...")
            return alphabeta(state, next_opponent, move, alpha, beta, depth, max_depth, player, next_heads)
        
        worst_score = float('inf')
        worst_move = 0
        
        for m in range(4):
            next_x = x + moves[m][0]
            next_y = y + moves[m][1]
            print(f"{indent}trying move {decode(m)} to ({next_x}, {next_y})")
            if state.inBounds(next_x, next_y) and state.isSafe(next_x, next_y, depth):
                next_heads[snake][0] = next_x
                next_heads[snake][1] = next_y
                result_score, result_move = alphabeta(state, next_opponent, m, alpha, beta, depth, max_depth, player, next_heads, indent+"    ")
                print(f"{indent}move {decode(m)} has the best score of {result_score}")

                if result_score < worst_score:
                    worst_score = result_score
                    worst_move = m
                
                beta = min(beta, worst_score)
                if beta <= alpha:
                    print(f"{indent}PRUNED! {beta} <= {alpha}")
                    break
        
        next_heads[snake][0] = x
        next_heads[snake][1] = y
        print(f"{indent}worst score here is {worst_score} if snake {snake} moves {decode(worst_move)}")
        return worst_score, worst_move

    

        
