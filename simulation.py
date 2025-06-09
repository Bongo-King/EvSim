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
        for ind in list(self.individuals):  # Make a copy to avoid issues if removing
            ind.move(self.env, self)
            ind.age += 1

            # Eat food if available
            self.env.consume_food(ind.x, ind.y, 1)
            # Remove if dead
            if ind.energy <= 0:
                print("Individual", ind.ID, "of species", ind.species.name, "has died.")
                self.individuals.remove(ind)
                ind.species.number-=1
            if len(self.individuals) == 0:
                 print("All individuals are dead.")

        self.env.grow_food()