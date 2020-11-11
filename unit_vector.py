import pygame
import math
from point import Point
from math import cos, sin, degrees


class UnitVector:
    """ Unit vector representation.

        Attributes:
            origin_point (:obj:`Point`): Vector origin point.
            angle (float): Vector angle from the origin point, in radians.
            direction_vector (:obj:`Point`): Vector direction vector.
    """
    def __init__(self, origin, angle):
        self.origin_point = origin
        self.angle = angle
        self.direction_vector = Point(cos(self.angle), sin(self.angle))


    def draw(self, window, length=1, color=(255, 255, 255)):
        """ Draws the vector in the pygame game window.

            Args:
                window (:obj:`Surface`:): Pygame window surface.
                length (int): Vector display length.
                color (:obj:`List`:): Line color as list of rgb colors.
        """
        x_offset = self.direction_vector.x * length
        y_offset = self.direction_vector.y * length
        head_point = (self.origin_point.x+x_offset, self.origin_point.y+y_offset)
        pygame.draw.line(window, color, self.origin_point.get_int_tuple(), head_point)
        self.origin_point.draw(window, color, 3)


    def projection(self,vector):
        proy=vector.dot_product(self.direction_vector)/(math.sqrt(self.direction_vector.get_x()**2 + self.direction_vector.get_y()**2))
        return Point(proy*self.direction_vector.get_x(), proy*self.direction_vector.get_y()).__add__(self.origin_point)


    def get_origin_point(self):
        return self.origin_point


    def get_direction(self):
        return self.direction_vector


    def __str__(self):
        return "<{}, {}°>".format(str(self.origin_point), str(int(degrees(self.angle))))


    def __repr__(self):
        return self.__str__()
