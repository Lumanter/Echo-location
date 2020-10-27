import pygame
from point import Point
from math import radians, degrees
from unit_vector import UnitVector

class LineSegment:
    def __init__(self, pointA, pointB):
        self.pointA = pointA
        self.pointB = pointB

    def intersects(self, vector):
        v1 = vector.origin_point - self.pointA
        v2 = self.pointB - self.pointA
        v3 = Point(-vector.direction_vector.y, vector.direction_vector.x)

        dot = v2.dot_product(v3)  # se calcula el denominador
        if abs(dot) < 0.000001:  # si dot es 0, el vector y el segmento son paralelos
            return None  # y no hay interseccion

        t1 = v2.cross_product(v1) / dot  # t1 es la distancia del origen hasta la interseccion
        t2 = v1.dot_product(v3) / dot  # t2 indica si la interseccion queda dentro del segmento

        if t1 >= 0.0 and 0.0 <= t2 <= 1.0:
            x_intersect = vector.origin_point.x + vector.direction_vector.x * t1
            y_intersect = vector.origin_point.y + vector.direction_vector.y * t1
            intersection_point = Point(x_intersect, y_intersect)
            return intersection_point
        else:
            return None

    def is_vertical(self):
        return self.pointA.x == self.pointB.x

    def get_reflected_vector(self, reflection_point, vector):
        if self.is_vertical():
            vector_comes_from_below = (reflection_point.y > vector.origin_point.y)
            if vector_comes_from_below:
                reflection_angle = radians(180) - vector.angle
            else:
                reflection_angle = radians(540) - vector.angle
        else:
            reflection_angle = radians(360) - vector.angle
            degrees_vector = degrees(vector.angle)
            degrees_reflection = degrees(reflection_angle)
        reflected_vector = UnitVector(reflection_point, reflection_angle)
        return reflected_vector

    def draw(self, window, color = (0,0,0)):
        pygame.draw.line(window, color, self.pointA.get_tuple(), self.pointB.get_tuple())

    def __repr__(self):
        return str(self.pointA) +'-' + str(self.pointB)