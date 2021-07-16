import json
import Converter, Encoded, Visualizer, Tree

file = open('./boards/f.json')
data = json.load( file )
file.close() 

# Encode
encoding = Converter.json_to_board( data )
Visualizer.visualize_encoded( encoding )

# Step forward
root = Tree.register_root(encoding)

Tree.compute_branches( 2 )
Tree.compute_branches( 2 )
Tree.compute_branches( 2 )
Tree.compute_branches( 2 )
Tree.compute_branches( 2 )
#Tree.compute_branches( 2 )