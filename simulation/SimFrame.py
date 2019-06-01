from typing import *
from simulation.Particle import Particle


class SimFrame:
    def __init__(self, particles: List[Particle]):
        self.particles = particles

    def get_particle(self, number):
        return self.particles[number]

    def get_particles(self):
        return self.particles

