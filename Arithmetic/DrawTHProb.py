import math
import pickle
from copy import deepcopy
from typing import *
import numpy as np
import matplotlib.pyplot as plt


from Maintain.ConfigManipulator import ConfigManipulator, ConfigFields


from simulation.Initiator import Initiator
from simulation.SimFrame import SimFrame
from simulation.Simulator import Simulator


class THProb:
    """
    Class used to calculate Thermal Probability
    """
    """
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
        Read pickled list with entire simulation form file
        :return: list with Simframes representing entire simulation
        """
        with open("simulation.sim", "rb") as file:
            return pickle.load(file)

    def evaluate(self):
        """
        Iterates over list with simulations, and calculate thprob for each
        :return:
        """
        print("Evaluating Thermal Probability")
        x = np.arange(0, self.time + 1, 1)
        y = list()

        actual_frame = 0

        while actual_frame <= self.time:
            print("THProb evaluating for frame: ", actual_frame)
            thprob = self.get_thermal_probability(self.frames[actual_frame])
            y.append(thprob)
            actual_frame += 1

        fig, ax = plt.subplots()

        fig.suptitle('Zmiana prawdopodobieństwa w czasie')

        ax.set_xlabel("czas (kl)")
        ax.set_ylabel("prawdopodobieństwo termodynamiczne")
        ax.plot(x, y)
        ax.set_yscale('log')
        plt.savefig("thprob.png", dpi=500)

    def create_macrostates(self, frame: SimFrame) -> np.ndarray:
        """
        Create ndarray representing macrostate.
        Shape of array is defined as:
            X -> maximal position in box coordinates + 1
            Y -> same as above
            vX -> maximal speed in box coordinates multiplied by two plus one,
                    cuz particle can has negative speed and 0 speed
            vY -> same as above
        :param frame:
        :return:
        """
        shape = (self.max_box_size + 1,
                 self.max_box_size + 1,
                 self.max_box_speed * 2 + 1,
                 self.max_box_speed * 2 + 1)
        particles = frame.get_particles()

        macrostate = np.ndarray(shape=shape, dtype=int)
        macrostate.fill(0)

        for particle in particles:
            x = particle.get_box_position()[0]
            y = particle.get_box_position()[1]

            x_speed = particle.get_box_velocities()[0]
            y_speed = particle.get_box_velocities()[1]

            # we need to fix speeds transforming them from system in which
            # they can have negative speeds, to system in which they can have
            # only positive or 0 speed
            # it's linear transformation to the left of value max_box_speed
            # then -max_box_speed becomes 0
            # and max_box_speed becomes two times bigger
            fixed_x_speed = x_speed + self.max_box_speed
            fixed_y_speed = y_speed + self.max_box_speed

            # also we need to check if we deal with particle which speeds are in
            # desired range - rounding errors can make situations in
            # which particles can obtain some extra speed
            # for them, we dont have place in ndarray
            if x_speed <= self.max_box_speed and y_speed <= self.max_box_speed:
                macrostate[x][y][fixed_x_speed][fixed_y_speed] += 1

        return macrostate

    def get_thermal_probability(self, frame: SimFrame) -> float:
        """
        In general thermal probability is permutaion with repeats over set of particles being
        in some macrostate.
        Then we can calculate it by dividing factorial of count of particles by product of
        factorials of particles being in this same state
        :param frame:
        :return:
        """

        macrostates = self.create_macrostates(frame)

        # we need to linearise 4D array
        macrostates_cout = macrostates.size
        macrostates = macrostates.reshape(macrostates_cout)

        # nominator = math.factorial(self.particle_amount)
        nominator = self.stirling_approximation(self.particle_amount)
        denominator = 1

        for i in range(macrostates_cout):
            denominator *= self.stirling_approximation(macrostates[i])

        # try:
        #     print(nominator, denominator)
        #     return nominator / denominator
        # except OverflowError as e:
        #     print("Float division overflow")
        #     return 10 ** 300

        return nominator / denominator

    def factorial(self, n: int):
        product = 1
        n1 = 2
        while n1 <= n:
            product *= n1
            n1 += 1
        return product

    def stirling_approximation(self, n):
        """
        Stirling approximation of factorial, although is faster than normal factorial
        python float math module allows to create numbers not grater than 10 ^ 300
        (200! is much grater), so we need to create some exceptions to catch this situations
        :param n:
        :return:
        """
        if n < 2:
            return 1
        else:
            try:
                return math.e ** (n * math.log(n) - n)
            except OverflowError as e:
                print("Float exponentiation overflow")
                return 10 ** 300
