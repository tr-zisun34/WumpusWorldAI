import tkinter as tk
from tkinter import ttk

CELL_SIZE = 50

class WumpusUI:
    def __init__(self, root, world, agent):
        self.root = root
        self.world = world
        self.agent = agent
        self.canvas = tk.Canvas(root, width=10 * CELL_SIZE, height=10 * CELL_SIZE)
        self.canvas.pack(padx=10, pady=10)
        
        # Status label for percepts
        self.status_text = tk.StringVar()
        ttk.Label(root, textvariable=self.status_text, font=('Arial', 12)).pack(pady=5)
        
        # Optional: color legend
        self.legend_frame = ttk.Frame(root)
        self.legend_frame.pack(pady=5)
        self.create_legend()

        self.draw_grid()

    def create_legend(self):
        legend = {
            "🧍‍♂️": "Agent",
            "💰": "Gold",
            "🐉": "Wumpus",
            "🕳️": "Pit",
            "Light Green": "Visited Cell",
            "White": "Safe Cell",
            "Orange": "Unsafe Cell"
        }

        for icon, label in legend.items():
            frame = ttk.Frame(self.legend_frame)
            frame.pack(side='left', padx=10)
            ttk.Label(frame, text=icon if icon.startswith("🧍") else "", font=("Arial", 16)).pack()
            ttk.Label(frame, text=label, font=("Arial", 10)).pack()

    def draw_grid(self):
        self.canvas.delete("all")
        for y in range(10):
            for x in range(10):
                cell = self.world.grid[y][x]
                px, py = x * CELL_SIZE, y * CELL_SIZE

                # Determine background color
                if (x, y) == (self.agent.x, self.agent.y):
                    color = "skyblue"
                elif (x, y) in self.agent.kb.visited_cells:
                    color = "lightgreen"
                elif (x, y) in self.agent.kb.safe_cells:
                    color = "white"
                elif (x, y) in self.agent.kb.unsafe_cells:
                    color = "orange"
                else:
                    color = "gray90"

                self.canvas.create_rectangle(px, py, px + CELL_SIZE, py + CELL_SIZE, fill=color, outline="black")

                # Draw emoji for contents
                if (x, y) == (self.agent.x, self.agent.y):
                    self.canvas.create_text(px + 25, py + 25, text="🧍‍♂️", font=("Arial", 22))

                elif cell.content == 'G':
                    self.canvas.create_text(px + 25, py + 25, text="💰", font=("Arial", 22))

                elif cell.content == 'W':
                    self.canvas.create_text(px + 25, py + 25, text="🐉", font=("Arial", 22))

                elif cell.content == 'P':
                    self.canvas.create_text(px + 25, py + 25, text="🕳️", font=("Arial", 22))

    def update(self, percepts):
        self.draw_grid()
        self.status_text.set(f"Percepts at ({self.agent.x},{self.agent.y}): {', '.join(percepts)}")
        self.root.update()
