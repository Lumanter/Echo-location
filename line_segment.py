import pygame
from point import Point
from math import radians, degrees, pi
from unit_vector import UnitVector
from angle_range import AngleRange


class LineSegment:
    """ Segment of a line.

        Attributes:
            pointA (:obj:`Point`): First line point.
            pointB (:obj:`Point`): Second line point.
    """
    def __init__(self, pointA, pointB):
        self.pointA = pointA
        self.pointB = pointB


    def get_intersection_point(self, vector):
        """ Returns the intersection point between the line and a given vector.

            Args:
                vector (:obj:`UnitVector`): Vector to check intersection.

            Returns:
                :obj:`Point`: Intersection point if occurs intersection, None otherwise.
        """
        v1 = vector.origin_point - self.pointA
        v2 = self.pointB - self.pointA
        v3 = Point(-vector.direction_vector.y, vector.direction_vector.x)

        denominator = v2.dot_product(v3)
        parallel_line_and_vector = (abs(denominator) < 0.000001)
        if parallel_line_and_vector:
            return None 

        t1 = v2.cross_product(v1) / denominator  # distance from origin to intersection
        t2 = v1.dot_product(v3) / denominator  # indicates if the intersection is inside the segment

        intersection_exists = (t1 >= 0.0 and 0.0 <= t2 <= 1.0)
        if intersection_exists:
            x_intersect = vector.origin_point.x + vector.direction_vector.x * t1
            y_intersect = vector.origin_point.y + vector.direction_vector.y * t1
            return Point(x_intersect, y_intersect)
        else:
            return None


    def is_vertical(self):
        """ Indicates if the line is completely vertical.

            Returns:
                bool: True is line is vertical, false otherwise.
        """
        return self.pointA.x == self.pointB.x


    def get_reflected_vector(self, reflection_point, vector):
        """ Returns the reflected vector upon hitting the line segment at a given point.

            Args:
                reflection_point (:obj:`Point`): Point of reflection on the line.
                vector (:obj:`UnitVector`): Vector to be reflected vector.

            Returns:
                :obj:`UnitVector`: Reflected vector.
        """
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


    def get_reflection_angle_range(self, reflection_point, vector):
        """ Returns the range of angles that a vector can take upon hitting the line.

            Args:
                reflection_point (:obj:`Point`): Point of reflection on the line.
                vector (:obj:`UnitVector`): Vector to be reflected.

            Returns:
                :obj:`AngleRange`: Reflection range of angles.
        """
        if self.is_vertical():
            vector_hits_from_left = (vector.origin_point.x < reflection_point.x)
            if vector_hits_from_left:
                return AngleRange(radians(90), radians(270))
            else: # from right
                return AngleRange(radians(270), radians(90))
        else:
            vector_hits_from_above = (vector.origin_point.y < reflection_point.y)
            if vector_hits_from_above:
                return AngleRange(0, radians(180))
            else: # from below
                return AngleRange(radians(180), radians(359))


    @staticmethod
    def get_nearest_intersected_line(vector, line_segments):
        """ Returns the the nearest line segment intersected by a vector

            Args:
                vector (:obj:`UnitVector`): Vector to be check intersection.
                line_segments (:obj:`list` of :obj:`LineSegment`): List of segments to check intersections.

            Returns:
                :obj:`LineSegment`: Nearest intersected line segment if there is intersection, None otherwise.
        """
        nearest_intersected_line = None
        smallest_intersection_distance = float('inf')

        for line_segment in line_segments:
            reflection_point = line_segment.get_intersection_point(vector)
            if reflection_point is not None and reflection_point != vector.origin_point:

                distance_to_reflection = vector.origin_point.get_distance_to(reflection_point)
                if distance_to_reflection < smallest_intersection_distance:
                    nearest_intersected_line = line_segment
                    smallest_intersection_distance = distance_to_reflection
        return nearest_intersected_line


    def draw(self, window, color = (0,0,0)):
        """ Draws the line segment in the pygame game window.

            Args:
                window (:obj:`Surface`:): Pygame window surface.
                color (:obj:`List`:): Line color as list of rgb colors.
        """
        pygame.draw.line(window, color, self.pointA.get_int_tuple(), self.pointB.get_int_tuple())


    def __repr__(self):
        return str(self.pointA) +'-' + str(self.pointB)