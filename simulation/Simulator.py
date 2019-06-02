from simulation.Particle import Particle
from simulation.SimFrame import SimFrame
from Maintain.ConfigManipulator import ConfigFields
from Maintain.ConfigManipulator import ConfigManipulator

from Maintain.Exceptions import NeverCollideException

from typing import *

import copy
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
        self.time_delta = float(ConfigManipulator().read(ConfigFields.timeDelta))
        self.size_x = float(ConfigManipulator().read(ConfigFields.size))
        self.size_y = float(ConfigManipulator().read(ConfigFields.size))
        self.maximal_distance_as_collision = float(ConfigManipulator().read(ConfigFields.maximalDistanceAsCollision))
        self.maximal_timedelta_as_colliding = float(ConfigManipulator().read(ConfigFields.maximalTimeDeltaAsColliding))
        self.particle_size = float(ConfigManipulator().read(ConfigFields.particleSize))

    def simulate(self, frame: SimFrame) -> SimFrame:
        particles = frame.get_particles()

        for p in range(len(particles)):
            is_collidong = self.wall_collision(particles[p])
            if is_collidong is not None:
                print(p, is_collidong)
                particles[p] = self.collide_with_wall(particles[p], is_collidong)

        for p1 in range(len(particles)):
            for p2 in range(len(particles)):
                if p1 != p2:
                    if self.distance_p(particles[p1], particles[p2]) - self.particle_size < self.maximal_distance_as_collision:
                        print(self.distance_p(particles[p1], particles[p2]) - self.particle_size)
                        particles[p1], particles[p2] = self.collide_with_particle(particles[p1], particles[p2])

        for p in range(len(particles)):
            particles[p] = self.move(particles[p], self.time_delta)
            print(particles[p])
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

    def move(self, particle: Particle, time: float):
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

        return Particle(particle_1_x, particle_1_y,
                        old_particle_1_vx, old_particle_1_vy), \
                Particle(particle_2_x, particle_2_y,
                         old_particle_2_vx, old_particle_2_vy)

    def collide_with_wall(self, particle, wall):
        if wall == "T":
            return Particle(particle.get_position()[0], particle.get_position()[1],
                            particle.get_velocity()[0], -1 * particle.get_velocity()[1])
        elif wall == "B":
            return Particle(particle.get_position()[0], particle.get_position()[1],
                            particle.get_velocity()[0], -1 * particle.get_velocity()[1])
        elif wall == "L":
            return Particle(particle.get_position()[0], particle.get_position()[1],
                            particle.get_velocity()[0] * -1, particle.get_velocity()[1])
        elif wall == "R":
            return Particle(particle.get_position()[0], particle.get_position()[1],
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

    def get_crossing_point(self, particle_1: Particle, particle_2: Particle) -> (float, float):
        trajectory_1 = self.get_trajectory(particle_1)
        trajectory_2 = self.get_trajectory(particle_2)

        trajectory_1_a = trajectory_1[0]
        trajectory_1_b = trajectory_1[1]

        trajectory_2_a = trajectory_2[0]
        trajectory_2_b = trajectory_2[1]

        # print(trajectory_1_a, trajectory_2_a)

        collision_point_x = (trajectory_2_b - trajectory_1_b) / (trajectory_1_a - trajectory_2_a)
        collision_point_y = trajectory_1_a * collision_point_x + trajectory_1_b
        return collision_point_x, collision_point_y

    def get_collision_points(self, particle_1: Particle, particle_2: Particle) -> ((float, float), (float, float)):
        particle_1_trajectory = self.get_trajectory(particle_1)
        particle_2_trajectory = self.get_trajectory(particle_2)
        crossing_point = self.get_crossing_point(particle_1, particle_2)

        delta_x = None
        delta_y = None

        crossing_angle = abs(math.atan(particle_1_trajectory[0]) - math.atan(particle_2_trajectory[0]))

        for i in range(2):
            # 1 -> bottom - left
            # 2 -> bottom - right
            if particle_1.get_position()[0] < crossing_point[0] and particle_1.get_position()[1] < crossing_point[1] \
                and particle_2.get_position()[0] > crossing_point[0] and particle_2.get_position()[1] < crossing_point[1]:
                    delta_x = self.particle_size
                    delta_y = self.particle_size / math.tan(crossing_angle / 2)
                    return (particle_1.get_position()[0] - delta_x,
                                    particle_1.get_position()[1] - delta_y), \
                            (particle_2.get_position()[0] + delta_x,
                                     particle_2.get_position()[1] - delta_y)

            # 1 -> bottom right
            # 2 -> upper right
            elif particle_1.get_position()[0] > crossing_point[0] and particle_1.get_position()[1] < crossing_point[1] \
                and particle_2.get_position()[0] > crossing_point[0] and particle_2.get_position()[1] > crossing_point[1]:
                    delta_x = self.particle_size / math.tan((180 - crossing_angle) / 2)
                    delta_y = self.particle_size
                    return (particle_1.get_position()[0] + delta_x,
                                particle_1.get_position()[1] - delta_y),\
                           (particle_2.get_position()[0] + delta_x,
                                particle_2.get_position()[1] + delta_y)

            # 1 -> upper right
            # 2 -> upper left
            elif particle_1.get_position()[0] > crossing_point[0] and particle_1.get_position()[1] > crossing_point[1] \
                and particle_2.get_position()[0] < crossing_point[0] and particle_2.get_position()[1] > crossing_point[1]:
                    delta_x = self.particle_size
                    delta_y = self.particle_size / math.tan(crossing_angle)
                    return (particle_1.get_position()[0] + delta_x,
                                particle_1.get_position()[1] + delta_y),\
                           (particle_2.get_position()[0] - delta_x,
                                particle_2.get_position()[1] + delta_y)

            # 1 -> upper left
            # 2 -> bottom left
            elif particle_1.get_position()[0] < crossing_point[0] and particle_1.get_position()[1] > crossing_point[1] \
                and particle_2.get_position()[0] < crossing_point[0] and particle_2.get_position()[1] < crossing_point[1]:
                    delta_x = self.particle_size / math.tan((180 - crossing_angle) / 2)
                    delta_y = self.particle_size
                    return (particle_1.get_position()[0] - delta_x,
                                particle_1.get_position()[1] + delta_y),\
                           (particle_2.get_position()[0] - delta_x,
                                particle_2.get_position()[1] - delta_y)

            # 1 -> bottom right
            # 2 -> bottom left
            elif particle_2.get_position()[0] < crossing_point[0] and particle_2.get_position()[1] < crossing_point[1] \
                    and particle_1.get_position()[0] > crossing_point[0] and particle_1.get_position()[1] < \
                    crossing_point[1]:
                delta_x = self.particle_size
                delta_y = self.particle_size / math.tan(crossing_angle / 2)
                return (particle_1.get_position()[0] + delta_x,
                        particle_1.get_position()[1] - delta_y), \
                       (particle_2.get_position()[0] - delta_x,
                        particle_2.get_position()[1] - delta_y)

            # 1 -> upper right
            # 2 -> bottom right
            elif particle_2.get_position()[0] > crossing_point[0] and particle_2.get_position()[1] < crossing_point[1] \
                    and particle_1.get_position()[0] > crossing_point[0] and particle_1.get_position()[1] > \
                    crossing_point[1]:
                delta_x = self.particle_size / math.tan((180 - crossing_angle) / 2)
                delta_y = self.particle_size
                return (particle_1.get_position()[0] + delta_x,
                        particle_1.get_position()[1] + delta_y), \
                       (particle_2.get_position()[0] + delta_x,
                        particle_2.get_position()[1] - delta_y)

            # 1 -> upper left
            # 2 -> upper right
            elif particle_2.get_position()[0] > crossing_point[0] and particle_2.get_position()[1] > crossing_point[1] \
                    and particle_1.get_position()[0] < crossing_point[0] and particle_1.get_position()[1] > \
                    crossing_point[1]:
                delta_x = self.particle_size
                delta_y = self.particle_size / math.tan(crossing_angle)
                return (particle_1.get_position()[0] - delta_x,
                        particle_1.get_position()[1] + delta_y), \
                       (particle_2.get_position()[0] + delta_x,
                        particle_2.get_position()[1] + delta_y)

            # 1-> bottom left
            # 2 -> upper left
            elif particle_2.get_position()[0] < crossing_point[0] and particle_2.get_position()[1] > crossing_point[1] \
                    and particle_1.get_position()[0] < crossing_point[0] and particle_1.get_position()[1] < \
                    crossing_point[1]:
                delta_x = self.particle_size / math.tan((180 - crossing_angle) / 2)
                delta_y = self.particle_size
                return (particle_1.get_position()[0] - delta_x,
                        particle_1.get_position()[1] - delta_y), \
                       (particle_2.get_position()[0] - delta_x,
                        particle_2.get_position()[1] + delta_y)

    def get_travel_time(self, particle, destination: Tuple[float]) -> float:
        distance_to_travel = self.distance(particle,
                                           destination)

        combined_speed = particle.get_combined_speed()
        return distance_to_travel / combined_speed

    def will_collide(self, particle_1: Particle, particle_2: Particle) -> bool:
        particle_1_trajectory = self.get_trajectory(particle_1)
        particle_2_trajectory = self.get_trajectory(particle_2)

        crossing_point = self.get_crossing_point(particle_1, particle_2)

        if particle_1_trajectory[0] != particle_2_trajectory[0]:
            # coming from...

            # left
            if not (crossing_point[0] > particle_1.get_position()[0] and particle_1.get_velocity()[0] > 0):
                return False

            # right
            elif not (crossing_point[0] < particle_1.get_velocity()[0] and particle_1.get_velocity()[0] < 0):
                return False

            # bottom
            elif not(crossing_point[1] > particle_1.get_position()[1] and particle_1.get_velocity()[1] > 0):
                return False

            # top
            elif not(crossing_point[1] < particle_1.get_position()[1] and particle_1.get_velocity()[1] < 0):
                return False

            # coming form...

            # left
            if not (crossing_point[0] > particle_2.get_position()[0] and particle_2.get_velocity()[0] > 0):
                return False

            # right
            elif not (crossing_point[0] < particle_2.get_velocity()[0] and particle_2.get_velocity()[0] < 0):
                return False

            # bottom
            elif not (crossing_point[1] > particle_2.get_position()[1] and particle_2.get_velocity()[1] > 0):
                return False

            # top
            elif not (crossing_point[1] < particle_2.get_position()[1] and particle_2.get_velocity()[1] < 0):
                return False

            particle_1_travel_time = self.get_travel_time(particle_1, crossing_point)
            particle_2_travel_time = self.get_travel_time(particle_2, crossing_point)

            if abs(particle_1_travel_time - particle_2_travel_time) <= self.maximal_timedelta_as_colliding:
                return True

        else:
            return False

    def wall_collision(self, particle: Particle) -> str:
        particle_x = particle.get_position()[0]
        particle_y = particle.get_position()[1]

        if particle_x < self.particle_size / 2:
            return "L"
        elif particle_x > self.size_x - self.particle_size / 2:
            return "R"
        elif particle_y > self.size_y - self.particle_size / 2:
            return "T"
        elif particle_y < self.particle_size / 2:
            return "B"
        else:
            return None

