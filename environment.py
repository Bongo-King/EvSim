import random
import math
from noise import pnoise2

class Environment:
    def __init__(self, width, height, seed=None):
        self.width = width
        self.height = height
        self.terrain = []
        self.food = [[0 for _ in range(width)] for _ in range(height)]
        self.seed = seed if seed is not None else random.randint(0, 1000)
        self.generate_terrain()

    def generate_terrain(self):
        # Biome distribution
        WATER_PCT = 0.10
        PLAINS_PCT = 0.37
        FOREST_PCT = 0.28
        MOUNTAIN_PCT = 0.15
        DESERT_PCT = 0.10

        # ULTIMATE BIOME PARAMETERS (STRIPE-PROOF)
        # Core biome parameters
        biome_scale = 0.005  # Massive biome scale
        biome_rotation = 37   # Prime number rotation (avoids alignment)
        
        # Anti-stripe parameters
        jitter_amount = 0.3   # Breaks up grid patterns
        warp_scale = 0.02     # Warping for organic shapes
        warp_intensity = 3.0  # How much to warp coordinates
        
        # Pre-calculate rotation
        cos_rot = math.cos(math.radians(biome_rotation))
        sin_rot = math.sin(math.radians(biome_rotation))
        
        # Generate noise with anti-stripe measures
        noise_grid = []
        all_noise = []
        random.seed(self.seed)  # For jitter consistency
        
        for y in range(self.height):
            row = []
            for x in range(self.width):
                # 1. Add jitter to break grid alignment
                jitter_x = random.uniform(-jitter_amount, jitter_amount)
                jitter_y = random.uniform(-jitter_amount, jitter_amount)
                
                # 2. Apply coordinate rotation
                rot_x = (x + jitter_x) * cos_rot - (y + jitter_y) * sin_rot
                rot_y = (x + jitter_x) * sin_rot + (y + jitter_y) * cos_rot
                
                # 3. Apply domain warping to break linear patterns
                warp_x = warp_intensity * pnoise2(
                    rot_x * warp_scale,
                    rot_y * warp_scale,
                    octaves=4,
                    base=self.seed
                )
                warp_y = warp_intensity * pnoise2(
                    rot_x * warp_scale + 1000,
                    rot_y * warp_scale + 1000,
                    octaves=4,
                    base=self.seed + 1
                )
                
                # 4. Final coordinates for biome noise
                final_x = rot_x * biome_scale + warp_x
                final_y = rot_y * biome_scale + warp_y
                
                # Generate the actual biome noise
                noise_val = pnoise2(
                    final_x,
                    final_y,
                    octaves=1,  # Single octave for smooth biomes
                    persistence=0.9,
                    base=self.seed + 2
                )
                noise_val = (noise_val + 1) / 2  # Normalize
                row.append(noise_val)
                all_noise.append(noise_val)
            noise_grid.append(row)

        # Calculate thresholds
        all_noise.sort()
        water_thresh = all_noise[int(len(all_noise) * WATER_PCT)]
        plains_thresh = all_noise[int(len(all_noise) * (WATER_PCT + PLAINS_PCT))]
        forest_thresh = all_noise[int(len(all_noise) * (WATER_PCT + PLAINS_PCT + FOREST_PCT))]
        desert_thresh = all_noise[int(len(all_noise) * (WATER_PCT + PLAINS_PCT + FOREST_PCT + DESERT_PCT))]

        # Assign biomes
        self.terrain = []
        for y in range(self.height):
            row = []
            for x in range(self.width):
                nv = noise_grid[y][x]
                if nv < water_thresh:
                    terrain = "water"
                elif nv < plains_thresh:
                    terrain = "plains"
                elif nv < forest_thresh:
                    terrain = "forest"
                elif nv < desert_thresh:
                    terrain = "desert"
                else:
                    terrain = "mountain"
                row.append(terrain)
            self.terrain.append(row)

        # Debug: Print distribution
        from collections import Counter
        flat_terrain = [cell for row in self.terrain for cell in row]
        print("Terrain distribution:", Counter(flat_terrain))


    def get_terrain(self, x, y):
        return self.terrain[y][x]

    def grow_food(self):
        for y in range(self.height):
            for x in range(self.width):
                #if random.random() < 0.000005:
                if random.random() < 0.0005:  # Lowered growth chance

                    self.food[y][x] = min(5, self.food[y][x] + 1)

    def consume_food(self, x, y, amount):
        available = self.food[y][x]
        eaten = min(available, amount)
        self.food[y][x] -= eaten
        return eaten