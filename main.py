from environment import Environment
from species import Species, speciesList
from simulation import Simulation
import pygame

# === Constants ===
CELL_SIZE = 5
WIDTH = 275
HEIGHT = 175
SCREEN_WIDTH = WIDTH * CELL_SIZE
SCREEN_HEIGHT = HEIGHT * CELL_SIZE

# === Colors ===
TERRAIN_COLORS = {
    "plains": (200, 200, 150),      # yellowish
    "forest": (34, 139, 34),        # green
    "desert": (237, 201, 175),      # pale sand
    "water": (70, 130, 180),        # blue
    "mountain": (120, 120, 120),    # gray
}

COLOR_FOOD = (0, 255, 0)

def draw_grid(screen, env, individuals):
    screen.fill((0, 0, 0))

    # Draw terrain
    for y in range(env.height):
        for x in range(env.width):
            terrain = env.get_terrain(x, y)
            color = TERRAIN_COLORS.get(terrain, (100, 100, 100))
            pygame.draw.rect(
                screen,
                color,
                pygame.Rect(x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE)
            )

    # Draw food
    for y in range(env.height):
        for x in range(env.width):
            if env.food[y][x] > 0:
                center = (x * CELL_SIZE + CELL_SIZE // 2, y * CELL_SIZE + CELL_SIZE // 2)
                pygame.draw.circle(screen, COLOR_FOOD, center, 3)

    # Draw individuals
    for ind in individuals:
        center = (ind.x * CELL_SIZE + CELL_SIZE // 2, ind.y * CELL_SIZE + CELL_SIZE // 2)
        pygame.draw.circle(screen, ind.species.color, center, 4)

    pygame.display.flip()

def run_simulation_loop():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Evolution Simulator")
    clock = pygame.time.Clock()

    # === Initialize environment and simulation ===
    env = Environment(WIDTH, HEIGHT)
    sim = Simulation(env, speciesList)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        sim.step()
        draw_grid(screen, env, sim.individuals)
        clock.tick(5)  # 5 frames per second

    pygame.quit()

if __name__ == "__main__":
    run_simulation_loop()
