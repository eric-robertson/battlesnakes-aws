import numpy as np
from . import Tree, Visualizer

class Node:

    def __init__( self, parent, boardstate, base_score, snakes ):
        self.base_score = base_score
        self.transient_score = base_score
        self.result = 0
        self.boardstate = boardstate
        self.futures = [None] * ( 4 ** snakes )
        self.parent = parent
        self.snakes = snakes

    def register_child ( self, id, node ):
        self.futures[id] = node

    # Computes the score for a given node after its children have been filled in
    def recompute ( self, rec = False) :

        future_size = (4 ** (self.snakes - 1))
        branch_scores = []
        best_move = 0
        best_move_id = 0

        # Check each move
        for m in range(4):

            worst = np.inf
            winning = 0

            for f in range(future_size):
                index = m + (f*4)
                s = self.futures[index]
                if ( s == None ): continue
                
                if s.transient_score < worst:
                    worst = s.transient_score
                if s.transient_score == np.inf:
                    winning += 1

            branch_scores.append((worst, winning))

            # If the worst result from this move is better than any other
            # Set it to be the next best move
            if worst > best_move:
                best_move = worst
                best_move_id = m

        # Register best resultant move
        self.result = best_move_id

        # Now, did we update are score? Should we recurse?
        if ( self.transient_score != best_move):
            self.transient_score = best_move
            if ( self.parent != None ):
                self.parent.recompute( rec=True )

        # Finally, what branches should we add to the stack?
        if not rec:
            for m in range(4):

                # If this was the best move or the opponent is not in the clear, expand
                if m == best_move_id or branch_scores[m][1] > 1:
                    for f in range(future_size):
                        index = m + (f*4)
                        s = self.futures[index]
                        if ( s == None ): continue
                        Tree.insert_branch( s.snakes, s.boardstate, s)

    def report ( self ):
        return self.result, self.transient_score, self.base_score
