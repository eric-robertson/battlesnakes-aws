import numpy as np
import Encoded
import MoveHead

lookups = {}

# Takes an array of board states and generates all the resulting future nodes
def project_futures ( board_states ):

    board_count = board_states.shape(0)
    results = np.empty( board_count, dtype=object)
    computed = np.zeros( board_count )

    for i,board in enumerate( board_states ):
        encoded = Encoded.to_bytes( board )

        if encoded in lookups:
            results[i] = lookups[encoded]
        else:
            computed[i] = 1

    to_compute = board_states[computed]
    compute_results = _compute_board_states( to_compute )

    
# Takes in a board stata array and computes all future board states from them
def _compute_board_states ( to_compute ) :

    # Input size of (n, s+2, w+2, w+2)
    # Output of shape (4*n, s+2, w+2, w+2)

    game_count = to_compute.shape[0]
    snake_count = to_compute.shape[1] - 2

    # Grab all heads in format ( n, s, (x,y) )
    heads = to_compute[:,1,:snake_count,:2]

    # 4 principal directions, so we get 4 boards
    workspace = np.stack( [ to_compute ] * 4 )

    # Compute the 4 possible movements

    



def get_possibleFutures ( snake, board ):

    snake_array = Encoded.get_snake( snake, board )
    bytes = snake_array.tobytes()
    
    if bytes in lookups: return lookups[bytes]

    results = do_snakeMovements( snake, board )
    
    lookups[bytes] = results
    return results


def do_snakeMovements ( snakes, board ):

    snake_array = Encoded.get_snake( snake, board )
    head = Encoded.get_head( snake, board )
    heads = Encoded.get_moves( head )
    length = Encoded.get_realizedLength( snake, board )

    results = []

    for i,j in enumerate(heads):
        working_array[ working_array != 0 ] -= 1

    working_array = np.stack([ snake_array ] * len(heads) )


    for i,h in enumerate( heads ): 
        working_array[i + 2, h[0], h[1] ] = length
    


    snakes = len(snakes)
    combined = np.empty((snakes, size+1, size ))

    for i,s in enumerate(snakes):
        (data,head,length,health) = s
        combined[i,0:size,:] = data

