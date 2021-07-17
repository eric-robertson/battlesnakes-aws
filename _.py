import json
import Converter, Encoded, Visualizer, Tree

file = open('./boards/a.json')
data = json.load( file )
file.close() 

# Encode
encoding = Converter.json_to_board( data )
Visualizer.visualize_encoded( encoding )

# Step forward
root = Tree.register_root(encoding)

# Do the movements!
Tree.compute_branches( Encoded.get_snakes(encoding) )
Tree.compute_branches( Encoded.get_snakes(encoding) )
Tree.compute_branches( Encoded.get_snakes(encoding) )
Tree.compute_branches( Encoded.get_snakes(encoding) )
Tree.compute_branches( Encoded.get_snakes(encoding) )
Tree.compute_branches( Encoded.get_snakes(encoding) )
Tree.compute_branches( Encoded.get_snakes(encoding) )

# Result?

print(root.report())
