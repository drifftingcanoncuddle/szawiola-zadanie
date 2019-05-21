class SimFrame:
    def __init__(self, particles):
        self.particles = particles

    def get_particle(self, number):
        return self.particles[number]

    def get_particles(self):
        return self.particles

