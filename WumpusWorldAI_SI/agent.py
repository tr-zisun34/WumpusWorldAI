from knowledge_base import KnowledgeBase
class Agent:
    def __init__(self, env, start=(0, 0)):
        self.env = env
        self.x, self.y = start
        self.start = start
        self.visited = set()
        self.safe = set([start])
        self.knowledge = {}
        self.path = [start]
        self.gold_collected = False
        self.arrow_used = False
        self.wumpus_possible = set()
        self.pit_possible = set()
        self.wumpus_killed = False
        self.kb = KnowledgeBase()

    def perceive(self):
        cell = self.env.get_cell(self.x, self.y)
        percepts = {
            "breeze": cell.breeze,
            "stench": cell.stench,
            "glitter": cell.glitter
        }

        self.knowledge[(self.x, self.y)] = percepts  # Already existing
        self.kb.tell((self.x, self.y), percepts)      # <--- ADD THIS LINE

        return percepts


    def infer_safe_neighbors(self):
        current_percepts = self.knowledge.get((self.x, self.y), {})
        neighbors = self.get_neighbors(self.x, self.y)
        for nx, ny in neighbors:
            if (nx, ny) in self.visited or (nx, ny) in self.safe:
                continue
            if not current_percepts.get("breeze", False) and not current_percepts.get("stench", False):
                self.safe.add((nx, ny))
            else:
                if current_percepts.get("breeze", False):
                    self.pit_possible.add((nx, ny))
                if current_percepts.get("stench", False):
                    self.wumpus_possible.add((nx, ny))

    def shoot_arrow(self):
        if self.arrow_used:
            return
        for wx, wy in self.wumpus_possible:
            if abs(wx - self.x) + abs(wy - self.y) == 1:
                print(f"Wumpus suspected at ({wx}, {wy}). Shooting arrow...")
                self.arrow_used = True
                if self.env.get_cell(wx, wy).has_wumpus:
                    print("Wumpus killed!")
                    self.env.get_cell(wx, wy).has_wumpus = False
                    self.env.update_percepts()
                    self.wumpus_killed = True
                else:
                    print("Missed the Wumpus!")
                break

    def move(self):
        self.visited.add((self.x, self.y))
        self.infer_safe_neighbors()
        for cell in self.safe:
            if cell not in self.visited:
                self.x, self.y = cell
                self.path.append(cell)
                return True
        return False

    def backtrack_to_start(self):
        if self.path[-1] != self.start:
            print("Returning to start...")
            self.path = self.path[::-1]  # Reverse path
            for (x, y) in self.path:
                print(f"Backtrack to ({x}, {y})")
            print("Agent safely returned to start with gold!")

    def act(self):
        while True:
            percepts = self.perceive()
            print(f"At ({self.x}, {self.y}) perceives: {percepts}")
            if percepts["glitter"] and not self.gold_collected:
                print(f"Gold found at ({self.x}, {self.y})! Collecting...")
                self.gold_collected = True
                self.backtrack_to_start()
                break

            if percepts["stench"] and not self.arrow_used:
                self.shoot_arrow()

            moved = self.move()
            if not moved:
                print("No more safe moves. Agent stops.")
                break

    def get_neighbors(self, x, y):
        neighbors = []
        for dx, dy in [(-1,0), (1,0), (0,-1), (0,1)]:
            nx, ny = x + dx, y + dy
            if 0 <= nx < self.env.size and 0 <= ny < self.env.size:
                neighbors.append((nx, ny))
        return neighbors
