import math
import pickle
from copy import deepcopy
from typing import *
import numpy as np
import matplotlib.pyplot as plt

from Arithmetic.DrawTHProb import THProb
from Maintain.ConfigManipulator import ConfigManipulator, ConfigFields


from simulation.Initiator import Initiator
from simulation.SimFrame import SimFrame
from simulation.Simulator import Simulator


class Entropy:
    """
        Function used to calculate and draw enthropy

        MACROSTATE
        [ posX ] [ posY] [ speedX ] [ speedY ]
    """
    def __init__(self):
        self.configparser = ConfigManipulator()
        self.size = int(self.configparser.read(ConfigFields.size))
        self.box_size = int(self.configparser.read(ConfigFields.boxSize))
        self.max_speed = int(self.configparser.read(ConfigFields.maxSpeed))
        self.particle_amount = int(self.configparser.read(ConfigFields.particleAmount))
        self.time = int(self.configparser.read(ConfigFields.time))
        self.frames = self.unpickle()
        self.max_box_speed = math.floor(self.max_speed / self.box_size)
        self.max_box_size = math.floor(self.size / self.box_size)

    def unpickle(self) -> List[SimFrame]:
        """
        Reads pickled table with simframes, aka simulation.sim
        :return:
        """
        with open("simulation.sim", "rb") as file:
            return pickle.load(file)

    def evaluate(self):
        """
        Function iterates over table with simframes and calculate entropy for each,
        adds it to another table and draw a chart
        :return:
        """
        print("Evaluating entropy")
        x = np.arange(0, self.time + 1, 1)
        y = list()

        actual_frame = 0

        while actual_frame <= self.time:
            print("Evaluating entropy for frame: ", actual_frame)
            entropy = self.get_entropy(self.frames[actual_frame])
            y.append(entropy)
            actual_frame += 1

        fig, ax = plt.subplots()

        fig.suptitle('Zmiana entropii w czasie')

        ax.set_xlabel("czas (kl)")
        ax.set_ylabel("entropia")
        ax.plot(x, y, c='r')
        # ax.set_yscale('log')
        plt.savefig("entropy.png", dpi=500)

    def get_entropy(self, frame: SimFrame) -> float:
        """
        Function eval entropy for given simframe
        Utilize THProb from other class
        :param frame:
        :return: float as entrpy
        """
        thprob = THProb().get_thermal_probability(frame)
        return math.log(thprob)