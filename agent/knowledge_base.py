class KnowledgeBase:
    def __init__(self):
        self.safe_cells = set()
        self.unsafe_cells = set()
        self.visited_cells = set()
        self.percepts = {}  # {(x, y): [percepts]}

    def add_percept(self, x, y, percepts):
        self.percepts[(x, y)] = percepts
        self.visited_cells.add((x, y))

    def mark_safe(self, x, y):
        self.safe_cells.add((x, y))

    def mark_unsafe(self, x, y):
        self.unsafe_cells.add((x, y))

    def is_safe(self, x, y):
        return (x, y) in self.safe_cells

    def is_visited(self, x, y):
        return (x, y) in self.visited_cells

    def get_unvisited_safe_neighbors(self, x, y):
        neighbors = [(x+1,y),(x-1,y),(x,y+1),(x,y-1)]
        return [(nx, ny) for (nx, ny) in neighbors
                if 0 <= nx < 10 and 0 <= ny < 10
                and (nx, ny) not in self.visited_cells
                and (nx, ny) not in self.unsafe_cells]
