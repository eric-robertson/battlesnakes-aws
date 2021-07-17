from Visualizer import visualize_encoded
import numpy as np
import VectorEngine, Visualizer
import Node
import time

# Caching
skiptree_lookups = {}

# The tree itself!
branches = [None,None,[],[],[]]
parents = [None,None,[],[],[]]

base_snakes = 0

def register_root ( board_state ):
    global base_snakes
    global branches
    global parents
    
    branches = [None,None,[],[],[]]
    parents = [None,None,[],[],[]]
    
    base_snakes = board_state.shape[0] - 2
    root = Node.Node( None, board_state, 1, base_snakes )

    branches[base_snakes].append(board_state)
    parents[base_snakes].append(root)

    return root

def register_branch ( node, move_id, board_state, score, snakes ):

    new_node = Node.Node( node, board_state, score, snakes )
    node.register_child( move_id, new_node )

def insert_branch ( snakes, state, node ):
    if snakes < 2: return
    branches[snakes].append( state )
    parents[snakes].append( node )

def compute_branches ( snakes, items = 100 ):
    
    global parents
    
    items = min(items, len(parents[snakes]))
    if items == 0: return

    parent_nodes = parents[snakes][:items]
    states = np.stack( branches[snakes][:items] )

    branches[snakes] = branches[snakes][items:]

    # Batching baby!
    start = time.time()
    futures = VectorEngine.step_snakes( states )
    scores = VectorEngine.score_boards( futures, base_snakes )
    t1 = time.time()

    # future ids
    future_counts = 4 ** snakes

    # Itterate through them all
    for i in range(items):

        parent = parent_nodes[i]

        for m in range(future_counts):

            # Grab resultant board, compute snake count, file in correct bucket for next batch
            result_board = futures[m,i,:,:,:] 
            where_alive = 1 * (result_board[ :, 0, 0 ] == 0)
            where_alive[0] = 1
            where_alive[1] = 1
            _where_index = np.argwhere(where_alive != 0 )
            result_board = result_board[_where_index[:,0]]
            snakes_left = sum(where_alive) - 2 

            # Do the filing
            register_branch( parent, m, result_board, scores[m,i], snakes_left)
        
        parent.recompute()


    
    parents[snakes] = parents[snakes][items:]
    t2 = time.time()

    print(f"Expanded {items} boards into {future_counts*items} total states each in {round((t1-start),5)}s and inserted into tree in {round((t2-t1),5)}s ")
