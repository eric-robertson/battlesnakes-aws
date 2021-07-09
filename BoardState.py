# Board state object itself

import numpy as np

# TODO: change layer order so snakes are at higher layers
INFO_LAYER = 2 # 0
FOOD_LAYER = 3 # 1

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
        return (x >= 0 and y >= 0 and x < self.board.shape[1] and y < self.board.shape[2])
    def getHealth ( self, snake ):
        return self.data[INFO_LAYER, snake, HEALTH_IDX]
    def getLength ( self, snake ):
        return self.data[INFO_LAYER, snake, LENGTH_IDX]
    def getDead ( self, snake ):
        return self.data[INFO_LAYER, snake, DEAD_IDX]
    def getLayer ( self, snake ):
        return self.data[snake]
    def getHeads ( self ):
        return np.where(self.data[:2] == 1)
    def setDead ( self, snake ):
        self.data[INFO_LAYER, snake, DEAD_IDX] = 1
    def eatFood ( self, snake ):
        self.data[INFO_LAYER, snake, HEALTH_IDX] = MAX_HEALTH
        self.data[INFO_LAYER, snake, LENGTH_IDX] += 1

    def log ( self ):
        print("Board:")
        for j in range(self.board.shape[2]-1,-1,-1):
            row = ""
            for i in range (self.board.shape[1]):
                if self.data[0,i,j] == 1:
                    row+="A"
                elif self.data[0,i,j] > 1:
                    row+= str(int(self.data[1,i,j]))
                elif self.data[1,i,j] == 1:
                    row+="B"
                elif self.data[1,i,j] > 1:
                    row+= str(int(self.data[1,i,j]))

                elif self.data[FOOD_LAYER,i,j] != 0:
                    row += "F"
                else:
                    row += "."
                row += " "

            print(row)
        print("Snake1: ", self.getHealth(0), 'dead' if self.getDead(0) else 'alive')
        print("Snake2: ", self.getHealth(1), 'dead' if self.getDead(1) else 'alive')
        print("---------------------")

    # Step forward given h1 & h2
    def do_game_tick ( self, h1, h2 ):

        # Increment each snake element
        snakes = self.data[:2]
        snakes[snakes != 0] += 1

        # Move snakes
        self.move_snake( 0, h1 )
        self.move_snake( 1, h2 )

        self.check_collide()

    # Move head
    def move_snake ( self, snake, head ):

        # Grab length and snake layer
        length = self.getLength( snake )
        layer = self.getLayer( snake )
        
        # Should we add another cell?
        if length != layer.max():
            layer[ layer == layer.max() ] == 0

        # Did we hit ourself?
        if layer[head] != 0:
            self.setDead( snake )

        # Set our new head
        layer[head] = 1

    # Check snake-on-snake collision
    def check_collide ( self ):
        
        # We did collide, who hit who
        _, xs, ys = self.getHeads()

        # Simple check here
        if np.any( self.getLayer(0) * self.getLayer(1) ): 
        
            # Snake 0 just hit snake 1
            if self.isSnakeBody(1, xs[0],ys[0]):
                self.setDead( 0 )
            elif self.isSnakeBody(0, xs[1],ys[1]):
                self.setDead( 1 )
            else:
                h0 = self.getLength( 0 )
                h1 = self.getLength( 1 )
                if h0 >= h1: 
                    self.setDead(1)
                if h1 >= h0:
                    self.setDead(0)
            
        # Grab food
        for s in range(2):
            if not self.getDead( s ):
                if self.getLayer(FOOD_LAYER)[xs[s],ys[s]]:
                    self.data[FOOD_LAYER,xs[s],ys[s]] = 0
                    self.eatFood( s )