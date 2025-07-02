# from environment import Environment
# from agent import Agent
# import sys


# def main():
#     env = Environment(size=10)
#     if len(sys.argv) > 1 and sys.argv[1] == "--load":
#         env.load_from_file("maps/map1.json")
#     else:
#         env.generate_random()

#     agent = Agent(env)
#     agent.act()

# if __name__ == "__main__":
#     main()

from environment import Environment
from agent import Agent

def run_simulation():
    env = Environment(size=10)  # Create 10x10 environment
    agent = Agent(env)

    print("Starting Wumpus World Simulation...\n")
    agent.act()

    print("\nFinal Stats:")
    print("Path taken:", agent.path)
    print("Gold collected:", agent.gold_collected)
    print("Visited cells:", agent.visited)
    print("Safe cells:", agent.safe)

if __name__ == "__main__":
    # run_simulation()  # Text version
    from ui import run_gui_simulation
    run_gui_simulation()  # GUI version

