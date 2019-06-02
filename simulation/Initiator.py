from Maintain.ConfigManipulator import ConfigFields
from Maintain.ConfigManipulator import ConfigManipulator
from simulation.SimFrame import SimFrame
from simulation.Particle import Particle

from Maintain.Exceptions import MissingParticleParams
from Maintain.Exceptions import WrongFileFormatException

import random
import math


class Initiator:
    def __init__(self):
        self.config_manipulator = ConfigManipulator()
        self.max_speed = float(self.config_manipulator.read(ConfigFields.maxSpeed))
        self.size = (float(self.config_manipulator.read(ConfigFields.size)),
                     float(self.config_manipulator.read(ConfigFields.size)))
        self.box_size = float(self.config_manipulator.read(ConfigFields.boxSize))
        self.max_particles_count = float(self.config_manipulator.read(ConfigFields.particleAmount))

    def create(self) -> SimFrame:
        init_satate_file = self.config_manipulator.read(ConfigFields.init_state_file)
        if init_satate_file == "":
            return self.create_random()
        else:
            return self.create_from_file(init_satate_file)

    def create_random(self) -> SimFrame:
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

        for particle in particles:
            print(particle)

        return SimFrame(particles)

    def create_from_file(self, file: str) -> SimFrame:
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

                return SimFrame(particles)

    def dice_speed(self) -> (float, float):
        speed_x = random.random() * self.max_speed
        speed_y = math.sqrt(self.max_speed ** 2 - speed_x ** 2)

        return speed_x, speed_y

    def dice_position(self):

        x = random.random() * self.box_size

        y = random.random() * self.size[1]

        return x, y