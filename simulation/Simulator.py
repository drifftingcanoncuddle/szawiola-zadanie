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
    """
    Simulation engine.
    All scripts generate list of SimFrames, and pickle it to file -> simulation.sim
    """
    def __init__(self):
        self.time_delta = float(ConfigManipulator().read(ConfigFields.timeDelta))
        self.size_x = float(ConfigManipulator().read(ConfigFields.size))
        self.size_y = float(ConfigManipulator().read(ConfigFields.size))
        self.maximal_distance_as_collision = float(ConfigManipulator().read(ConfigFields.maximalDistanceAsCollision))
        self.maximal_timedelta_as_colliding = float(ConfigManipulator().read(ConfigFields.maximalTimeDeltaAsColliding))
        self.particle_size = float(ConfigManipulator().read(ConfigFields.particleSize))
        self.time = int(ConfigManipulator().read(ConfigFields.time))

    def dump(self):
        """
        Conduct simulation and save it to file
        :return: nth
        """
        frames_count = 0

        states = list()
        states.append(Initiator().create())

        while frames_count < self.time:
            print("Simulating frame: ", frames_count)
            frames_count += 1
            # we need to make deep copy before we can make next simulaiton
            # otherwise simulation tries to simulate itself
            # python quirk
            f = copy.deepcopy(states[-1])
            new_state = self.simulate(f)
            states.append(new_state)

        # pickle
        with open("simulation.sim", "wb") as file:
            pickle.dump(states, file)

    def simulate(self, frame: SimFrame) -> SimFrame:

        """
        funciton takes one simframe and simulate all changes in world during delta_time
        delta_time is described in config
        :param frame: frame to simulate
        :return: new frame after proceeding some time
        """

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


    # set of lovely overloaded functions for calculating distance between two objects
    # all of them use Pythagoras theorem

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
        """
        Function moves particle, based on distance which it can pass during given time
        :param particle: particle to move
        :param time: time elapsing
        :return: new, moved particle
        """
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
        """
        Function collide two particle which each other.

        We never consider collision for 0 degree angle, even if it happens (?) - rounding errors -
        so we always add some small value, for case this situation can occur, and then we get some
        small angle approaching 0

        Afterwards we calculate rotation between basic XY coord system and collision system
        Transform speed components to match new coord system

        Make collision

        Transform collision system to basic XY system

        And tricky part :)
        There are situations in which two particles are considered as colliding when distance
        between their centers are smaller than sum of their radius - there are clipping each other.
        In this situation engine in next simulation, will try to instantly collide each other so
        we finish up with infinity loop of collision. It seems like two or more particles get
        glued and are shivering.
        So to avoid situation like this we need to fix their positions so sum of their radius are
        smaller than distance between their centers, that is called fixing

        Also if particles are close enough to wall, collisions witch each other are disabled

        :param particle_1:
        :param particle_2:
        :return: particles after collision
        """

        if particle_1.get_position()[0] > self.size_x - self.particle_size * 1.5 \
                or particle_1.get_position()[0] < self.particle_size  \
                or particle_1.get_position()[1] > self.size_y - self.particle_size \
                or particle_1.get_position()[1] < self.particle_size :
            return particle_1, particle_2

        if particle_2.get_position()[0] > self.size_x - self.particle_size * 1.5 \
                or particle_2.get_position()[0] < self.particle_size  \
                or particle_2.get_position()[1] > self.size_y - self.particle_size \
                or particle_2.get_position()[1] < self.particle_size:
            return particle_1, particle_2

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
        """
        Calculate collision with wall.

        :param particle: particle to collide
        :param wall: wall name to collide
        :return: new particle after collision
        """
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
        """
        As we takes, that particle moves along straight line we cen evaluate
        a and b components of line equation
        :param particle: particle wich trajectory we like to know
        :return: a and b tuple
        """
        particle_vx = particle.get_velocity()[0]
        particle_vy = particle.get_velocity()[1]

        particle_x = particle.get_position()[0]
        particle_y = particle.get_position()[1]

        if particle_vx == 0:
            a = 10 ** 20
        else:
            a = particle_vy / particle_vx

        b = particle_y - a * particle_x

        return a, b

    def wall_collision(self, particle: Particle) -> str:
        """
        Detect if particle is colliding with wall
        We consider wall collision only if distance between wall and particle is lesser than
        half of radius of particle.

        So if collision is detected, engine instantly moves particle to so distance between particle
        and wall is greater than half of radius and negate proper component of speed

        Letting particle clip with the wall is necessary, other wise engine could detects new collision
        right after previous collision, as particle potentially cannot leave collision zone in time,
        for example because it has insufficient component speed.

        So letting for clip, and some small teleportaions provide us zone,
         which could be passed in only one direction, towards wall, and leaved just after collision

        :param particle: particle to collide
        :return: None if there is no collision, otherwise wall to collide
        """
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

