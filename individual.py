import random
import simulation

DIRECTIONS = [
    (-1, 0),  # left
    (1, 0),   # right
    (0, -1),  # up
    (0, 1),   # down
    (-1, -1), # up-left
    (-1, 1),  # down-left
    (1, -1),  # up-right
    (1, 1),   # down-right
]


class Individual:
    def __init__(self, species, x, y, ind_ID, behavior_weights, traits=None):
        self.species = species
        self.x = x
        self.y = y
        self.ID = ind_ID
        self.energy = 100
        self.age = 0
        self.behavior_weights = behavior_weights if behavior_weights else species.behavior_weights.copy()
        self.traits = traits if traits else species.base_traits.copy()
        
    def get_nearby_individuals(self, others):
        nearby = []
        radius = self.traits["vision_radius"]
        for other in others:
            if other is not self:
                dx = abs(other.x - self.x)
                dy = abs(other.y - self.y)
                if dx <= radius and dy <= radius:
                    nearby.append(other)
        return nearby
    
  

    def move(self, env, sim):
        width = env.width
        height = env.height
        best_score = -1
        best_move = (self.x, self.y)
        nearby = self.get_nearby_individuals(sim.individuals)

        #if the individual has enough energy to reproduce, move towards other members of the same species with enough energy
        if self.energy >70:
            for ind in nearby:
                if ind.species == self.species and ind.energy > 70:
                    if abs(ind.x - self.x) > 1:
                        dx = 1 if ind.x > self.x else -1 if ind.x < self.x else 0
                        dy = 1 if ind.y > self.y else -1 if ind.y < self.y else 0
                        best_move = (self.x + dx, self.y + dy)

                    #if next to each other, reproduce
                    elif ind.energy >70: 
                        Reproduce(self, ind, sim)
                        
        #if not, move to find food.
        else: 
            for dx, dy in DIRECTIONS:
                nx, ny = self.x + dx, self.y + dy

                if 0 <= nx < width and 0 <= ny < height:
                    terrain = env.get_terrain(nx, ny)
                    food = env.food[ny][nx]

                    # Base movement score: terrain affinity × food
                    terrain_affinity = self.species.terrain_affinity.get(terrain, 0.5)
                    score = terrain_affinity + (0.2 * food)

                    if score > best_score:
                        best_score = score
                        best_move = (nx, ny)

        # Move to best tile
        if best_move != (self.x, self.y):
            terrain = env.get_terrain(*best_move)
            move_cost = 2.0 - (self.traits["speed"] * self.species.terrain_affinity.get(terrain, 0.5))
            self.energy -= max(move_cost, 0.5)
            self.x, self.y = best_move
            # Lose energy from not moving
        else:
            self.energy-=1


    def evaluate_visible_tiles(self, env, individuals):
        vision = self.traits["vision_radius"]
        best_score = float('-inf')
        best_tile = (self.x, self.y)  # default: stay in place

        for dy in range(-vision, vision + 1):
            for dx in range(-vision, vision + 1):
                nx, ny = self.x + dx, self.y + dy

                if not (0 <= nx < env.width and 0 <= ny < env.height):
                    continue

                # FOOD SCORE
                food_score = env.food[ny][nx] / 5.0  # normalize

                # REPRODUCTION SCORE
                mate_score = 0
                for other in individuals:
                    if other is not self and other.species == self.species and other.energy > 70:
                        if abs(other.x - nx) <= 1 and abs(other.y - ny) <= 1:
                            mate_score += 1

                # EXPLORATION SCORE (favor tiles farther from current position)
                exploration_score = ((dx ** 2 + dy ** 2) ** 0.5) / vision

                # DANGER SCORE (inverse of predator proximity)
                danger_score = 0
                for other in individuals:
                    if other is not self and other.species != self.species:
                        dist = ((other.x - nx) ** 2 + (other.y - ny) ** 2) ** 0.5
                        if dist < 3:  # arbitrary danger radius
                            danger_score -= (3 - dist) / 3

                # TOTAL WEIGHTED SCORE
                score = (
                    self.behavior_weights["food"] * food_score +
                    self.behavior_weights["reproduction"] * mate_score +
                    self.behavior_weights["exploration"] * exploration_score +
                    self.behavior_weights["avoid_predators"] * danger_score
                )

                if score > best_score:
                    best_score = score
                    best_tile = (nx, ny)

        return best_tile



                

def Reproduce(ind1, ind2, sim):
    ind1.species.number+=1
    new = Individual(ind1.species, ind1.x, ind1.y, ind1.species.number)
    sim.individuals.append(new)
    ind1.energy-=70
    ind2.energy-=70
    return

