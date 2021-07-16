# Root of the tree search algorithm itself
# It acts at the clippers that trim and select branched as needed
from . import mood

import numpy as np
import heapq as hq

jobs = []
job_id = 0

def decode ( i ):
    return (['left', 'right', 'up', 'down'])[i]

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

def select_brach():
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


class Node:
    def __init__(self, score, board, previous, label ):
        self.transient_score = score
        self.objective_score = score
        self.board = board
        self.previous = previous
        self.children = {}

        if not( score < 0 or score == np.inf ) :
            register_branch( self, label )

    def log (self):
        self.board.log()

    def score_priority ( self ):
        return 1

    def register_childen( self, branches ):
        # Create children branch nodes
        for (move0,move1) in branches:
            board,score = branches[move0, move1]
            self.register_child( move0, move1, Node( score, board, self, str(move0)+'+'+str(move1)))
            
        #print("Updating children of board...")

        # Recursively compute new child values
        self.recompute()

    def register_child ( self, move0, move1, node ):
        if not move0 in self.children: self.children[move0] = {}
        self.children[move0][move1] = node

    def get_score( self ):
        return self.transient_score

    def recompute ( self ):

        score_options = []

        if len(self.children) == 0:
            return -9999

        if logging: print("Of your moves:")
        for your_move in self.children:
            if logging: print(decode(your_move), ':')
            sub_scores = [ np.inf ]
            for their_move in self.children[your_move]:
                if logging: print('then', decode(their_move), ':', self.children[your_move][their_move].get_score())
                sub_scores.append( self.children[your_move][their_move].get_score() )
            score_options.append( min(sub_scores) )

        self.transient_score = max( score_options ) + 1

        if logging: print('Reset to: ', self.transient_score )

        if self.previous != False:
            self.previous.recompute()

    def get_prediction (self):

        best = (-9999, 0)

        for your_move in self.children:

            sub_scores = []
            for their_move in self.children[your_move]:
                sub_scores.append( self.children[your_move][their_move].get_score() )

            score = min(sub_scores)
            if score > best[0]:
                best = (score, your_move )
                
        return best

        