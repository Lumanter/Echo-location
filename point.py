import pygame
import math

class Point:
    """ Point representation.

        Attributes:
            x(float): X axis point.
            y(float): Y axis point.
    """
    def __init__(self, x, y):
        self.x = x
        self.y = y


    def get_angle_to(self, point):
        """ Returns the angle to another point.

            Args:
                point(:obj:`Point`): Another point.

            Returns:
                float: Angle to the other point.
        """
        angle = math.atan2(point.y - self.y, point.x - self.x)
        if angle < 0:
            angle += math.pi * 2
        return angle


    def get_distance_to(self, point):
        """ Returns the distance to another point.

            Args:
                point(:obj:`Point`): Another point.

            Returns:
                float: Distance to the other point.
        """
        return math.sqrt((self.x - point.get_x()) ** 2 + (self.y - point.get_y()) ** 2)


    def get_int_tuple(self):
        """ Returns point as a tuple of integers

            Returns:
                :obj:`list` of int: Tuple of integers.
        """
        return int(self.x), int(self.y)


    def dot_product(self, point):
        """ Returns the dot product between this point and another.

            Args:
                point(:obj:`Point`): Another point.

            Returns:
                float: Dot product result.
        """
        return (self.x * point.x) + (self.y * point.y)


    def cross_product(self, point):
        """ Returns the cross product between this point and another.

            Args:
                point(:obj:`Point`): Another point.

            Returns:
                float: Cross product result.
        """
        return (self.x * point.y) - (self.y * point.x)


    def __add__(self, other):
        return Point(self.x + other.x, self.y + other.y)


    def __sub__(self, other):
        return Point(self.x - other.x, self.y - other.y)


    def __truediv__(self, other):
        return Point(self.x / other, self.y / other)


    def get_x(self):
        return self.x

    def get_y(self):
        return self.y


    def draw(self, window, color=(255, 255, 255), radius=4):
        """ Draws the point in the pygame game window.

            Args:
                window(:obj:`Surface`:): Pygame window surface.
                radius(int): Point display radius.
                color(:obj:`List`:): Line color as list of rgb colors.
        """
        pygame.draw.circle(window, color, self.get_int_tuple(), radius)


    def __str__(self):
        x, y = self.get_int_tuple()
        return '({}x, {}y)'.format(x, y)


    def __repr__(self):
        return self.__str__()


    def __eq__(self, point):
        return self.x == point.x and self.y == point.y