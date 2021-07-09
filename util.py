import numpy as np
import random

FOOD = -1
WALL = -2
EMPTY = 0

MOVES = ['up', 'down', 'left', 'right']

# manhattan distance
def mh_dist(p1, p2):
    return abs(p1.x - p2.x) + abs(p1.y - p2.y)

def remaining_moves(possible_moves):
    rem = []
    for move, pos in possible_moves.items():
        if pos != -1:
            rem.append(move)
    return rem

class Point:
    x = 0
    y = 0
    def __init__(self, x, y):
        self.x = x
        self.y = y
    
    def move(self, dir: str):
        if dir == 'up':
            return Point(self.x, self.y + 1)
        if dir == 'down':
            return Point(self.x, self.y - 1)
        if dir == 'left':
            return Point(self.x - 1, self.y)
        if dir == 'right':
            return Point(self.x + 1, self.y)

class Cell:
    occupants = set()
    t = None

    def __init__(self):
        self.t = EMPTY
    
    def occupy(self, idx:int):
        self.occupants.add(idx)
    
    def vacate(self, idx:int):
        self.occupants.remove(idx)
    
    def vacate_all(self):
        self.occupants = set()
    
    def num_occupants(self) -> int:
        return len(self.occupants)
    
    def is_occupant(self, idx:int) -> bool:
        return idx in self.occupants
    
    def set_food(self):
        self.t = FOOD


class Board:

    board = None
    w = 0
    h = 0

    def __init__(self, w, h):
        self.w = w
        self.h = h
        self.board = [[Cell() for i in range(h + 2)] for i in range(w + 2)]
        self.clear()
        # self.board = np.zeros((w + 2, h + 2))
        # self.snakes = np.zeros_like(self.board) - 1
        # self.clear()

    def clear(self):
        for i in range(len(self.board)):
            for j in range(len(self.board[i])):
                if i == 0 or j == 0 or i == len(self.board) - 1 or j == len(self.board[i]) - 1:
                    self.board[i][j].t = WALL
                else:
                    self.board[i][j].t = EMPTY
                self.board[i][j].vacate_all()

    def print(self):
        print()
        for y in reversed(range(self.h + 2)):
            for x in range(self.w + 2):
                cell = self.board[x][y]
                if cell.t == EMPTY and cell.num_occupants() == 0:
                    print(".", end=" ")
                elif cell.t == WALL:
                    print("X", end=" ")
                elif cell.t == FOOD:
                    print("f", end=" ")
                else:
                    s_idx = list(cell.occupants)[0]
                    print(s_idx, end=" ")
            print()
        print()
        

    def sample_empty(self):
        x = random.choice(range(self.w)) + 1
        y = random.choice(range(self.h)) + 1
        while self.get_type(Point(x, y)) != EMPTY:
            x = random.choice(range(self.w)) + 1
            y = random.choice(range(self.h)) + 1
        return Point(x, y)
        # i = random.choice(np.where(self.board == EMPTY)[0])
        # return Point(i // self.w, i % self.w)
    
    def occupy(self, point:Point, idx:int):
        self.board[point.x][point.y].occupy(idx)
    
    def vacate(self, point:Point, idx:int):
        self.board[point.x][point.y].t = EMPTY
    
    def num_occupants(self, point:Point) -> int:
        return self.board[point.x][point.y].num_occupants()
    
    def get_type(self, point:Point) -> int:
        return self.board[point.x][point.y].t

    def set_type(self, point:Point, new_t:int):
        self.board[point.x][point.y].t = new_t

    def get_occupants(self, point:Point):
        return self.board[point.x][point.y].occupants
    
    def is_occupant_of(self, point:Point, snake_idx:int) -> bool:
        return self.board[point.x][point.y].is_occupant(snake_idx)

    def put_food(self, point:Point):
        self.board[point.x][point.y].t = FOOD

    def in_board(self, point:Point):
        return point.y >= 0 and point.x >= 0 and \
        point.y < self.h + 1 and point.x < self.w + 2
    
    def is_safe(self, point:Point):
        c = self.board[point.x][point.y].t
        return c == FOOD or c == EMPTY
    
    # def will_be_safe(self, point:Point, dist:int):
    #     c = self.board[point.x][point.y]
    #     return c != WALL and c <= dist

    def neighbors(self, p: Point):
        result = []
        for dir in MOVES:
            n = p.move(dir)
            if self.in_board(n):
                result.append(n)
        return result
    
    # CAN BE IMPROVED WITH (1) A STAR (2) SNEK TAIL CONTRACTION (keep track of distance, use will_be_safe)
    def find_food(self, start: Point):
        paths = []
        q = []
        visited = set()
        parent = dict()
        visited.insert(start)
        q.append(start)
        while len(q) > 0:
            current = q.pop(0)
            for point in self.neighbors(current):
                if self.in_board(point) and self.is_safe(point) and point not in visited:
                    parent[point] = current
                    visited.add(point)
                    if self.get_type(point) == FOOD:
                        path = []
                        while start != point:
                            path.append(point)
                            point = parent[point]
                        path.append(start)
                        paths.append(path)
                    q.append(point)
        return paths

    def flood(self, start: Point) -> int:
        q = []
        q.append(start)
        visited = set(q)
        while len(q) > 0:
            current = q.pop(0)
            for point in self.neighbors(current):
                if self.in_board(point) and self.is_safe(point) and point not in visited:
                    visited.add(point)
                    q.append(point)
        return len(visited)

# --------------------------------------------------------------------------------------------
# --------------------------------------------------------------------------------------------
# --------------------------------------------------------------------------------------------

class Snake:
    alive = True
    health = 100
    score = 0
    free_moves = 2
    id = ""
    points = []

    def __init__(self, health, turn, free_moves = 2, id = ""):
        self.health = health
        self.alive = True
        self.score = 0
        self.points = []
        self.free_moves = free_moves
        self.id = id

    def get_head(self) -> Point :
        return self.points[0]
    
    def lose_health(self) -> int :
        self.health -= 1
        return self.health

    def make_move(self, dir: str) -> Point :
        head = self.get_head()
        new_head = head.move(dir)
        self.points.insert(0, new_head)
        self.score += 1
        return new_head

    def pop_tail(self) -> Point :
        return self.points.pop(-1)
    
    def __len__(self) -> int :
        return len(self.points)
    
    def clear(self):
        self.points = []
    
    def use_free_move(self):
        self.free_moves -= 1
    
    def get_remaining_time_in(self, point: Point): # can be optimized slightly
        for i in range(len(self)):
            if self.points[i] == point:
                return len(self) - i
        return 0

    def get_moves(self): # moves which do not go into the neck
        moves = []
        head = self.get_head()
        for dir in MOVES:
            p = head.move(dir)
            if len(self) > 1:
                if self.points[1] != p:
                    moves.append(dir)
            else:
                moves.append(dir)
        return moves
        
    def add_point(self, p:Point):
        self.points.append(p)
    
    def in_snake(self, p:Point) -> bool:
        return p in self.points

# -----------------------------------------------------------------------
# -----------------------------------------------------------------------
# -----------------------------------------------------------------------

class GameState:
    max_food = 0
    current_food = 0
    timer = 0
    snakes = []
    board = None

    def __init__(self, w: int, h: int, max_food = 0):
        self.board = Board(w, h)
        self.timer = 0
        self.max_food = max_food
        for i in range(max_food):
            self.addFood()
        
    def add_snake(self) -> int:
        start = self.board.sample_empty()
        return self.add_snake(start)

    def addFood(self):
        p = self.board.sample_empty()
        self.board.put_food(p)
        self.current_food += 1
    
    def addFood(self, p:Point):
        self.board.put_food(p)
        self.current_food += 1

    def add_snake(self, start:Point):
        snake = Snake(start)
        snake_idx = len(self.snakes)
        self.board.occupy(start, snake_idx)
        self.snakes.append(snake)
        return snake_idx
    
    def add_snake(self, snake:Snake):
        snake_idx = len(self.snakes)
        self.snakes.append(snake)
        for p in snake.points:
            self.board.occupy(p, snake_idx)
        return snake_idx
    
    def get_snake(self, snake_idx:int) -> Snake:
        return self.snakes[snake_idx]
    
    def make_move(self, dir:str, snake_idx:int):
        snake = self.snakes[snake_idx]
        head = snake.make_move(dir)
        snake.lose_health()
        if self.board.is_occupant_of(head, snake_idx): # self collision
            self.snakes[snake_idx].alive = False
        
        self.board.occupy(head, snake_idx)
        c = self.board.get_type(head)

        if c == FOOD:
            self.snakes[snake_idx].health = 100
        elif c == WALL:
            tail = snake.pop_tail()
            self.board.vacate(tail, snake_idx)
        elif c == EMPTY:
            if snake.free_moves == 0:
                tail = snake.pop_tail()
                self.board.vacate(tail, snake_idx)
            else:
                snake.use_free_move()

    def check_collision(self, point: Point):
        if self.board.num_occupants(point) > 1:
            occupants = self.board.get_occupants(point)
            heads = []
            head_lengths = []
            
            for snake_idx in occupants:
                current_snake = self.snakes[snake_idx]
                head = current_snake.get_head()
                if point == head:
                    heads.append(snake_idx)
                    head_lengths.append(len(current_snake))
            
            if len(heads) == self.board.num_occupants(point) and len(heads) > 1:
                max_len = max(head_lengths)
                count_max = head_lengths.count(max_len)
                if count_max > 1:
                    max_len = -1

                for snake_idx in heads:
                    current_snake = self.snakes[snake_idx]
                    if len(current_snake) != max_len:
                        current_snake.alive = False
            else:
                for snake_idx in heads:
                    self.snakes[snake_idx].alive = False

    def remove_food(self, point: Point):
        if self.board.get_type(point) == FOOD:
            self.board.set_type(point, EMPTY)
            self.current_food -= 1

    def cleanup(self):
        for snake in self.snakes:
            if snake.health <= 0:
                snake.alive = False
            if snake.alive:
                current_point = snake.get_head()
                self.check_collision(current_point)
                self.remove_food(current_point)
        
        for snake_idx in range(len(self.snakes)):
            snake = self.snakes[snake_idx]
            if not snake.alive:
                for point in snake.points:
                    self.board.vacate(point, snake_idx)
                snake.clear()
        
        while self.current_food < self.max_food:
            self.add_food()
        
        # assert self.is_valid()

        self.timer += 1
            
    def is_valid(self) -> bool:
        if self.current_food != self.max_food:
            print("current food != max food")
            return False
        return self.is_given_valid()

    def is_given_valid(self) -> bool:
        if not self.board.is_valid():
            print("board is invalid")
            return False
        for snake_idx in range(len(self.snakes)):
            snake = self.snakes[snake_idx]
            for point in snake.points:
                if snake.alive and not self.board.is_occupant(point, snake_idx):
                    print("snake alive but not occupying point")
                    return False
        return True
    
    def get_height(self) -> int:
        return self.board.h
    
    def get_width(self) -> int:
        return self.board.w

    def print_scoreboard(self):
        for i in range(len(self.snakes)):
            snake = self.snakes[i]
            head = snake.get_head()
            print(f"{i} {snake.health} {snake.alive} {head.x},{head.y}")

    def will_be_safe(self, point:Point, dist:int) -> bool:
        if self.board.num_occupants(point) == 0:
            return True
        occupant = list(self.board.get_occupants(point))[0]
        return self.snakes[occupant].get_remaining_time_in(point) <= dist

    def is_safe(self, point:Point, dist:int) -> bool:
        return self.board.get_type(point) != WALL and self.will_be_safe(point, dist)
    
    def find_food(self, start:Point):
        depth = 0
        paths = []
        q = []
        visited = set()
        parent = dict()

        visited.add(start)
        q.append(start)
        q.append(Point(-1,-1))

        while len(q) > 0:
            current = q.pop(0)
            if current.x == -1 and current.y == -1:
                depth += 1
                q.append(Point(-1,-1))
                if q[0].x == -1 and q[0].y == -1:
                    break
            else:
                for point in self.board.neighbors(current):
                    if self.board.in_board(point) and self.is_safe(point, depth) and point not in visited:
                        parent[point] = current
                        visited.add(point)
                        if self.board.get_type(point) == FOOD:
                            path = []
                            while start != point:
                                path.append(point)
                                point = parent[point]
                            path.append(start)
                            paths.append(path)
                        q.append(point)
        return paths

    def flood(self, start:Point):
        depth = 0
        q = [start, Point(-1,-1)]
        visited = set()
        visited.add(start)

        while len(q) > 0:
            current = q.pop(0)
            if current.x == -1 and current.y == -1:
                depth += 1
                q.append(Point(-1, -1))
                if q[0].x == -1 and q[0].y == -1:
                    break
            else:
                for point in self.board.neighbors(current):
                    if self.board.in_board(point) and self.is_safe(point, depth) and point not in visited:
                        visited.add(point)
                        q.append(point)
        return len(visited)

    def get_opponent(self, idx: int) -> int:
        depth = 0
        snake = self.get_snake(idx)
        start = snake.get_head()
        q = [start, Point(-1,-1)]
        visited = set()
        visited.add(start)

        while len(q) > 0:
            current = q.pop(0)
            if current.x == -1 and current.y == -1:
                depth += 1
                q.append(Point(-1, -1))
                if q[0].x == -1 and q[0].y == -1:
                    break
            else:
                for point in self.board.neighbors(current):
                    if self.board.in_board(point):
                        if self.board.num_occupants(current) > 0:
                            occupant = list(self.board.get_occupants(current))[0]
                            if occupant != idx:
                                return occupant
                        if self.is_safe(point, depth) and point not in visited:
                            visited.add(point)
                            q.append(point)
        return idx

    def voronoi(self, snake_idx: int) -> tuple:
        depth = 0
        food_depth = -1
        pair_depth_mark = (Point(-1,-1), -1)
        mark = -1
        q = []
        v = dict()
        counts = [0 for i in range(len(self.snakes))]

        for i in range(len(self.snakes)):
            snake = self.snakes[i]
            if snake.alive:
                head = snake.get_head()
                p = (head, i)
                q.append(p)
                v[head] = i
        q.append(pair_depth_mark)

        while len(q) > 0:
            p = q.pop(0)
            if p == pair_depth_mark:
                depth += 1
                q.append(pair_depth_mark)
                if q[0] == pair_depth_mark:
                    break
            else:
                current = p[0]
                idx = p[1]

                for point in self.board.neighbors(current):
                    if point in v:
                        other = v[point]
                        if other != mark and other != idx:
                            counts[other] -= 1
                            v[point] = mark
                    elif self.board.in_board(point) and self.is_safe(point, depth):
                        if self.board.get_type(point) == FOOD and idx == snake_idx and food_depth == -1:
                            food_depth = depth
                        counts[idx] += 1
                        v[point] = idx
                        q.append((point, idx))
        return counts[snake_idx], food_depth

    def num_alive(self) -> int:
        count = 0
        for snake in self.snakes:
            if snake.alive:
                count += 1
        return count

def cvt_pt(dict_pt):
    return Point(dict_pt['x'] + 1, dict_pt['y'] + 1)
    
def cvt_snake(snake_data: dict, turn: int):

    free_moves = max(0, 2 - turn)
    health = snake_data["health"]
    snake_id = snake_data["id"]
    snake = Snake(health, turn, free_moves, snake_id)
    snake.points = []
    for point in snake_data['body']:
        snake.add_point(cvt_pt(point))
    
    return snake

def cvt_state(data: dict):
    height = data['board']['height']
    width = data['board']['height']
    state = GameState(width, height)
    state.snakes = []

    turn = data['turn']
    for food in data['board']['food']:
        state.addFood(cvt_pt(food))
    my_id = data['you']['id']
    my_idx = -1
    for snake_data in data['board']['snakes']:
        snake = cvt_snake(snake_data, turn)
        snake_idx = state.add_snake(snake)
        print("Added snake_idx ", snake_idx)
        if snake.id == my_id:
            my_idx = snake_idx
    
    assert my_idx != -1
    
    return state, my_idx
