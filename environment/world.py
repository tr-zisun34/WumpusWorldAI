from .cell import Cell
from utils.parser import load_world

class World:
    def __init__(self, file_path):
        raw_grid = load_world(file_path)
        self.grid = [[Cell(x, y, raw_grid[y][x]) for x in range(10)] for y in range(10)]

    def get_cell(self, x, y):
        if 0 <= x < 10 and 0 <= y < 10:
            return self.grid[y][x]
        return None
