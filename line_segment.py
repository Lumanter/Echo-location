import pygame

class LineSegment:
    def __init__(self, pointA, pointB):
        self.pointA = pointA
        self.pointB = pointB

    def draw(self, window, color = (0,0,0)):
        pygame.draw.line(window, color, self.pointA.get_tuple(), self.pointB.get_tuple())