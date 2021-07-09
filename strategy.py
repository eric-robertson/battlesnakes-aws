
class MinMax:
    max_depth = 5

    def __init__(self, m_depth):
        self.max_depth = m_depth
    
    def evaluate(state, snake):
        if state.snakes[snake]