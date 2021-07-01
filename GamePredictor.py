# Takes in a given game state and predicts all the next possible game states

import numpy as np
move_options = [ (-1,0,'L'), (0,-1,'U'), (1,0,'R'), (0,1,'D') ]

# Gets the next steps for a given current state
def get_next_states ( current_state ):

    # 2 extra layers, so this is total number of game snakes
    total_snakes = current_state.shape[0] - 2
    board_size = current_state.shape[1]

    # Game healths
    next_game_health = current_state[0].copy()
    next_game_health[:,0] -= 1
    
    # Calculate the possible moves for each snake
    # Makes sure each move does not collide with a wall or itself
    # Does not check on food & other snakes
    snake_move_options = compute_move_options( current_state, board_size, total_snakes )

    # Return results
    return next_game_health, current_state[-1], snake_move_options

# Computes all valid moves for every snake
# Does not check collisions or food or anything, just out of bounds and self-collisions
def compute_move_options ( board, size, snakes ):

    results = []

    for i in range(snakes):

        this_snake_options = []

        # Get the snake in question and its current head position
        this_snake_layer = board[i + 1]
        head_x, head_y = np.where( this_snake_layer == 1 )

        for dx, dy, label in move_options:
            
            # Generate new head
            _new_head_x = head_x[0] + dx
            _new_head_y = head_y[0] + dy

            # Then lets move the head!
            valid, _snake_with_move = try_assign_movement( board, i, (_new_head_x, _new_head_y), size)
            if valid: 
                this_snake_options.append( (_snake_with_move, label) )

        results.append( this_snake_options )

    return results

# Takes in a snake layer and does the given movement for it
# Returns false if its invalid
def try_assign_movement ( board, index, new_head, bounds):

    x,y = new_head
    snake_layer = board[index + 1]
    size_on_board = snake_layer.max()
    target_size = board[0,index,1]

    # Is head valid in bounds
    if x >= bounds or y >= bounds:
        return False, False
    if x < 0 or y < 0:
        return False, False

    # Where are you moving to
    target_square = snake_layer[x,y]

    # Is the snake about to hit itself?
    if target_square > 0:

        # In the case of a growing snake, you cant eat any of your body
        if size_on_board != target_size:
            return False, False

        # In the case of a non-growwing snake, you can eat your tail but nothing else
        elif target_square < size_on_board:
            return False, False

    # Move the snake

    layer = snake_layer.copy()
    layer[ layer != 0 ] += 1
    layer[ new_head ] = 1

    # if you are not set to grow, remove tail, unless you ate it
    if size_on_board == target_size and target_square != size_on_board:
        layer[ layer == layer.max() ] = 0

    return True, layer