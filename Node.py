import numpy as np

class Node:

    def __init__( self, parent, boardstate, base_score, snakes ):
        self.base_score = base_score
        self.transient_score = base_score
        self.boardstate = boardstate
        self.futures = [None] * ( 4 ** snakes )
        self.parent = parent
        self.snakes = snakes

    def register_child ( self, id, node ):
        self.futures[id] = node

    def recompute ( self ) :
        segment = (4 ** (self.snakes - 1))
        scores = []
        for i in range(4):
            worst = np.inf
            for j in range(segment):
                index = (i * segment) + j
                s = self.futures[index].transient_score
                if s < worst:
                    worst = s
            scores.append(worst)
        if ( self.transient_score != max(scores)):
            self.transient_score = max(scores)
            if ( self.parent != None ):
                self.parent.recompute()
        

