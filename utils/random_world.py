import random

def generate_random_world(pit_prob=0.1, wumpus_count=2, gold_count=1):
    grid = [['-' for _ in range(10)] for _ in range(10)]

    # Place pits
    for y in range(10):
        for x in range(10):
            if (x, y) == (0, 9):  # Starting point must be safe
                continue
            if random.random() < pit_prob:
                grid[y][x] = 'P'

    # Place Wumpus
    for _ in range(wumpus_count):
        while True:
            x, y = random.randint(0, 9), random.randint(0, 9)
            if grid[y][x] == '-' and (x, y) != (0, 9):
                grid[y][x] = 'W'
                break

    # Place Gold
    for _ in range(gold_count):
        while True:
            x, y = random.randint(0, 9), random.randint(0, 9)
            if grid[y][x] == '-' and (x, y) != (0, 9):
                grid[y][x] = 'G'
                break

    return grid

def save_world_to_file(grid, path='worlds/random.txt'):
    with open(path, 'w') as file:
        for row in grid:
            file.write(''.join(row) + '\n')
