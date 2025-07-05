import pygame
from environment import Environment
from agent import Agent

CELL_SIZE = 50
WIDTH = HEIGHT = 10 * CELL_SIZE

def draw_grid(screen, env, agent):
    colors = {
        'pit': (0, 0, 0),
        'gold': (255, 215, 0),
        'wumpus': (255, 0, 0),
        'agent': (0, 255, 0),
        'safe': (200, 255, 200),
        'visited': (180, 180, 255)
    }

    for x in range(env.size):
        for y in range(env.size):
            rect = pygame.Rect(y * CELL_SIZE, x * CELL_SIZE, CELL_SIZE, CELL_SIZE)
            cell = env.grid[x][y]

            if (x, y) in agent.visited:
                pygame.draw.rect(screen, colors['visited'], rect)
            elif (x, y) in agent.safe:
                pygame.draw.rect(screen, colors['safe'], rect)
            else:
                pygame.draw.rect(screen, (240, 240, 240), rect)

            if cell.has_pit:
                pygame.draw.circle(screen, colors['pit'], rect.center, 8)
            if cell.has_wumpus:
                pygame.draw.circle(screen, colors['wumpus'], rect.center, 8)
            if cell.has_gold:
                pygame.draw.circle(screen, colors['gold'], rect.center, 8)

    ax, ay = agent.x, agent.y
    rect = pygame.Rect(ay * CELL_SIZE, ax * CELL_SIZE, CELL_SIZE, CELL_SIZE)
    pygame.draw.rect(screen, colors['agent'], rect, 3)

def run_gui_simulation():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Wumpus World AI")

    env = Environment(size=10)
    env.generate_random()
    agent = Agent(env)

    clock = pygame.time.Clock()
    running = True
    paused = False

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        screen.fill((255, 255, 255))
        draw_grid(screen, env, agent)
        pygame.display.flip()

        if not paused:
            percepts = agent.perceive()
            print(f"At ({agent.x}, {agent.y}) perceives: {percepts}")
            if percepts["glitter"] and not agent.gold_collected:
                print(f"Gold found at ({agent.x}, {agent.y})! Collecting...")
                agent.gold_collected = True
                agent.backtrack_to_start()
                paused = True
            elif percepts["stench"] and not agent.arrow_used:
                agent.shoot_arrow()
            else:
                moved = agent.move()
                if not moved:
                    print("No more safe moves. Agent stops.")
                    paused = True

        clock.tick(1)  # 1 frame per second

    pygame.quit()
