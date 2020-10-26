import pygame
import math
from vector_utilities import find_angle

class Sonar:
    def __init__(self, center_point):
        self.center_point = center_point
        self.triangle_points = ((237, 235), (237, 265), (263, 250))

    def update_rotation(self, mouse_point):
        center = self.center_point
        angle = find_angle(center, mouse_point)
        pivot = (int(center.x + 25 * math.cos(angle)), int(center.y + 25 * math.sin(angle)))
        left_point = (int(center.x + 15 * math.cos(angle - (math.pi / 2))), int(center.y + 15 * math.sin(angle - (math.pi / 2))))
        right_point = (int(center.x + 15 * math.cos(angle + (math.pi / 2))), int(center.y + 15 * math.sin(angle + (math.pi / 2))))
        self.triangle_points = (pivot, left_point, right_point)

    def draw(self, window):
        pygame.draw.polygon(window, (245, 245, 245), self.triangle_points)