from .knowledge_base import KnowledgeBase
from .interface import infer_from_percepts

class Agent:
    def __init__(self, world):
        self.world = world
        self.kb = KnowledgeBase()
        self.x = 0
        self.y = 9
        self.arrow_used = False

    def perceive(self):
        cell = self.world.get_cell(self.x, self.y)
        percepts = []
        if cell.content == 'P':
            percepts.append('Breeze')
        if cell.content == 'W':
            percepts.append('Stench')
        if cell.content == 'G':
            percepts.append('Glitter')
        return percepts

    def step(self):
        # Perceive and update KB
        percepts = self.perceive()
        self.kb.add_percept(self.x, self.y, percepts)
        infer_from_percepts(self.kb, self.x, self.y, percepts)

        # Goal found
        if 'Glitter' in percepts:
            print(f"Gold found at ({self.x},{self.y})!")
            return False  # Stop moving

        # Try moving to an unvisited safe neighbor
        safe_moves = self.kb.get_unvisited_safe_neighbors(self.x, self.y)
        if safe_moves:
            nx, ny = safe_moves[0]
            self.x, self.y = nx, ny
        else:
            print("No known safe moves left. Stopping.")
            return False

        return True
