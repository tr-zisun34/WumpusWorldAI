import time
import tkinter as tk
from environment.world import World
from agent.agent import Agent
from ui.gui import WumpusUI
from utils.random_world import generate_random_world, save_world_to_file

def main():
    grid = generate_random_world()
    save_world_to_file(grid, 'worlds/random.txt')

    world = World('worlds/random.txt')
    agent = Agent(world)

    root = tk.Tk()
    root.title("Wumpus World AI")
    ui = WumpusUI(root, world, agent)

    # Simulation loop
    def step_loop():
        while True:
            percepts = agent.perceive()
            ui.update(percepts)
            proceed = agent.step()
            if not proceed:
                ui.status_text.set("Agent stopped.")
                break
            time.sleep(0.7)  # Pause to animate

    root.after(500, step_loop)
    root.mainloop()

if __name__ == "__main__":
    main()
