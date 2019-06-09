import math

from Maintain.ConfigManipulator import ConfigManipulator, ConfigFields


class Particle:
    """
    Class containing definition for one particle
    """
    def __init__(self, x, y, vX, vY):
        self.x = x      # x pos component
        self.y = y      # y pos component
        self.vX = vX    # x speed component
        self.vY = vY    # y speed component

    def get_position(self) -> (float, float):
        """
        position getter
        :return: position tuple
        """
        return self.x, self.y

    def get_velocity(self) -> (float, float):
        """
        speed getter
        :return: spped tuple
        """
        return self.vX, self.vY

    def get_box_position(self) -> (int, int):
        """
        Position getter, but in coordinates described as more generalized.
        Under assumptions one box has side length of k
        we calculate x component of box position as quotient of x position and k
        ceiled if x was < 0 and floored id x > 0.
        Same for y
        :return: box pos tuple
        """
        box_size = int(ConfigManipulator().read(ConfigFields.boxSize))
        if self.x > 0:
            box_x = math.floor(self.x / box_size)
        else:
            box_x = math.ceil(self.x / box_size)

        if self.y > 0:
            box_y = math.floor(self.y / box_size)
        else:
            box_y = math.ceil(self.y / box_size)

        return box_x, box_y

    def get_box_velocities(self) -> (int, int):
        """
        Same as above but for speed
        :return: box speed tuple
        """
        box_size = int(ConfigManipulator().read(ConfigFields.boxSize))
        if self.vX > 0:
            box_x = math.floor(self.vX / box_size)
        else:
            box_x = math.ceil(self.vX / box_size)

        if self.vY > 0:
            box_y = math.floor(self.vY / box_size)
        else:
            box_y = math.ceil(self.vY / box_size)

        return box_x, box_y

    def get_combined_speed(self) -> float:
        """
        calculate combiend speed
        :return: combiend speed as float
        """
        squared_combined_speed = self.vX ** 2 + self.vY ** 2
        return math.sqrt(squared_combined_speed)

    def __str__(self):
        """
        Used to print particle object
        :return:
        """
        return "Position: {}. {}; Velocity {} , {}".format(self.x,
                                                        self.y,
                                                        self.vX,
                                                        self.vY)
