import numpy as np

def compute_head_offsets ( snakes ):    
    
    futures = 4 ** snakes
    offset = np.zeros((futures, snakes, 2 )).astype('int8')
    
    # Compute direction options
    move = []
    for i in range(futures):
        snake_dirs = []
        for s in range(snakes):
            buckets = 4 ** (s+1) 
            index = i % buckets
            value = index // (buckets//4)
            snake_dirs.append(value)
        move.append( snake_dirs )
    move = np.array( move )
    
    # Compute deltas
    dx = np.zeros(move.shape)
    dy = np.zeros( move.shape )
    
    dx[move==0] = -1
    dx[move==1] = 1
    dy[move==2] = -1
    dy[move==3] = 1

    # Set offsets
    offset[:,:,0] = dx
    offset[:,:,1] = dy

    return offset

'''
Takes in an array of game states to step forward into possible future states

Given n game-states, each containig s snakes, and a board-size of w:

Accepts inputs of shape:
(n, s+2, w+2, w+2)

And returns future predictions in the shape:
(4^s, n, s+2, w+2, w+2)


There are 4^s possible future positions for s snakes moving in the 4 cardinal directions.
Each board will come with the following changes

- Snake's bodies will move forward in a cardinal direction
- Snake's head position will be updated to reflect motion
- Snakes will loose 1 health
- Snakes will be marked as dead if they:
    - Hit a wall
    - Hit themselves
    - Hit another snake
    - Loose a head-to-head
    - TODO: need to also be able to starve
- Snakes will gain 1 lenght + 100 Health when they consume food
- Food is removed on eating
- ALSO allow snakes to grow longer after eating

'''
def step_snakes ( to_compute ):

    # Stats to consider
    board_size = to_compute.shape[3]
    snake_count = to_compute.shape[1] - 2
    board_count = to_compute.shape[0]
    futures = 4 ** ( snake_count )
    size = (futures * board_count * snake_count )
    
    # Construct head offsets
    heads = to_compute[:,1,:snake_count,:2]
    new_heads = np.stack([heads] * futures).copy()
    offset = compute_head_offsets( snake_count)
    
    # Insert those offsets to move heads
    new_heads = np.moveaxis(new_heads, 1, 0 )
    new_heads[:] += offset
    new_heads = np.moveaxis(new_heads, 0, 1 )
    
    # Snake position decrement
    # BOARD CHANGE -> decrement all spaces by 1
    _ = to_compute[:,2:,:,:]
    _should_grow = to_compute[:,1,:snake_count,2] != to_compute[:,1,:snake_count,3]

    _ = np.moveaxis(_,0,-1)
    _ = np.moveaxis(_,0,-1)
    
    # BOARD CHANGE -> Update length
    to_compute[:,1,:snake_count,3] += _should_grow * 1
    _[ np.logical_and(_ != 0, np.logical_not(_should_grow)) ] -= 1
    
    _ = np.moveaxis(_,-1,0)
    _ = np.moveaxis(_,-1,0)
    to_compute[:,2:,:,:] = _
    
    # Snake health decrement
    # BOARD CHANGE -> snake health decrement
    to_compute[:,1,:snake_count,4] -= 1
    
    # Workspace to build snake from in 4 directions
    workspace = np.stack([to_compute] * futures).copy()
    
    # Change head markers
    # BOARD CHANGE -> update every snakes head position in metadata layer
    workspace[:,:,1,:snake_count,:2] = new_heads
    
    # Grab snake lenghts
    lengths = workspace[:,:,1,:snake_count,2]
    
    # Shape board and head for indexing
    _new_heads = np.reshape(new_heads, (size,2))
    _ws = np.reshape(workspace[:,:,2:], (size,13,13))

    # Check where snake collides with itself
    self_hits = _ws[np.arange(size), _new_heads[:,0], _new_heads[:,1]] != 0
    wall_hits = np.logical_or(_new_heads == 0, (_new_heads == board_size -1))
    wall_hits = np.logical_or(wall_hits[:,0], wall_hits[:,1])
    
    dead_snakes = np.logical_or(self_hits, wall_hits)
    
    # BOARD CHANGE -> Mark self-colisions at 0,0 as dead snakes!
    # BOARD CHANGE -> Mark wall-colisions at 0,0 as dead snakes!
    _new_heads[ dead_snakes, : ] = 0

    # BOARD CHANGE -> Insert new head location on the board, overwriting whatever was there
    _ws[np.arange(size), _new_heads[:,0], _new_heads[:,1]] = lengths.flatten()
    
    # Save back board
    workspace[:,:,2:] = np.reshape(_ws, (futures, board_count,snake_count,board_size,board_size))

    # Get board-space
    _ws = np.reshape(workspace, (futures * board_count, snake_count+2, 13,13) )
    _ws_layers = np.reshape(workspace[:,:,2:], (futures * board_count * snake_count, 13,13) )
    
    i = np.arange(board_count*futures*snake_count) // snake_count
    s = np.arange(board_count*futures*snake_count) % snake_count
    
    food_slice = _ws[ i, 0, _new_heads[:,0], _new_heads[:,1] ]
    snake_slices = _ws[ i, 2:, _new_heads[:,0], _new_heads[:,1] ]

    # Compute what snakes are fighting over a given square!
    top_snakes = np.argsort(-snake_slices, axis=1)
    not_top_snake = s != top_snakes[:,0]
    
    top_weight = snake_slices[np.arange(size),top_snakes[:,0]]
    seccond_weight = snake_slices[np.arange(size),top_snakes[:,1]]
    tied_for_top = top_weight == seccond_weight
    
    # What snakes are dieing to collisions
    died_to_collision = np.logical_or(not_top_snake, tied_for_top)
    
    # BOARD CHANGE -> KILL snakes that died to collisions
    _ws_layers[died_to_collision,0,0] = 1
    workspace[:,:,2:] = np.reshape(_ws_layers, (futures, board_count,snake_count,board_size,board_size))
    
    # Who got the food?
    gained_food = np.logical_and( food_slice, np.logical_not(died_to_collision) )
    snake_got_food = s[gained_food]
    _ws[ i[gained_food], 1, s[gained_food], 2] += 1
    _ws[ i[gained_food], 1, s[gained_food], 4] = 100
    
    food_slice[gained_food] = 0
    _ws[ i, 0, _new_heads[:,0], _new_heads[:,1] ] = food_slice
    
    workspace[:,:,1] = np.reshape(_ws[:,1], (futures, board_count,board_size,board_size))
    workspace[:,:,0] = np.reshape(_ws[:,0], (futures, board_count,board_size,board_size))
    
    # New Workspace done!
    # OUTPUT OF SHAPE:
    # (4^s, n, s+2, w+2, w+2)
    return workspace
'''

Scores the given snakes
Assumes you are always snake#0

Accepts inputs of shape:
(f, n, s+2, w+2, w+2)

And returns score in the form
(n)

'''

def score_boards ( futures, base_snakes ):

    # Game stats
    s = futures.shape
    f = futures.shape[0]
    board_size = futures.shape[3]
    
    futures = np.reshape(futures, (f*s[1],s[2],s[3],s[4]))
    
    # Gets your own stats
    
    _your_alive = futures[:,2,0,0] == 0
    _your_health = futures[:,1,0,4]
    _your_length = futures[:,1,0,3]
    _max_length = futures[:,1,:,3].max(axis=1)
    _your_head = futures[:,1,0,:2]
    _dead_count = base_snakes - (1*(futures[:,2:,0,0] == 0)).sum(axis = 1)
    _all_dead = np.all(futures[:,3:,0,0] != 0, axis = 1)
    
    score = np.zeros((f * s[1]), dtype='f')
    score += futures[:,1,0,2] * 20
    score += _your_health 
    
    score += _dead_count * 1000
    
    not_on_edge = (_your_head[:,0] > 2) * (_your_head[:,1] > 2) * (_your_head[:,1] < board_size - 3 ) * (_your_head[:,0] < board_size - 3 )
    score += not_on_edge * 100
    
    supremacy = (_your_length - _max_length) > 0
    score += supremacy * 100
    
    multiplier = _your_alive * (_your_health != 0)
    final = multiplier * score 

    final[_all_dead] = np.inf
    final[multiplier==0] = 0
    
    return np.reshape(final, (f, s[1]))
    