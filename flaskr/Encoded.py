import copy


def get_head ( snake, encoded ):
    return encoded[ 1, snake, 0], encoded[ 1, snake, 1]
def get_length ( snake, encoded ):
    return encoded[ 1, snake, 2]
def get_realizedLength ( snake, encoded ):
    return encoded[ 1, snake, 3]
def get_health ( snake, encoded ):
    return encoded[ 1, snake, 4]
def get_food ( encoded ):
    return encoded[ 0 ]
def get_snake ( snake, encoded ):
    return encoded[ 2 + snake ]
def get_snakes ( encoded ):
    return encoded.shape[0] - 2
def get_size ( encoded ):
    return encoded.shape[1] - 2 

    
def to_bytes ( encoded ):
    return encoded.tobytes()


def clone ( encoded ):
    return encoded.copy()