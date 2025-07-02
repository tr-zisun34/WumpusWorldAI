from environment import Environment

def save_random_map(filename="maps/random.txt"):
    env = Environment(size=10)
    with open(filename, 'w') as f:
        for row in env.grid:
            line = ""
            for cell in row:
                c = ""
                if cell.has_pit: c += "P"
                if cell.has_wumpus: c += "W"
                if cell.has_gold: c += "G"
                line += c or "."
            f.write(line + "\n")
