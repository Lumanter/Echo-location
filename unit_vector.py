import pygame
import math
from point import Point

class UnitVector:
    def __init__(self, origin, angle):
        self.origin_point = origin
        self.angle = angle
        self.direction_vector = Point(math.cos(self.angle), math.sin(self.angle))

    def draw(self, window, lenght=1, color=(255,255,255)):
        x_offset = self.direction_vector.x * lenght
        y_offset = self.direction_vector.y * lenght
        head_point = (self.origin_point.x+x_offset, self.origin_point.y+y_offset)
        pygame.draw.line(window, color, self.origin_point.get_tuple(), head_point)
        self.origin_point.draw(window, color, 3)

    def __repr__(self):
        return '('+str(self.origin_point) +', '+ str(self.angle)+')'