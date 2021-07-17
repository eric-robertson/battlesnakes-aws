import json
import Converter, Encoded, Visualizer, Tree

file = open('./boards/g.json')
data = json.load( file )
file.close() 

# Encode
encoding = Converter.json_to_board( data )
Visualizer.visualize_encoded( encoding )

# Step forward
root = Tree.register_root(encoding)

# Do the movements!
Tree.compute_branches( Encoded.get_snakes(encoding) )

# Result?

move,score,_ = root.report()
move_name = ['left', 'right', 'up', 'down'][move]
print(move_name, score)
