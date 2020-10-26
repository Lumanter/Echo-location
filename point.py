import pygame

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

    def dot(self, p2):
        return (self.x * p2.x) + (self.y * p2.y)

    def cross(self, p2):
        return (self.x * p2.y) - (self.y * p2.x)

    def get_tuple(self):
        return int(self.x), int(self.y)

    def __str__(self):
        return str(self.get_tuple())

    def __repr__(self):
        return self.__str__()

    def draw(self, window, color=(0, 0, 0), radius=4):
        pygame.draw.circle(window, color, self.get_tuple(), radius)