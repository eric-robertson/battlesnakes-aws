import json
import Converter, Encoded, Visualizer

file = open('./boards/a.json')
data = json.load( file )
file.close() 

# Encode
encoding = Converter.json_to_board( data )
Visualizer.visualize_encoded( encoding )
