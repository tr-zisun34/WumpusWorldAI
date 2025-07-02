import random
import json

class Cell:
    def __init__(self):
        self.has_pit = False
        self.has_wumpus = False
        self.has_gold = False
        self.breeze = False
        self.stench = False
        self.glitter = False

class Environment:
    def __init__(self, size=10):
        self.size = size
        self.grid = [[Cell() for _ in range(size)] for _ in range(size)]

    def load_from_file(self, filename):
        with open(filename, 'r') as f:
            data = json.load(f)
        for item in data.get("pits", []):
            self.grid[item[0]][item[1]].has_pit = True
        for item in data.get("wumpus", []):
            self.grid[item[0]][item[1]].has_wumpus = True
        for item in data.get("gold", []):
            self.grid[item[0]][item[1]].has_gold = True
        self.update_percepts()

    def generate_random(self):
        for i in range(self.size):
            for j in range(self.size):
                if random.random() < 0.1:
                    self.grid[i][j].has_pit = True
                if random.random() < 0.05:
                    self.grid[i][j].has_gold = True
                if random.random() < 0.02:
                    self.grid[i][j].has_wumpus = True
        self.update_percepts()

    def update_percepts(self):
        for i in range(self.size):
            for j in range(self.size):
                cell = self.grid[i][j]
                cell.glitter = cell.has_gold
                cell.breeze = self.adjacent_has(i, j, "has_pit")
                cell.stench = self.adjacent_has(i, j, "has_wumpus")

    def adjacent_has(self, x, y, attr):
        for dx, dy in [(-1,0),(1,0),(0,-1),(0,1)]:
            nx, ny = x + dx, y + dy
            if 0 <= nx < self.size and 0 <= ny < self.size:
                if getattr(self.grid[nx][ny], attr):
                    return True
        return False

    def get_cell(self, x, y):
        return self.grid[x][y] if 0 <= x < self.size and 0 <= y < self.size else None
