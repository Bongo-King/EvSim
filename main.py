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

    env = Environment(WIDTH, HEIGHT)
    sim = Simulation(env, speciesList)

    running = True
    frame_count = 0
    sim_speed = 15  # Only run sim.step() every 5 frames

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Step the simulation only every N frames
        if frame_count % sim_speed == 0:
            sim.step()

        draw_grid(screen, env, sim.individuals)
        pygame.display.flip()

        frame_count += 1
        clock.tick(30)  # Visual framerate target (30 FPS)

    pygame.quit()


if __name__ == "__main__":
    run_simulation_loop()
