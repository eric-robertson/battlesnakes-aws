# Board state object itself

import numpy as np

class BoardState:

    def __init__ (self, data ):
        self.data = data

    def clone ( self ):
        return BoardState( self.data.copy() )

    def isSnakeBody ( self, snake, x, y):
        return self.data[snake,x, y] > 1
    def inBounds ( self, x, y ):
        return (x >=0 and y >= 0 and x < 11 and y < 11)
    def getHealth ( self, snake ):
        return self.data[2,snake,0]
    def getLength ( self, snake ):
        return self.data[2,snake,1]
    def getDead ( self, snake ):
        return self.data[2,snake,2]
    def getLayer ( self, snake ):
        return self.data[snake]
    def getHeads ( self ):
        return np.where(self.data[:2] == 1)
    def setDead ( self, snake ):
        self.data[2,snake,2] = 1
    def eatFood ( self, snake ):
        self.data[2,snake,0] = 100
        self.data[2,snake,1] += 1

    def log ( self ):
        print("Board:")
        for j in range(10,-1,-1):
            row = ""
            for i in range (11):
                if self.data[0,i,j] == 1:
                    row+="A"
                elif self.data[0,i,j] > 1:
                    row+= str(int(self.data[1,i,j]))
                elif self.data[1,i,j] == 1:
                    row+="B"
                elif self.data[1,i,j] > 1:
                    row+= str(int(self.data[1,i,j]))

                elif self.data[3,i,j] != 0:
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
                if self.getLayer(3)[xs[s],ys[s]]:
                    self.data[3,xs[s],ys[s]] = 0
                    self.eatFood( s )