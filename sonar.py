import pygame
from math import cos, sin, radians, degrees
from point import Point
from angle_range import AngleRange

class Sonar:
    """ Sonar that emits sound rays.

        Attributes:
            center_point (:obj:`Point`): Sonar center point.
            radius (int): Sonar radius used for display and collision detection.
            view_angle (int): Sonar view angle, used when sound rays are emitted.
            mouse_point (:obj:`Point`): Point of the mouse coordinates.
            rotation_angle (float): Sonar rotation angle, in radians.
            triangle_points (:obj:`list` of :obj:`list`): Sonar triangle points used for display.
            field_of_view_points (:obj:`list` of :obj:`list`): Sonar field of view points used for display.
    """
    def __init__(self, center_point, radius = 15, view_angle_range = radians(15)):
        self.center_point = center_point
        self.radius = radius
        self.view_angle = view_angle_range
        self.mouse_point = Point(0, 0)

        self.rotation_angle = 0
        self.triangle_points = None
        self.field_of_view_points = None
        self.update_triangle_points()
        self.update_field_of_view_points()


    def update_rotation(self, mouse_point):
        """ Updates the sonar rotation.

            Args:
                mouse_point (:obj:`Point`): Mouse click point.
        """
        self.rotation_angle = self.center_point.get_angle_to(mouse_point)
        self.mouse_point = mouse_point
        self.update_triangle_points()
        self.update_field_of_view_points()


    def update_triangle_points(self):
        """ Updates the rotation of the sonar triangle points.
        """
        pivot = self.get_coordinates_around_center(self.rotation_angle, self.radius)
        left_point = self.get_coordinates_around_center(self.rotation_angle + radians(135), self.radius)
        right_point = self.get_coordinates_around_center(self.rotation_angle + radians(225), self.radius)
        self.triangle_points = (pivot, left_point, right_point)


    def update_field_of_view_points(self):
        """ Updates the rotation of the sonar field of view points.
        """
        left_angle = self.rotation_angle + (self.view_angle/2)
        left_angle = (left_angle - radians(360)) if (degrees(left_angle) > 360) else left_angle  # adjust over 360 angle
        right_angle = self.rotation_angle - (self.view_angle / 2)
        right_angle = (right_angle + radians(360)) if (right_angle < 0) else right_angle # adjust negative angle

        field_of_view_length = self.radius + 25
        left_view_point = self.get_coordinates_around_center(left_angle, field_of_view_length)
        right_view_point = self.get_coordinates_around_center(right_angle, field_of_view_length)
        self.field_of_view_points = (self.center_point.get_int_tuple(), left_view_point, right_view_point)


    def get_coordinates_around_center(self, angle, distance):
        """ Returns the x,y coordinates around the sonar center from a given angle and distance.

            Args:
                angle (float): Rotation value from the sonar perspective.
                distance (int): Distance from the sonar to the coordinates.

            Returns:
                :obj:`list` of float: Tuple of coordinates.
        """
        center = self.center_point
        point = Point(center.x+distance, center.y) # initial point to rotate
        x = center.x + cos(angle) * (point.x - center.x) - sin(angle) * (point.y - center.y)
        y = center.x + sin(angle) * (point.x - center.x) + cos(angle) * (point.y - center.y)
        return x, y


    def collides(self, vector):
        """ Indicates if a vector collides with the sonar.

            Args:
                vector (:obj:`UnitVector`): Vector to check collision.

            Returns:
                bool: True if collides, false otherwise.
        """
        if self.center_point.get_x() != vector.get_origin_point().get_x() and self.center_point.get_y() != vector.get_origin_point().get_y():
            vector_ori_c = self.center_point.__sub__(vector.get_origin_point())
            point_closest = vector.projection(vector_ori_c)
            dis = self.center_point.get_distance_to(point_closest)
            return dis < self.radius
        return False


    def get_view_angle_range(self):
        """ Returns the sonar view angle range. Range depends on the current pivot point
            and the sonar view angle.

            Returns:
                :obj:`AngleRange`: View angle range.
        """
        pivot_point = Point(self.triangle_points[0][0], self.triangle_points[0][1])
        pivot_angle = self.center_point.get_angle_to(pivot_point)

        min_angle = degrees(pivot_angle - (self.view_angle / 2))
        max_angle = degrees(pivot_angle + (self.view_angle / 2))

        min_angle = (360 + min_angle) if (min_angle < 0) else min_angle # adjust negative angle
        max_angle = (max_angle - 360) if (max_angle > 360) else max_angle # adjust over 360 angle
        return AngleRange(radians(min_angle), radians(max_angle))


    def draw(self, window):
        """ Draws the sonar in the pygame game window.

            Args:
                window (:obj:`Surface`:): Pygame window surface.
        """
        dark_grey = (45, 45, 45)
        pygame.draw.line(window, dark_grey, self.center_point.get_int_tuple(), self.mouse_point.get_int_tuple(), 3) # draw view line
        pygame.draw.polygon(window, dark_grey, self.field_of_view_points) # draw field of view
        pygame.draw.polygon(window, (245, 245, 245), self.triangle_points) # draw triangle sonar
