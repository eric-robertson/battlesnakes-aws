from util import GameState
from math import tanh
from copy import deepcopy

class MinMax:
    max_depth = 5

    def __init__(self, max_depth: int):
        self.max_depth = max_depth

    def decide_move(self, state: GameState, snake_idx: int) -> str:
        a = float('-inf')
        b = float('inf')
        score, move = self.tree_search(state, snake_idx, "up", a, b, 0, self.max_depth, True)

        if score < 0:
            return ""
        
        next_state = deepcopy(state).make_move(move, snake_idx)
        next_state.cleanup()
        if not next_state.get_snake(snake_idx).alive:
            return ""
        
        return move
    
    def evaluate(self, state: GameState, snake_idx: int) -> float:
        score = 0
        snake = state.get_snake(snake_idx)

        if not snake.alive:
            return float('-inf')
        
        head = snake.get_head()
        
        num_alive = state.num_alive()
        if num_alive == 1:
            return float('inf')
        
        free_squares, owned_food_depth = state.voronoi(snake_idx)
        if free_squares == 0:
            return float('-inf')

        score += 1e5 / num_alive
        score += 10 * free_squares
        score += 0.8 / len(snake)

        food_paths = state.find_food(head)

        if len(food_paths) > 0:
            food_length = owned_food_depth
            if food_length == -1 and len(food_paths) > 0:
                food_length = food_paths[0].length
            
            if snake.health < food_length:
                return float('-inf')
            
            breathing_room = snake.health - food_length
            score += 100 * tanh(0.15 * breathing_room)

        return score

    def tree_search(self, state: GameState, snake_idx: int, move: str, a: float, b: float, depth: int, max_depth: int, max_player: bool):
        print("depth =", depth)
        snake = state.get_snake(snake_idx)
        # delta = 
        if depth == self.max_depth or not snake.alive:
            return (self.evaluate(state, snake_idx), move)
        
        opponent_idx = state.get_opponent(snake_idx)
        opponent = state.get_snake(opponent_idx)

        if max_player:
            print("max player")
            best_score = float('-inf')
            best_move = ''

            for move in snake.get_moves():
                print("moving", move)
                # make a copy of the game state
                next_state = deepcopy(state)
                next_state.make_move(move, snake_idx)

                result = self.tree_search(next_state, snake_idx, move, a, b, depth + 1, max_depth, not max_player)
                print("result =", result)
                if result[0] > best_score:
                    best_score = result[0]
                    best_move = move
                    
                a = max(a, best_score)
                if b <= a:
                    break
            
            return (best_score, best_move)
        else:
            worst_score = float('inf')
            worst_move = ''

            for move in opponent.get_moves():
                next_state = deepcopy(state)
                if opponent_idx != snake_idx:
                    next_state.make_move(move, opponent_idx)
                    next_state.cleanup()
                
                result = self.tree_search(next_state, snake_idx, move, a, b, depth + 1, max_depth, not max_player)
                if result[0] < worst_score:
                    worst_score = result[0]
                    worst_move = move
                b = min(b, worst_score)
                if b <= a:
                    break
            return (worst_score, worst_move)