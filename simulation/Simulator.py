from simulation.Particle import Particle
from simulation.SimFrame import SimFrame


class Simulator:
    def __init__(self):
        pass

    def simulate(self, frame:SimFrame):
        particles = frame.get_particles()
        for i in range(len(particles)):
            x, y = particles[i].get_position()
            particles[i] = Particle(x + 1, y + 1, 0, 0)

        return SimFrame(particles)
