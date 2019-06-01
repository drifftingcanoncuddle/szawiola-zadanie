import math

from Maintain.ConfigManipulator import ConfigManipulator


class Particle:
    def __init__(self, x, y, vX, vY):
        self.x = x
        self.y = y
        self.vX = vX
        self.vY = vY

    def get_position(self) -> (float, float):
        return self.x, self.y

    def get_velocity(self) -> (float, float):
        return self.vX, self.vY

    def get_box_position(self) -> (float, float):
        box_size = int(ConfigManipulator().read("boxSize"))
        box_x = self.x // box_size
        box_y = self.y // box_size
        return box_x, box_y

    def get_combined_speed(self) -> float:
        squared_combined_speed = self.vX ** 2 + self.vY ** 2
        return math.sqrt(squared_combined_speed)
