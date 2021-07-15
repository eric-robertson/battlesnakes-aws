```python
import json
import numpy as np
import Converter, Encoded, Visualizer
```


```python
# Load board
file = open('./boards/f.json')
data = json.load( file )
file.close() 
```


```python
# Encode
encoding = Converter.json_to_board( data )
```


```python
Visualizer.visualize_encoded( encoding )
```

    ----------------------
                           
      · · · · · · · · · · ·
      · · · · · · · · · · ·
      · · · · · · · · · · ·
      · · · · · · · · · · ·
      · · · · · · · · · · ·
      · · 1 A F B 1 · · · ·
      · · · · · · · · · · ·
      · · · · · · · · · · ·
      · · · · · · · · · · ·
      · · · · · · · · · · ·
      · · · · · · · · · · ·
                           
    A: 100 HP, 2 Len
    B: 100 HP, 2 Len
    ----------------------



```python
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
```


```python
def step_snakes ( to_compute ):
    
    # TODO for board step
    
    # Input size of (n, s+2, w+2, w+2)
    # Number of boards, snakes + 2, width + 2, width + 2 
    
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
    _[ _ != 0 ] -= 1
    
    # Snake health decrement
    # BOARD CHANGE -> snake health decrement
    to_compute[:,1,:snake_count,4] -= 1
    
    # Workspace to build snake from in 4 directions
    workspace = np.stack([to_compute] * futures).copy()
    
    # Change head markers
    # BOARD CHANGE -> update every snakes head position in metadata layer
    workspace[:,:,1,:snake_count,:2] = new_heads
    
    # Grab snake lenghts
    lengths = workspace[:,:,1,:snake_count,3]
    
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

    print(gained_food)
    
    
    # New Workspace done!
    # OUTPUT OF SHAPE:
    # (4^s, n, s+2, w+2, w+2)
    return workspace
```


```python
results = step_snakes( np.stack([encoding] ).copy() )
results.shape
```

    [False  True False False False  True False  True False False  True False
     False False False False False False  True False False False False False
     False False  True False False False False False]





    (16, 1, 4, 13, 13)




```python
for i in range(results.shape[0]):
    Visualizer.visualize_encoded( results[i,0] )
```

    ----------------------
                           
      · · · · · · · · · · ·
      · · · · · · · · · · ·
      · · · · · · · · · · ·
      · · · · · · · · · · ·
      · · · · · · · · · · ·
      · · A 1 B 1 · · · · ·
      · · · · · · · · · · ·
      · · · · · · · · · · ·
      · · · · · · · · · · ·
      · · · · · · · · · · ·
      · · · · · · · · · · ·
                           
    A: 99 HP, 2 Len
    B: 100 HP, 3 Len
    ----------------------
    ----------------------
                           
      · · · · · · · · · · ·
      · · · · · · · · · · ·
      · · · · · · · · · · ·
      · · · · · · · · · · ·
      · · · · · · · · · · ·
      · · · 1 F 1 · · · · ·
      · · · · · · · · · · ·
      · · · · · · · · · · ·
      · · · · · · · · · · ·
      · · · · · · · · · · ·
      · · · · · · · · · · ·
                           
    A: 99 HP, 2 Len, DEAD
    B: 99 HP, 2 Len, DEAD
    ----------------------
    ----------------------
                           
      · · · · · · · · · · ·
      · · · · · · · · · · ·
      · · · · · · · · · · ·
      · · · · · · · · · · ·
      · · · · · · · · · · ·
      · · · 1 B 1 · · · · ·
      · · · A · · · · · · ·
      · · · · · · · · · · ·
      · · · · · · · · · · ·
      · · · · · · · · · · ·
      · · · · · · · · · · ·
                           
    A: 99 HP, 2 Len
    B: 100 HP, 3 Len
    ----------------------
    ----------------------
                           
      · · · · · · · · · · ·
      · · · · · · · · · · ·
      · · · · · · · · · · ·
      · · · · · · · · · · ·
      · · · A · · · · · · ·
      · · · 1 B 1 · · · · ·
      · · · · · · · · · · ·
      · · · · · · · · · · ·
      · · · · · · · · · · ·
      · · · · · · · · · · ·
      · · · · · · · · · · ·
                           
    A: 99 HP, 2 Len
    B: 100 HP, 3 Len
    ----------------------
    ----------------------
                           
      · · · · · · · · · · ·
      · · · · · · · · · · ·
      · · · · · · · · · · ·
      · · · · · · · · · · ·
      · · · · · · · · · · ·
      · · A 1 F 1 B · · · ·
      · · · · · · · · · · ·
      · · · · · · · · · · ·
      · · · · · · · · · · ·
      · · · · · · · · · · ·
      · · · · · · · · · · ·
                           
    A: 99 HP, 2 Len
    B: 99 HP, 2 Len
    ----------------------
    ----------------------
                           
      · · · · · · · · · · ·
      · · · · · · · · · · ·
      · · · · · · · · · · ·
      · · · · · · · · · · ·
      · · · · · · · · · · ·
      · · · 1 A 1 B · · · ·
      · · · · · · · · · · ·
      · · · · · · · · · · ·
      · · · · · · · · · · ·
      · · · · · · · · · · ·
      · · · · · · · · · · ·
                           
    A: 100 HP, 3 Len
    B: 99 HP, 2 Len
    ----------------------
    ----------------------
                           
      · · · · · · · · · · ·
      · · · · · · · · · · ·
      · · · · · · · · · · ·
      · · · · · · · · · · ·
      · · · · · · · · · · ·
      · · · 1 F 1 B · · · ·
      · · · A · · · · · · ·
      · · · · · · · · · · ·
      · · · · · · · · · · ·
      · · · · · · · · · · ·
      · · · · · · · · · · ·
                           
    A: 99 HP, 2 Len
    B: 99 HP, 2 Len
    ----------------------
    ----------------------
                           
      · · · · · · · · · · ·
      · · · · · · · · · · ·
      · · · · · · · · · · ·
      · · · · · · · · · · ·
      · · · A · · · · · · ·
      · · · 1 F 1 B · · · ·
      · · · · · · · · · · ·
      · · · · · · · · · · ·
      · · · · · · · · · · ·
      · · · · · · · · · · ·
      · · · · · · · · · · ·
                           
    A: 99 HP, 2 Len
    B: 99 HP, 2 Len
    ----------------------
    ----------------------
                           
      · · · · · · · · · · ·
      · · · · · · · · · · ·
      · · · · · · · · · · ·
      · · · · · · · · · · ·
      · · · · · · · · · · ·
      · · A 1 F 1 · · · · ·
      · · · · · B · · · · ·
      · · · · · · · · · · ·
      · · · · · · · · · · ·
      · · · · · · · · · · ·
      · · · · · · · · · · ·
                           
    A: 99 HP, 2 Len
    B: 99 HP, 2 Len
    ----------------------
    ----------------------
                           
      · · · · · · · · · · ·
      · · · · · · · · · · ·
      · · · · · · · · · · ·
      · · · · · · · · · · ·
      · · · · · · · · · · ·
      · · · 1 A 1 · · · · ·
      · · · · · B · · · · ·
      · · · · · · · · · · ·
      · · · · · · · · · · ·
      · · · · · · · · · · ·
      · · · · · · · · · · ·
                           
    A: 100 HP, 3 Len
    B: 99 HP, 2 Len
    ----------------------
    ----------------------
                           
      · · · · · · · · · · ·
      · · · · · · · · · · ·
      · · · · · · · · · · ·
      · · · · · · · · · · ·
      · · · · · · · · · · ·
      · · · 1 F 1 · · · · ·
      · · · A · B · · · · ·
      · · · · · · · · · · ·
      · · · · · · · · · · ·
      · · · · · · · · · · ·
      · · · · · · · · · · ·
                           
    A: 99 HP, 2 Len
    B: 99 HP, 2 Len
    ----------------------
    ----------------------
                           
      · · · · · · · · · · ·
      · · · · · · · · · · ·
      · · · · · · · · · · ·
      · · · · · · · · · · ·
      · · · A · · · · · · ·
      · · · 1 F 1 · · · · ·
      · · · · · B · · · · ·
      · · · · · · · · · · ·
      · · · · · · · · · · ·
      · · · · · · · · · · ·
      · · · · · · · · · · ·
                           
    A: 99 HP, 2 Len
    B: 99 HP, 2 Len
    ----------------------
    ----------------------
                           
      · · · · · · · · · · ·
      · · · · · · · · · · ·
      · · · · · · · · · · ·
      · · · · · · · · · · ·
      · · · · · B · · · · ·
      · · A 1 F 1 · · · · ·
      · · · · · · · · · · ·
      · · · · · · · · · · ·
      · · · · · · · · · · ·
      · · · · · · · · · · ·
      · · · · · · · · · · ·
                           
    A: 99 HP, 2 Len
    B: 99 HP, 2 Len
    ----------------------
    ----------------------
                           
      · · · · · · · · · · ·
      · · · · · · · · · · ·
      · · · · · · · · · · ·
      · · · · · · · · · · ·
      · · · · · B · · · · ·
      · · · 1 A 1 · · · · ·
      · · · · · · · · · · ·
      · · · · · · · · · · ·
      · · · · · · · · · · ·
      · · · · · · · · · · ·
      · · · · · · · · · · ·
                           
    A: 100 HP, 3 Len
    B: 99 HP, 2 Len
    ----------------------
    ----------------------
                           
      · · · · · · · · · · ·
      · · · · · · · · · · ·
      · · · · · · · · · · ·
      · · · · · · · · · · ·
      · · · · · B · · · · ·
      · · · 1 F 1 · · · · ·
      · · · A · · · · · · ·
      · · · · · · · · · · ·
      · · · · · · · · · · ·
      · · · · · · · · · · ·
      · · · · · · · · · · ·
                           
    A: 99 HP, 2 Len
    B: 99 HP, 2 Len
    ----------------------
    ----------------------
                           
      · · · · · · · · · · ·
      · · · · · · · · · · ·
      · · · · · · · · · · ·
      · · · · · · · · · · ·
      · · · A · B · · · · ·
      · · · 1 F 1 · · · · ·
      · · · · · · · · · · ·
      · · · · · · · · · · ·
      · · · · · · · · · · ·
      · · · · · · · · · · ·
      · · · · · · · · · · ·
                           
    A: 99 HP, 2 Len
    B: 99 HP, 2 Len
    ----------------------



```python

```


```python

```
