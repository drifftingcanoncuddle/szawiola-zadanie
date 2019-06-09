import pickle

from simulation.SimFrame import SimFrame
from simulation.Particle import Particle
from Maintain.ConfigManipulator import ConfigManipulator
from Maintain.ConfigManipulator import ConfigFields
from simulation.Initiator import Initiator
from simulation.Simulator import Simulator

from typing import *

import matplotlib.pyplot as mpl
import matplotlib.animation as animation
import numpy as np


class DrawVX:
    """
        Class create animation showing changes of position in time
        """
    def __init__(self):
        self.config = ConfigManipulator()
        self.particles_amount = int(self.config.read(ConfigFields.particleAmount))
        self.particle_size = int(self.config.read(ConfigFields.particleSize)) * 265 / int(self.config.read(ConfigFields.size))
        self.box_size = int(self.config.read(ConfigFields.boxSize))

        self.figure, self.axes = mpl.subplots()
        self.anim = None
        self.dpi = 500
        self.path = "VXAnimation.mp4"

        self.frame_number = 1
        self.frames = self.unpickle()

        print("Drawing VX chart")

    def unpickle(self) -> List[SimFrame]:
        """
                Obtain table with simframes from pickled file
                :return:
                """
        with open("simulation.sim", "rb") as file:
            return pickle.load(file)

    def init_drawing(self):
        """
                Initialize chart
                :return:
                """
        print("Intalizing")
        # set positions
        sim_frame = self.frames[0]
        x = list()
        y = list()
        for particle in sim_frame.get_particles():
            x.append(particle.get_position()[0])
            y.append(particle.get_position()[1])

        # set colorts
        colors = 0.02 * (np.random.random(self.particles_amount)) - 0.5

        # plot chart
        self.scat = self.axes.scatter(x, y, s=self.particle_size ** 2, c=colors)
        self.axes.axis([0,
                        int(self.config.read(ConfigFields.size)),
                        0,
                        int(self.config.read(ConfigFields.size))])

        # set ticks
        grid_ticks = np.arange(0,
                               int(self.config.read(ConfigFields.size)),
                               self.box_size)

        self.axes.set_xticks(grid_ticks)
        self.axes.set_yticks(grid_ticks)

        # add grid
        self.axes.grid()

        return self.scat,

    def update(self, step):
        """
        Update animation
        :return:
        """
        print("Rendering frame: ", self.frame_number)
        # check new positions
        sim_frame = self.frames[self.frame_number]
        positions = list()

        # change title showing frame number
        self.axes.set_title(self.frame_number)
        for particle in sim_frame.get_particles():
            x = particle.get_position()[0]
            y = particle.get_position()[1]
            positions.append((x, y))

        self.frame_number += 1

        # save positions to chart
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


if __name__ == "__main__":
    DrawVX().draw()
