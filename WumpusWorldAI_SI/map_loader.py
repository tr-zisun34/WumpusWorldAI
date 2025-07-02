from environment import Environment, Cell

def load_map_from_file(filename):
    with open(filename, 'r') as file:
        lines = file.readlines()

    size = len(lines)
    env = Environment(size=size)
    env.grid = [[Cell() for _ in range(size)] for _ in range(size)]

    for i, line in enumerate(lines):
        for j, char in enumerate(line.strip()):
            cell = env.grid[i][j]
            if 'P' in char: cell.has_pit = True
            if 'W' in char: cell.has_wumpus = True
            if 'G' in char: cell.has_gold = True

    env.generate_environment()  # Refresh percepts
    return env
