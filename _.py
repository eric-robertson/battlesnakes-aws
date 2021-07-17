import json, time
import Converter, Encoded, Visualizer, Tree

file = open('./boards/h.json')
data = json.load( file )
file.close() 

# Encode
encoding = Converter.json_to_board( data )
Visualizer.visualize_encoded( encoding )

# Step forward
root = Tree.register_root(encoding)

start = time.time() * 1000

# Start tree search
while True:

    Tree.compute_branches( 2 )
    
    now = time.time() * 1000
    if ( now - start > 300 ): break

# Result?

move,score,_ = root.report()
move_name = ['left', 'right', 'up', 'down'][move]
print(move_name, score)
