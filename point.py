import pygame
import math

class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __add__(self, other):
        return Point(self.x + other.x, self.y + other.y)

    def __sub__(self, other):
        return Point(self.x - other.x, self.y - other.y)

    def __truediv__(self, other):
        return Point(self.x / other, self.y / other)

    def dot_product(self, other):
        return (self.x * other.x) + (self.y * other.y)

    def cross_product(self, other):
        return (self.x * other.y) - (self.y * other.x)

    def get_angle_to(self, other):
        angle = math.atan2(other.y - self.y, other.x - self.x)
        if angle < 0:
            angle += math.pi * 2
        return angle
    def get_distance_to(self,other):
        return math.sqrt((self.x - other.get_x())**2+(self.y - other.get_y())**2)

    def get_tuple(self):
        return int(self.x), int(self.y)

    def __str__(self):
        return str((self.x, self.y))

    def __repr__(self):
        return self.__str__()
        
    def get_x(self):
        return self.x

    def get_y(self):
        return self.y

    def draw(self, window, color=(255, 255, 255), radius=4):
        pygame.draw.circle(window, color, self.get_tuple(), radius)