def display_world(world, agent):
    print("=== World State ===")
    for y in range(10):
        row = ''
        for x in range(10):
            if (agent.x, agent.y) == (x, y):
                row += 'A'
            else:
                row += world.grid[y][x].content
        print(row)
    print()
