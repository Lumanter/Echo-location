import pygame
import math
from point import Point

class UnitVector:
    """ Unit vector representation.

        Attributes:
            origin_point(:obj:`Point`): Vector origin point.
            angle(float): Vector angle from the origin point, in radians.
            direction_vector(:obj:`Point`): Vector direction vector.
    """
    def __init__(self, origin, angle):
        self.origin_point = origin
        self.angle = angle
        self.direction_vector = Point(math.cos(self.angle), math.sin(self.angle))


    def draw(self, window, lenght=1, color=(255,255,255)):
        """ Draws the vector in the pygame game window.

            Args:
                window(:obj:`Surface`:): Pygame window surface.
                lenght(int): Vector display lenght.
                color(:obj:`List`:): Line color as list of rgb colors.
        """
        x_offset = self.direction_vector.x * lenght
        y_offset = self.direction_vector.y * lenght
        head_point = (self.origin_point.x+x_offset, self.origin_point.y+y_offset)
        pygame.draw.line(window, color, self.origin_point.get_int_tuple(), head_point)
        self.origin_point.draw(window, color, 3)


    def get_origin_point(self):
        return self.origin_point


    def get_direction(self):
        return self.direction_vector


    def projection(self,vector):
        proy=vector.dot_product(self.direction_vector)/(math.sqrt(self.direction_vector.get_x()**2 + self.direction_vector.get_y()**2))
        return Point(proy*self.direction_vector.get_x(), proy*self.direction_vector.get_y()).__add__(self.origin_point)

    def __repr__(self):
        return '('+str(self.origin_point) +', '+ str(self.angle)+')'