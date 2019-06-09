from typing import *
from simulation.Particle import Particle


class SimFrame:
    """
    One state of world in some moment in time
    """
    def __init__(self, particles: List[Particle]):
        """
        :param particles: list with particles in world
        """
        self.particles = particles

    def get_particle(self, number) -> Particle:
        """
        getter for one particle
        :param number: number of particle in world
        :return: Particle
        """
        return self.particles[number]

    def get_particles(self) -> List[Particle]:
        """
        getter for whole list with particles
        :return:
        """
        return self.particles

