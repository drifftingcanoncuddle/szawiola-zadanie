import pickle

from simulation.Initiator import Initiator
from simulation.Particle import Particle
from simulation.SimFrame import SimFrame
from Maintain.ConfigManipulator import ConfigFields
from Maintain.ConfigManipulator import ConfigManipulator

from Maintain.Exceptions import NeverCollideException

from typing import *

import copy
import math


class Simulator:
    def __init__(self):
        self.time_delta = float(ConfigManipulator().read(ConfigFields.timeDelta))
        self.size_x = float(ConfigManipulator().read(ConfigFields.size))
        self.size_y = float(ConfigManipulator().read(ConfigFields.size))
        self.maximal_distance_as_collision = float(ConfigManipulator().read(ConfigFields.maximalDistanceAsCollision))
        self.maximal_timedelta_as_colliding = float(ConfigManipulator().read(ConfigFields.maximalTimeDeltaAsColliding))
        self.particle_size = float(ConfigManipulator().read(ConfigFields.particleSize))
        self.time = int(ConfigManipulator().read(ConfigFields.time))

    def dump(self):
        frames_count = 0

        states = list()
        states.append(Initiator().create())

        while frames_count < self.time:
            frames_count += 1
            f = copy.deepcopy(states[-1])
            states.append(self.simulate(f))

        with open("simulation.sim", "wb") as file:
            pickle.dump(states, file)

    def simulate(self, frame: SimFrame) -> SimFrame:

        print("-" * 10)
        print("Rendering frame")
        particles = frame.get_particles()

        # was_fixed = True
        #
        # while was_fixed:
        #     was_fixed = False
        #     for p1 in range(len(particles)):
        #         for p2 in range(len(particles)):
        #             if self.distance_p(particles[p1], particles[p2]) < self.particle_size * 2:
        #                 was_fixed = True
        #                 while self.distance_p(particles[p1], particles[p2]) < self.particle_size * 2:
        #                     particles[p1] = self.move(particles[p1], self.time_delta)
        #                     particles[p2] = self.move(particles[p2], self.time_delta)

        print("Checking collisions with walls")
        for p in range(len(particles)):
            is_collidong = self.wall_collision(particles[p])
            if is_collidong is not None:
                print("Particle number {} is colliding with wall {}".format(p,
                                                                            is_collidong))
                particles[p] = self.collide_with_wall(particles[p], is_collidong)

        print("Checking collisions between particles")
        for p1 in range(len(particles)):
            for p2 in range(len(particles)):
                if p1 != p2:
                    if self.distance_p(particles[p1], particles[p2]) - self.particle_size / 2 < self.maximal_distance_as_collision:
                        print("Particle {} collides with {} on distance {}".format(p1, p2,
                                                                                   self.distance_p(particles[p1], particles[p2]) - self.particle_size / 2))
                        particles[p1], particles[p2] = self.collide_with_particle(particles[p1], particles[p2])

        print("Moving particles")
        for p in range(len(particles)):
             particles[p] = self.move(particles[p], self.time_delta)

        print("Frame rendered")
        print("-" * 10)
        return SimFrame(particles)



    def distance(self, particle_1: Particle, particle_2: Particle) -> float:
        particle_1_x = particle_1.get_position()[0]
        particle_1_y = particle_1.get_position()[1]

        particle_2_x = particle_2.get_position()[0]
        particle_2_y = particle_2.get_position()[1]

        x_difference = particle_1_x - particle_2_x
        y_difference = particle_1_y - particle_2_y

        return math.sqrt(x_difference ** 2 + y_difference ** 2)

    def distance_p(self, particle_1: Particle, particle_2: Particle) -> float:
        particle_1_x = particle_1.get_position()[0]
        particle_1_y = particle_1.get_position()[1]

        particle_2_x = particle_2.get_position()[0]
        particle_2_y = particle_2.get_position()[1]

        x_difference = particle_1_x - particle_2_x
        y_difference = particle_1_y - particle_2_y

        return math.sqrt(x_difference ** 2 + y_difference ** 2)

    def distance(self, point1: Tuple[float], point2: Tuple[float]) -> float:
        point1_x = point1[0]
        point1_y = point1[1]

        point2_x = point2[0]
        point2_y = point2[1]

        x_difference = point1_x - point2_x
        y_difference = point1_y - point2_y

        return math.sqrt(x_difference ** 2 + y_difference ** 2)

    def distance(self, particle: Particle, point2: Tuple[float]) -> float:
        point1_x = particle.get_position()[0]
        point1_y = particle.get_position()[1]

        point2_x = point2[0]
        point2_y = point2[1]

        x_difference = point1_x - point2_x
        y_difference = point1_y - point2_y

        return math.sqrt(x_difference ** 2 + y_difference ** 2)

    def distance(self, particle: Particle, point2: List[float]) -> float:
        point1_x = particle.get_position()[0]
        point1_y = particle.get_position()[1]

        point2_x = point2[0]
        point2_y = point2[1]

        x_difference = point1_x - point2_x
        y_difference = point1_y - point2_y

        return math.sqrt(x_difference ** 2 + y_difference ** 2)

    def move(self, particle: Particle, time: float) -> Particle:
        particle_x = particle.get_position()[0]
        particle_y = particle.get_position()[1]

        particle_vx = particle.get_velocity()[0]
        particle_vy = particle.get_velocity()[1]

        delta_x = particle_vx * time
        delta_y = particle_vy * time

        particle_x += delta_x
        particle_y += delta_y

        return Particle(particle_x, particle_y,
                        particle_vx, particle_vy)

    def collide_with_particle(self, particle_1: Particle, particle_2: Particle) -> (Particle, Particle):
        x_diff = particle_1.get_position()[0] - particle_2.get_position()[0]
        y_diff = particle_1.get_position()[1] - particle_2.get_position()[1]

        x_diff += 0.00001

        rotation = math.atan(y_diff / x_diff)

        particle_1_combined_speed = particle_1.get_combined_speed()
        particle_2_combined_speed = particle_2.get_combined_speed()

        particle_1_a = self.get_trajectory(particle_1)[0]
        particle_2_a = self.get_trajectory(particle_2)[0]

        particle_1_combined_speed_angle = math.atan(particle_1_a)
        particle_2_combined_speed_angle = math.atan(particle_2_a)

        new_particle_1_combined_speed_angle = particle_1_combined_speed_angle - rotation
        new_particle_2_combined_speed_angle = particle_2_combined_speed_angle - rotation

        new_particle_1_vx = particle_1_combined_speed * math.cos(new_particle_1_combined_speed_angle)
        new_particle_1_vy = particle_1_combined_speed * math.sin(new_particle_1_combined_speed_angle)

        new_particle_2_vx = particle_2_combined_speed * math.cos(new_particle_2_combined_speed_angle)
        new_particle_2_vy = particle_2_combined_speed * math.sin(new_particle_2_combined_speed_angle)

        new_particle_2_vx, new_particle_1_vx = new_particle_1_vx, new_particle_2_vx

        particle_1_combined_speed = math.sqrt(new_particle_1_vx ** 2 + new_particle_1_vy ** 2)
        particle_2_combined_speed = math.sqrt(new_particle_2_vx ** 2 + new_particle_2_vy ** 2)

        new_particle_1_combined_speed_angle = math.atan(new_particle_1_vy / new_particle_2_vx)
        new_particle_2_combined_speed_angle = math.atan(new_particle_2_vy / new_particle_2_vx)

        old_particle_1_combined_speed_angle = new_particle_1_combined_speed_angle + rotation
        old_particle_2_combined_speed_angle = new_particle_2_combined_speed_angle + rotation

        old_particle_1_vx = particle_1_combined_speed * math.cos(old_particle_1_combined_speed_angle)
        old_particle_1_vy = particle_1_combined_speed * math.sin(old_particle_1_combined_speed_angle)

        old_particle_2_vx = particle_2_combined_speed * math.cos(old_particle_2_combined_speed_angle)
        old_particle_2_vy = particle_2_combined_speed * math.sin(old_particle_2_combined_speed_angle)

        particle_1_x, particle_1_y = particle_1.get_position()
        particle_2_x, particle_2_y = particle_2.get_position()

        new_particle_1 = Particle(particle_1_x, particle_1_y,
                        old_particle_1_vx, old_particle_1_vy)

        new_particle_2 = Particle(particle_2_x, particle_2_y,
                         old_particle_2_vx, old_particle_2_vy)

        print("Fixing particles positions after collision")

        while self.distance_p(new_particle_1, new_particle_2) < self.particle_size:
            print("Distance to fix: ", self.distance_p(particle_1, particle_2))
            new_particle_1 = self.move(new_particle_1, self.time_delta / 5)
            new_particle_2 = self.move(new_particle_2, self.time_delta / 5 * -1)

        return new_particle_1, new_particle_2


    def collide_with_wall(self, particle, wall):
        if wall == "T":
            return Particle(particle.get_position()[0], self.size_x - self.particle_size / 2,
                            particle.get_velocity()[0], -1 * particle.get_velocity()[1])
        elif wall == "B":
            return Particle(particle.get_position()[0], self.particle_size / 2,
                            particle.get_velocity()[0], -1 * particle.get_velocity()[1])
        elif wall == "L":
            return Particle(self.particle_size / 2, particle.get_position()[1],
                            particle.get_velocity()[0] * -1, particle.get_velocity()[1])
        elif wall == "R":
            return Particle(self.size_x - self.particle_size / 2, particle.get_position()[1],
                            particle.get_velocity()[0] * -1, particle.get_velocity()[1])

    def get_trajectory(self, particle: Particle) -> (float, float):
        particle_vx = particle.get_velocity()[0]
        particle_vy = particle.get_velocity()[1]

        particle_x = particle.get_position()[0]
        particle_y = particle.get_position()[1]

        if particle_vx == 0:
            a = 1
        else:
            a = particle_vy / particle_vx

        b = particle_y - a * particle_x

        return a, b

    def wall_collision(self, particle: Particle) -> str:
        particle_x = particle.get_position()[0]
        particle_y = particle.get_position()[1]

        if particle_x < self.particle_size / 2.5:
            return "L"
        elif particle_x > self.size_x - self.particle_size / 2.5:
            return "R"
        elif particle_y > self.size_y - self.particle_size / 2.5:
            return "T"
        elif particle_y < self.particle_size / 2.5:
            return "B"
        else:
            return None

