import random
from individual import Individual

class Simulation:
    def __init__(self, env, species_list):
        self.env = env
        self.individuals = []
        for species in species_list:
            for _ in range(species.number):
                    x = random.randint(0, env.width - 1)
                    y = random.randint(0, env.height - 1)
                    self.individuals.append(Individual(species, x, y, _))

    def step(self):
        already_paired = set()
        for ind in list(self.individuals):  # Make a copy to avoid issues if removing
            ind.move(self.env, self)
            ind.age += 1

            # Eat food if available
            eaten = self.env.consume_food(ind.x, ind.y, 1)
            ind.energy += eaten * 5
            # Remove if dead
            if ind.energy <= 0:
                print("Individual", ind.ID, "of species", ind.species.name, "has died.")
                self.individuals.remove(ind)
                ind.species.number-=1
            if len(self.individuals) == 0:
                 print("All individuals are dead.")
            # Reproduction logic
            if ind.ID in already_paired or ind.energy <= 70:
                continue
            for other in self.individuals:
                if other is not ind and other.species == ind.species and other.energy > 70:
                    if abs(other.x - ind.x) <= 1 and abs(other.y - ind.y) <= 1:
                        if other.ID not in already_paired:
                            from individual import Reproduce  # import here to avoid circular import
                            Reproduce(ind, other, self)
                            already_paired.add(ind.ID)
                            already_paired.add(other.ID)
                            break

        self.env.grow_food()