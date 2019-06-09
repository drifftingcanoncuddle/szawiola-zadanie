from Maintain.ConfigManipulator import ConfigFields
from Maintain.ConfigManipulator import ConfigManipulator
from simulation.SimFrame import SimFrame
from simulation.Particle import Particle

from Maintain.Exceptions import MissingParticleParams
from Maintain.Exceptions import WrongFileFormatException

import random
import math


class Initiator:
    """
        Creates first frame for further simulation, can read data from csv formatted plain text document,
        which name should be supplied under -f option during script startup

    """
    def __init__(self):
        self.config_manipulator = ConfigManipulator()
        self.max_speed = float(self.config_manipulator.read(ConfigFields.maxSpeed))
        self.size = (float(self.config_manipulator.read(ConfigFields.size)),
                     float(self.config_manipulator.read(ConfigFields.size)))
        self.box_size = float(self.config_manipulator.read(ConfigFields.boxSize))
        self.max_particles_count = float(self.config_manipulator.read(ConfigFields.particleAmount))

    def create(self) -> SimFrame:
        """
        function to call to generate first frame,
        generation from file is inferred from existence of init_file value in config.ini
        :return: SimFrame with first state
        """
        print("Creating first frame")

        init_satate_file = self.config_manipulator.read(ConfigFields.init_state_file)
        if init_satate_file == "":
            # file not found
            return self.create_random()
        else:
            # file found
            return self.create_from_file(init_satate_file)

    def create_random(self) -> SimFrame:
        """
        private subfunciton for random generation of states
        :return: SimFrame
        """
        print("first frame will be created randomly")

        particles = []
        count_of_created_particles = 0
        while count_of_created_particles < self.max_particles_count:
            position = self.dice_position()
            speed = self.dice_speed()
            new_particle = Particle(position[0],
                                    position[1],
                                    speed[0],
                                    speed[1])

            particles.append(new_particle)
            count_of_created_particles += 1

        # for particle in particles:
        #     print(particle)

        return SimFrame(particles)

    def create_from_file(self, file: str) -> SimFrame:
        """
        Private subfunction, bla bla bla
        :param file: csv file containing data for particles
        :return: SimFrame
        """
        print("First frame will be read from file")
        file_suffix = file.split(".")[-1]
        if file_suffix != "csv":
            raise ResourceWarning("Wrong file format")
        else:
            with open(file, "r") as file_with_particles:
                particles = []
                particle_count = 0
                line = file_with_particles.readline()
                while line != "":
                    line = line.replace(" ", "")
                    particle_properties = line.split(",")
                    try:
                        if len(particle_properties) < 4:
                            raise MissingParticleParams(
                                "Found only " + len(particle_properties) +
                                " on particle " + particle_count)
                        else:
                            new_particle = Particle(int(particle_properties[0]),
                                                    int(particle_properties[1]),
                                                    int(particle_properties[2]),
                                                    int(particle_properties[3]))
                            particles.append(new_particle)

                    except MissingParticleParams as E:
                        print(E)

                    particle_count += 1
                    line = file_with_particles.readline()
                ConfigManipulator().set(ConfigFields.particleAmount, particle_count)
                return SimFrame(particles)

    def dice_speed(self) -> (float, float):
        """
        Dice speed for particle,
        x component is randomized, and y component is calculated as cathetus of right angle triangle,
        so hypotenuse holds
        :return: speed tuple
        """
        speed_x = random.random() * self.max_speed
        speed_y = math.sqrt(self.max_speed ** 2 - speed_x ** 2)

        # also randomize directions of move
        if random.randint(0, 1) == 0:
            speed_x = -speed_x
        if random.randrange(0, 1) == 1:
            speed_y = -speed_y

        return speed_x, speed_y

    def dice_position(self):
        """
        Dice position
        :return: position tuple
        """
        x = random.random() * self.box_size

        y = random.random() * self.size[1]

        return x, y