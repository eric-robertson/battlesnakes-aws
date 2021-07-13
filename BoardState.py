# Board state object itself

import numpy as np

INFO_LAYER = 0
FOOD_LAYER = 1

HEALTH_IDX = 0
LENGTH_IDX = 1
DEAD_IDX = 2

MAX_HEALTH = 100

class BoardState:

    def __init__ (self, data ):
        self.data = data

    def clone ( self ):
        return BoardState( self.data.copy() )

    def isSnakeBody ( self, snake, x, y):
        return self.data[snake,x, y] > 1
    def inBounds ( self, x, y ):
        return (x >= 0 and y >= 0 and x < self.data.shape[1] and y < self.data.shape[2])
    def getHealth ( self, snake ):
        return self.data[INFO_LAYER, snake, HEALTH_IDX]
    def getLength ( self, snake ):
        return self.data[INFO_LAYER, snake, LENGTH_IDX]
    def getDead ( self, snake ):
        return self.data[INFO_LAYER, snake, DEAD_IDX]
    def getLayer ( self, snake ):
        return self.data[2 + snake]
    def getHeads ( self ):
        return np.where(self.data[2:] == 1)
    def getHead ( self, snake ):
        xs, ys = np.where(self.data[2 + snake] == 1)
        return xs[0], ys[0]
    def setDead ( self, snake ):
        self.data[INFO_LAYER, 2 + snake, DEAD_IDX] = 1
    def eatFood ( self, snake ):
        self.data[INFO_LAYER, 2 + snake, HEALTH_IDX] = MAX_HEALTH
        self.data[INFO_LAYER, 2 + snake, LENGTH_IDX] += 1
    
    def totalSnakes(self):
        return self.data.shape[0] - 2
    def numDeadSnakes(self):
        return np.sum(self.data[INFO_LAYER, :, DEAD_IDX])
    def numAliveSnakes(self):
        return self.totalSnakes() - self.numDeadSnakes()

    # returns whether or not a point will be safe in depth game turns
    def isSafe(self, x, y, depth):
        occupant = np.max(self.data[2:, x, y])
        if occupant == 0:
            return True
        snake = np.argmax(self.data[2:, x, y])
        length = self.getLength(snake)
        return occupant + depth > length


    def log ( self, indent="" ):
        print(f"{indent}Board:")
        for j in range(self.data.shape[2]-1,-1,-1):
            row = indent
            for i in range (self.data.shape[1]):
                if self.data[2,i,j] == 1:
                    row+="A"
                elif self.data[2,i,j] > 1:
                    row+= str(int(self.data[2,i,j]))
                elif self.data[3,i,j] == 1:
                    row+="B"
                elif self.data[3,i,j] > 1:
                    row+= str(int(self.data[3,i,j]))

                elif self.data[FOOD_LAYER,i,j] != 0:
                    row += "F"
                else:
                    row += "."
                row += " "

            print(row)
        print(f"{indent}Snake1: ", self.getHealth(0), 'dead' if self.getDead(0) else 'alive')
        print(f"{indent}Snake2: ", self.getHealth(1), 'dead' if self.getDead(1) else 'alive')
        print(f"{indent}---------------------")

    # Step forward given h1 & h2
    def do_game_tick ( self, heads ):

        # Increment each snake element
        snakes = self.data[2:]
        snakes[snakes != 0] += 1

        # Move snakes TODO: vectorize
        for s in range(snakes.shape[0]):
            self.move_snake( s, heads[s] )

        self.check_collide()

    # Move head
    def move_snake ( self, snake, head ):
        # Grab length and snake layer
        length = self.getLength( snake )
        layer = self.getLayer( snake )
        
        # Should we add another cell?
        if length != layer.max():
            layer[ layer == layer.max() ] = 0 # == 0?

        # Did we hit ourself?
        if layer[head[0], head[1]] != 0:
            self.setDead( snake )

        # Set our new head
        layer[head] = 1

    # Check snake-on-snake collision
    def check_collide ( self ):
        
        # We did collide, who hit who
        _, xs, ys = self.getHeads()

        snakes = self.data[2:]
        # Simple check here
        if np.any( np.product(snakes, axis=0) ):
            # pairwise comparisons
            for s1 in range(snakes.shape[0] - 1):
                for s2 in range(s1 + 1, snakes.shape[0]):
                    if self.isSnakeBody(s2, xs[s1], ys[s1]):
                        self.setDead(s1)
                    elif self.isSnakeBody(s1, xs[s2], ys[s2]):
                        self.setDead(s2)
                    else: # head-to-head collision, larger survives
                        h1 = self.getLength(s1)
                        h2 = self.getLength(s2)
                        if h1 >= h2:
                            self.setDead(s2)
                        if h2 <= h1:
                            self.setDead(s1)
            
        # Grab food
        for s in range(snakes.shape[0]):
            if not self.getDead( s ):
                if self.getLayer(FOOD_LAYER)[xs[s],ys[s]]:
                    self.data[FOOD_LAYER,xs[s],ys[s]] = 0
                    self.eatFood( s )