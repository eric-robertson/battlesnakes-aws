import random
from typing import List, Dict
import numpy as np

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
        if pos != -1 and board[pos[0]][pos[1]] > 0:
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
    board = np.zeros((board_height, board_width)) # zero indicates open space
    i = len(my_body)
    for d in my_body[:-1]:
        board[d['x']][d['y']] = i
        i -= 1
    for snake in data['board']['snakes']:
        i = len(snake['body'])
        for d in snake['body'][:-1]:
            board[d['x']][d['y']] = i
            i -= 1
   
    # avoid other snakes yes
    possible_moves = avoid_snakes(possible_moves, board)

    # try to avoid head-on collisions if possible
    possible_moves = avoid_head_on(possible_moves, data, my_head)

    # TODO: try to avoid closing itself off
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