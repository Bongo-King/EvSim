class Species:
    def __init__(self, name, color, is_predator, behavior_weights, base_traits, terrain_affinity, number):
        self.name = name
        self.color = color
        self.is_predator = is_predator
        self.behavior_weights = behavior_weights
        self.base_traits = base_traits  # e.g. {'speed': 1.0, 'size': 0.5}
        self.terrain_affinity = terrain_affinity  # e.g. {'forest': 1.0, 'rock': 0.4}
        self.number = number

# Create example species

rabbit = Species(
    name="Rabbit",
    color= (0,0,255),
    is_predator=False,
    base_traits={"speed": 1.2, "size": 0.5, "vision_radius": 2},
    behavior_weights= {"food": 1.0, "reproduction": 1.3, "exploration": 0.5, "avoid_predators": 1.5,},
    terrain_affinity={"grassland": 1.0, "forest": 0.7, "desert": 0.5, "mountain": 0.3},
    number = 20
)

wolf = Species(
    name="Wolf",
    color=(255,0,0),
    is_predator=True,
    base_traits={"speed": 1.5, "size": 1.0, "vision_radius": 3},
    behavior_weights= {"food": 2.0, "reproduction": 1.3, "exploration": 1.0, "avoid_predators": 0.5,},
    terrain_affinity={"forest": 1.0, "grassland": 0.6, "desert": 0.3, "mountain": 0.4},
    number = 10
)

speciesList = [rabbit,wolf]
    
