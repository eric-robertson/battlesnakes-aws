# Root of the tree search algorithm itself
# It acts at the clippers that trim and select branched as needed

import numpy as np
import heapq as hq
from Node import Node
import mood

jobs = []
job_id = 0

# Overall scoring
def judge ( board_state ):
    score_0 = score_board( board_state, 0)
    score_1 = score_board( board_state, 1)

    if score_0 < 0: return score_0
    if score_1 == np.inf: return -9999
    if score_1 < 0: return np.inf

    return score_0

# How good is this board for a given player
def score_board ( board_state, snake ):
    if snake == 0:
        return mood.score_board( board_state, snake )
    if snake == 1:
        if board_state.getDead(1):
            return -9999
        if board_state.getDead(0):
            return np.inf
        return 0

# Used to choose what branch to explore next
def register_branch(branch_node, label ):
    global job_id
    priority = branch_node.score_priority()
    job_id += 1
    hq.heappush(jobs, (priority,job_id, label, branch_node) )

def select_brach ():
    if len(jobs) == 0:
        return False, False

    next = jobs[0]
    hq.heappop( jobs )

    if ( next[3].get_score() < 0 ):
        return select_brach()

    #print("Selected Branch", next[2])
    #next[3].log()
    return True, next[3]

def clear_job_tree():
    global jobs
    jobs = []