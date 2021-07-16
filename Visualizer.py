import Encoded

def visualize_encoded ( encoding, score = -1 ): 

    size = Encoded.get_size( encoding )
    foods = Encoded.get_food( encoding )
    snakes = Encoded.get_snakes( encoding)

    snake_codes = ['A', 'B', 'C', 'D', 'E', 'F']

    print('----------------------')
    
    for j in range(size+1,-1, -1):
        row = []
        for i in range(size+1):
            tile = '·'
            if i == 0 or j == 0 or i == size + 1 or j == size + 1:
                tile = ' '
                row.append(tile)
                continue
            if foods[i,j]:
                tile = 'F'
                row.append(tile)
                continue
            for s in range(snakes):
                data = Encoded.get_snake( s, encoding )
                head = Encoded.get_head( s, encoding )
                if head == (i,j):
                    tile = snake_codes[s]
                elif data[i,j] != 0:
                    tile = str(data[i,j])
            row.append(tile)

        print(' '.join(row))

    if score != -1:
        print("SCORED: " + str(score))

    for s in range(snakes):
        health = Encoded.get_health( s, encoding )
        length = Encoded.get_realizedLength( s, encoding )
        dead = Encoded.get_snake( s, encoding )[0,0] != 0
        grow = Encoded.get_realizedLength(s, encoding) != Encoded.get_length(s,encoding)

        print(f"{snake_codes[s]}: {health} HP, {length} Len" + (", DEAD" if dead else ""), "+" if grow else "")

    print('----------------------')
