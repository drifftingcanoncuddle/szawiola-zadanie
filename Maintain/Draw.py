from simulation.SimFrame import SimFrame
from simulation.Particle import Particle
from Maintain.ConfigManipulator import ConfigManipulator
from Maintain.ConfigManipulator import ConfigFields
from simulation.Initiator import Initiator
from simulation.Simulator import Simulator

import matplotlib.pyplot as mpl
import matplotlib.animation as animation
import numpy as np


class Draw:
    def __init__(self, path):
        self.sim_frame = Initiator().create()
        self.config = ConfigManipulator()
        self.path = path
        self.particles_amount = int(self.config.read(ConfigFields.particleAmount))
        self.anim = None
        self.figure, self.axes = mpl.subplots()
        self.particle_size = int(self.config.read(ConfigFields.particleSize)) * 265 / int(self.config.read(ConfigFields.size))
        self.dpi = 500

    def init_drawing(self):
        x = list()
        y = list()
        for particle in self.sim_frame.get_particles():
            x.append(particle.get_position()[0])
            y.append(particle.get_position()[1])

        colors = 0.02 * (np.random.random(self.particles_amount)) - 0.5


        self.scat = self.axes.scatter(x, y, s=self.particle_size ** 2, c=colors)
        self.axes.axis([0,
                        int(self.config.read(ConfigFields.size)),
                        0,
                        int(self.config.read(ConfigFields.size))])
        return self.scat,

    def update(self, step):
        self.sim_frame = Simulator().simulate(self.sim_frame)
        positions = list()
        for particle in self.sim_frame.get_particles():
            x = particle.get_position()[0]
            y = particle.get_position()[1]
            positions.append((x, y))


        # positions
        self.scat.set_offsets(positions)

        # sizes
        # self.scat.set_sizes([10] * 2)

        #colors
        # self.scat.set_array([0.2] * 2)

        return self.scat,

    def draw(self):
        self.anim = animation.FuncAnimation(self.figure,
                                            self.update,
                                            interval=int(self.config.read(ConfigFields.time)),
                                            frames=int(self.config.read(ConfigFields.time)),
                                            init_func=self.init_drawing,
                                            blit=True
                                            )
        self.anim.save(self.path, dpi=self.dpi, fps=1/float(self.config.read(ConfigFields.timeDelta)), extra_args=['-vcodec', 'libx264'])


