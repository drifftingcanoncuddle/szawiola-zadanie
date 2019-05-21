from Maintain.ConfigManipulator import ConfigFields
from Maintain.ConfigManipulator import ConfigManipulator
from simulation.SimFrame import SimFrame
from simulation.Particle import Particle

import random


class Initiator:
    def __init__(self):
        pass

    def create(self):
        particles = list()
        max_x = int(ConfigManipulator().read(ConfigFields.sizeX))
        max_y = int(ConfigManipulator().read(ConfigFields.sizeY))
        for i in range(int(ConfigManipulator().read(ConfigFields.particleAmount))):
            particles.append(Particle(random.randint(0,max_x),
                                      random.randint(0, max_y),
                                      0,
                                      0))
        return SimFrame(particles)
