from simulation.Particle import Particle
from simulation.SimFrame import SimFrame
from Maintain.ConfigManipulator import ConfigFields
from Maintain.ConfigManipulator import ConfigManipulator

from Maintain.Exceptions import NeverCollideException

from typing import *

import math


class Trajectory:
    def __init__(self, a: float, b: float):
        self.a = a
        self.b = b

    def get_a(self) -> float:
        return self.a

    def get_b(self) -> float:
        return self.b


class Transactions:
    def __init__(self):
        self.register = dict()

    def insert_transaction(self, particle_1: Particle, particle_2: Particle, time: float):
        if time < ConfigManipulator().read(ConfigFields.timeDelta):
            self.register[time] = (particle_1, particle_2)
        else:
            return


    def sort_transactions(self) -> dict:
        keys = self.register.keys()
        keys = sorted(keys)
        new_register = dict()
        for i in range(len(keys)):
            new_register[i] = self.register[keys[i]]
        return new_register


class Simulator:
    def __init__(self):
        self.time_delta = ConfigManipulator().read(ConfigFields.timeDelta)
        self.size_x = ConfigManipulator().read(ConfigFields.size)
        self.size_y = ConfigManipulator().read(ConfigFields.size)
        self.maximal_distance_as_collision = ConfigManipulator().read(ConfigFields.maximalDistanceAsCollision)
        self.maximal_timedelta_as_colliding = ConfigManipulator().read(ConfigFields.maximalTimeDeltaAsColliding)
        self.particle_size = ConfigManipulator().read(ConfigFields.particleSize)

    def simulate(self, frame: SimFrame) -> SimFrame:
        particles = frame.get_particles()
        for particle_1 in particles:
            for particle_2 in particles:
                if particle_1 is not particle_2:
                    if self.will_collide(particle_1, particle_2):
                        collision_point = self.get_collision_point(particle_1,
                                                                   particle_2)

    def distance(self, particle_1: Particle, particle_2: Particle) -> float:
        particle_1_x = particle_1.get_position()[0]
        particle_1_y = particle_1.get_position()[1]

        particle_2_x = particle_2.get_position()[0]
        particle_2_y = particle_2.get_position()[1]

        x_difference = particle_1_x - particle_2_x
        y_difference = particle_1_y - particle_2_y

        return math.sqrt(x_difference ** 2 + y_difference ** 2)

    def distance(self, point1: (float, float), point2: (float, float)) -> float:
        point1_x = point1[0]
        point1_y = point1[1]

        point2_x = point2[0]
        point2_y = point2[1]

        x_difference = point1_x - point2_x
        y_difference = point1_y - point2_y

        return math.sqrt(x_difference ** 2 + y_difference ** 2)

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

    def get_crossing_point(self, particle_1: Particle, particle_2: Particle) -> (float, float):
        trajectory_1 = self.get_trajectory(particle_1)
        trajectory_2 = self.get_trajectory(particle_2)

        trajectory_1_a = trajectory_1.get_a()
        trajectory_1_b = trajectory_1.get_b()

        trajectory_2_a = trajectory_2.get_a()
        trajectory_2_b = trajectory_2.get_b()

        collision_point_x = (trajectory_2_b - trajectory_1_b) / (trajectory_1_a - trajectory_2_a)
        collision_point_y = trajectory_1_a * collision_point_x + trajectory_1_b
        return collision_point_x, collision_point_y

    def get_collision_points(self, particle_1: Particle, particle_2: Particle) -> ((float, float), (float, float)):
        particle_1_trajectory = self.get_trajectory(particle_1)
        particle_2_trajectory = self.get_trajectory(particle_2)
        crossing_point = self.get_crossing_point(particle_1, particle_2)

        delta_x = None
        delta_y = None

        crossing_angle = abs(particle_1_trajectory[0] - particle_2_trajectory[0])
        for i in range(2):
            if particle_1.get_position()[0] < crossing_point[0] and particle_1.get_position()[1] < crossing_point[1] \
                and particle_2.get_position()[0] > crossing_point[0] and particle_2.get_position()[1] < crossing_point[1]:
                    delta_x = self.particle_size
                    delta_y = self.particle_size / math.tan(crossing_angle / 2)
                    return (particle_1.get_position()[0] - delta_x,
                                    particle_1.get_position()[1] - delta_y), \
                            (particle_2.get_position()[0] + delta_x,
                                     particle_2.get_position()[1] - delta_y)

            elif particle_1.get_position()[0] > crossing_point[0] and particle_1.get_position()[1] < crossing_point[1] \
                and particle_2.get_position()[0] > crossing_point[0] and particle_2.get_position()[1] > crossing_point[1]:
                    delta_x = self.particle_size / math.tan((180 - crossing_angle) / 2)
                    delta_y = self.particle_size

            elif particle_1.get_position()[0] > crossing_point[0] and particle_1.get_position()[1] > crossing_point[1] \
                and particle_2.get_position()[0] < crossing_point[0] and particle_2.get_position()[1] > crossing_point[1]:
                    delta_x = self.particle_size
                    delta_y = self.particle_size / math.tan(crossing_angle)
            elif particle_1.get_position()[0] < crossing_point[0] and particle_1.get_position()[1] > crossing_point[1] \
                and particle_2.get_position()[0] < crossing_point[0] and particle_2.get_position()[1] < crossing_point[1]:
                    delta_x = self.particle_size / math.tan((180 - crossing_angle) / 2)
                    delta_y = self.particle_size



    def get_travel_time(self, particle, destination: List[float,float]) -> float:
        distance_to_travel = self.distance(particle.get_position(),
                                           destination)

        combined_speed = particle.get_combined_speed()
        return distance_to_travel / combined_speed

    def will_collide(self, particle_1: Particle, particle_2: Particle) -> bool:
        particle_1_trajectory = self.get_trajectory(particle_1)
        particle_2_trajectory = self.get_trajectory(particle_2)

        crossing_point = self.get_crossing_point(particle_1, particle_2)

        if particle_1_trajectory[0] != particle_2_trajectory[0]:
            if not (crossing_point[0] > particle_1.get_position()[0] and particle_1.get_velocity()[0] > 0):
                return False
            elif not (crossing_point[0] < particle_1.get_velocity()[0] and particle_1.get_velocity()[0] < 0):
                return False
            elif not(crossing_point[1] > particle_1.get_position()[1] and particle_1.get_velocity()[1] > 0):
                return False
            elif not(crossing_point[1] < particle_1.get_position()[1] and particle_1.get_velocity()[1] < 0):
                return False

            if not (crossing_point[0] > particle_2.get_position()[0] and particle_2.get_velocity()[0] > 0):
                return False
            elif not (crossing_point[0] < particle_2.get_velocity()[0] and particle_2.get_velocity()[0] < 0):
                return False
            elif not (crossing_point[1] > particle_2.get_position()[1] and particle_2.get_velocity()[1] > 0):
                return False
            elif not (crossing_point[1] < particle_2.get_position()[1] and particle_2.get_velocity()[1] < 0):
                return False

            particle_1_travel_time = self.get_travel_time(particle_1, crossing_point)
            particle_2_travel_time = self.get_travel_time(particle_2, crossing_point)

            if abs(particle_1_travel_time - particle_2_travel_time) <= self.maximal_timedelta_as_colliding:
                return True

        else:
            return False


