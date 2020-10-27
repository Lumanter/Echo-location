import pygame
from math import cos, sin, radians, pi
from point import Point

class Sonar:
    def __init__(self, center_point, radius=12):
        self.center_point = center_point
        self.radius = radius
        self.triangle_points = None
        self.rotation_angle = 0
        self.update_triangle_points()


    def update_rotation(self, mouse_point):
        self.rotation_angle = self.center_point.get_angle_to(mouse_point)
        self.update_triangle_points()


    def update_triangle_points(self):
        pivot = self.get_point_around_center(self.rotation_angle)
        left_point = self.get_point_around_center(self.rotation_angle + radians(135))
        right_point = self.get_point_around_center(self.rotation_angle + radians(225))
        self.triangle_points = (pivot, left_point, right_point)


    def get_point_around_center(self, angle):
        center = self.center_point
        point = Point(center.x+self.radius, center.y) # initial point to rotate
        x = center.x + cos(angle) * (point.x - center.x) - sin(angle) * (point.y - center.y)
        y = center.x + sin(angle) * (point.x - center.x) + cos(angle) * (point.y - center.y)
        return (x, y)


    def draw(self, window):
        pygame.draw.polygon(window, (245, 245, 245), self.triangle_points)