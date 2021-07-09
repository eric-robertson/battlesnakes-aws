import random
from typing import List, Dict
import numpy as np
from strategy import MinMax
from util import *

def avoid_neck(my_head: Dict[str, int], my_body: List[dict], possible_moves: List[str]) -> List[str]:
    my_neck = cvt_pt(my_body[1])  # The segment of body right after the head is the 'neck'
    if my_neck.x < my_head.x:  # my neck is left of my head
        possible_moves['left'] = -1
    elif my_neck.x > my_head.x:  # my neck is right of my head
        possible_moves['right'] = -1
    elif my_neck.y < my_head.y:  # my neck is below my head
        possible_moves['down'] = -1
    elif my_neck.y > my_head.y:  # my neck is above my head
        possible_moves['up'] = -1

    return possible_moves

def avoid_walls(height: int, width: int, head, possible_moves):
    if head.x >= width:
        possible_moves['right'] = -1
    if head.x <= 1:
        possible_moves['left'] = -1
    if head.y >= height:
        possible_moves['up'] = -1
    if head.y <= 1:
        possible_moves['down'] = -1
    return possible_moves

def avoid_snakes(possible_moves: dict, board) -> dict:
    for move, pos in possible_moves.items():
        if pos != -1 and board[pos.x][pos.y] > 1:
            possible_moves[move] = -1
    return possible_moves

def avoid_head_on(possible_moves, data, my_head):
    n = len(remaining_moves(possible_moves))
    if n > 1:
        for move, pos in possible_moves.items():
            if pos != -1:
                for snake in data['board']['snakes']:
                    s_head = cvt_pt(snake['head'])
                    if len(snake['body']) > len(data['you']['body']) and mh_dist(s_head, pos) == 1:
                        possible_moves[move] = -1
                        n -= 1
                        if n <= 1:
                            break
    return possible_moves

def choose_move(data: dict) -> str:
    """
    example of 'data' https://docs.battlesnake.com/references/api/sample-move-request
    """
    my_head = cvt_pt(data["you"]["head"])
    my_body = data["you"]["body"]

    possible_moves = {
      "up"    : my_head.move("up"),
      "down"  : my_head.move("down"),
      "left"  : my_head.move("left"),
      "right" : my_head.move("right")
    }

    # avoid neck
    possible_moves = avoid_neck(my_head, my_body, possible_moves)

    # avoid walls
    board_height = data['board']['height']
    board_width = data['board']['height']
    possible_moves = avoid_walls(board_height, board_width, my_head, possible_moves)
    
    # matrix representation of the board
    board = np.zeros((board_height + 2, board_width + 2)) # zero indicates open space
    i = len(my_body)
    for d in my_body:
        point = cvt_pt(d)
        board[point.x][point.y] = i
        i -= 1
    for snake in data['board']['snakes']:
        i = len(snake['body'])
        for d in snake['body']:
            point = cvt_pt(d)
            board[point.x][point.y] = i
            i -= 1
    
    for f in data['board']['food']:
        point = cvt_pt(f)
        board[point.x][point.y] = -1 # -1 indicated food
   
    # avoid other snakes yes
    possible_moves = avoid_snakes(possible_moves, board)
    # try to avoid head-on collisions if possible
    possible_moves = avoid_head_on(possible_moves, data, my_head)
    # choose random move from remaining options if there are any
    rem = remaining_moves(possible_moves)
    move = "left"
    if len(rem) > 0:
        move = random.choice(rem)
    

    print(f"CHOOSING MOVE: {move} from all valid options in {rem}")
    
    return move

def use_tree_search(data):
    # state, my_idx = cvt_state(data)
    # strategy = MinMax(1)
    # move = strategy.decide_move(state, my_idx)
    move = ""
    if move == "":
        return choose_move(data)
    else:
        print(f"CHOOSING MOVE: {move}")

    return move
    
