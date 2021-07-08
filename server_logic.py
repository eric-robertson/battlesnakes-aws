import random
from typing import List, Dict
import numpy as np

"""
This file can be a nice home for your move logic, and to write helper functions.

We have started this for you, with a function to help remove the 'neck' direction
from the list of possible moves!
"""


def avoid_neck(my_head: Dict[str, int], my_body: List[dict], possible_moves: List[str]) -> List[str]:
    my_neck = cvt_pt(my_body[1])  # The segment of body right after the head is the 'neck'
    if my_neck[0] < my_head[0]:  # my neck is left of my head
        possible_moves['left'] = -1
    elif my_neck[0] > my_head[0]:  # my neck is right of my head
        possible_moves['right'] = -1
    elif my_neck[1] < my_head[1]:  # my neck is below my head
        possible_moves['down'] = -1
    elif my_neck[1] > my_head[1]:  # my neck is above my head
        possible_moves['up'] = -1

    return possible_moves

def avoid_walls(height: int, width: int, head, possible_moves):
    if head[0] == width - 1:
        possible_moves['right'] = -1
    if head[0] == 0:
        possible_moves['left'] = -1
    if head[1] == height - 1:
        possible_moves['up'] = -1
    if head[1] == 0:
        possible_moves['down'] = -1
    return possible_moves

def avoid_snakes(possible_moves: dict, board) -> dict:
    # don't let your Battlesnake pick a move that would hit its own body
    for move, pos in possible_moves.items():
        if pos != -1 and board[pos[0]][pos[1]] < 0:
            possible_moves[move] = -1
    return possible_moves

def avoid_head_on(possible_moves, data, my_head):
    n = len(remaining_moves(possible_moves))
    if n > 1:
        for move, pos in possible_moves.items():
            if pos != -1:
                for snake in data['board']['snakes']:
                    s_head = cvt_pt(snake['head'])
                    if mh_dist(s_head, my_head) != 0 and mh_dist(s_head, pos) == 1:
                        possible_moves[move] = -1
                        n -= 1
                        if n <= 1:
                            break
    return possible_moves

def choose_move(data: dict) -> str:
    """
    data: Dictionary of all Game Board data as received from the Battlesnake Engine.
    For a full example of 'data', see https://docs.battlesnake.com/references/api/sample-move-request

    return: A String, the single move to make. One of "up", "down", "left" or "right".

    Use the information in 'data' to decide your next move. The 'data' variable can be interacted
    with as a Python Dictionary, and contains all of the information about the Battlesnake board 
    for each move of the game.

    """
    my_head = cvt_pt(data["you"]["head"])
    my_body = data["you"]["body"]

    possible_moves = {
      "up"    : next_pos(my_head, "up"),
      "down"  : next_pos(my_head, "down"),
      "left"  : next_pos(my_head, "left"),
      "right" : next_pos(my_head, "right")
    }

    # avoid neck
    possible_moves = avoid_neck(my_head, my_body, possible_moves)

    # avoid walls
    board_height = data['board']['height']
    board_width = data['board']['height']
    possible_moves = avoid_walls(board_height, board_width, my_head, possible_moves)
    
    # matrix representation of the board
    # TODO: edges of each square representation. This way the direction of the snakes are represented
    board = np.zeros((board_height, board_width)) # zero indicates open space
    for d in my_body[:-1]: # exclude the very end (tail), this will move out of the way the next turn
        board[d['x']][d['y']] = -1 # -1 indicates snake body
    for snake in data['board']['snakes']:
        for d in snake['body'][:-1]:
            board[d['x']][d['y']] = -1 # -1 indicates snake body
   
    # avoid other snakes yes
    possible_moves = avoid_snakes(possible_moves, board)

    # try to avoid head-on collisions if possible
    possible_moves = avoid_head_on(possible_moves, data, my_head)

    
    # Choose a random direction from the remaining possible_moves to move in, and then return that move
    rem = remaining_moves(possible_moves)
    move = "left"
    if len(rem) > 0:
        move = random.choice(rem)

    print(f"CHOOSING MOVE: {move} from all valid options in {rem}")
    
    return move


def next_pos(pos, move):
    if move == 'up':
        return [pos[0], pos[1] + 1]
    elif move == 'down':
        return [pos[0], pos[1] - 1]
    elif move == 'left':
        return [pos[0] - 1, pos[1]]
    elif move == 'right':
        return [pos[0] + 1, pos[1]]
    else:
        print(f"ERROR: {move} is invalid move" )
        return -1

# manhattan distance
def mh_dist(p1, p2):
    return abs(p1[0] - p2[0]) + abs(p1[1] - p2[1])

def cvt_pt(dict_pt):
    return [dict_pt['x'], dict_pt['y']]

def remaining_moves(possible_moves):
    rem = []
    for move, pos in possible_moves.items():
        if pos != -1:
            rem.append(move)
    return rem