import pygame
from math import radians, degrees
from point import Point
from sonar import Sonar
from line_segment import LineSegment
from unit_vector import UnitVector
from ray_generator import RayGenerator
from ray import Ray
from echo_pixel import EchoPixel

screen_width = 500
screen_height = 500
window = pygame.display.set_mode((screen_width, screen_height))
center_point = Point(int(screen_width / 2), int(screen_height / 2))

sonar = Sonar(center_point)
echo_pixels = []

line_obstacles = [LineSegment(Point(150, 150), Point(350, 150)), LineSegment(Point(100, 450), Point(400, 450)), LineSegment(Point(50, 100), Point(50, 400)), LineSegment(Point(450, 100), Point(450, 400))]
reflected_vector = None


def get_nearest_intersected_line(vector, line_obstacles):
    nearest_intersected_obstacle = None
    smallest_intersection_distance = float('inf')

    for line_obstacle in line_obstacles:
        reflection_point = line_obstacle.get_intersection_point(vector)
        if reflection_point is not None and reflection_point != vector.origin_point:

            distance_to_reflection = vector.origin_point.get_distance_to(reflection_point)
            if distance_to_reflection < smallest_intersection_distance:
                nearest_intersected_obstacle = line_obstacle
                smallest_intersection_distance = distance_to_reflection
    return nearest_intersected_obstacle


def generate_echo_pixels(source_ray, sonar, line_obstacles, echo_pixels):
    if source_ray.bounces > 8:
        return None

    if sonar.sonar_collision(source_ray.vector):
        print("sonar collision!")
        return EchoPixel(255, Point(50, 50))

    intersected_line = get_nearest_intersected_line(source_ray.vector, line_obstacles)
    ray_bounced = (intersected_line is not None)
    if ray_bounced:
        reflected_ray = RayGenerator().get_reflected_ray(source_ray, intersected_line)
        if reflected_ray.energy > 0:
            print("bounce " + str(reflected_ray.bounces) + ' ' + str(reflected_ray))
            echo_pixels.append(EchoPixel(255, reflected_ray.vector.origin_point))

            generate_echo_pixels(reflected_ray, sonar, line_obstacles, echo_pixels)
    return None


def redraw_window():
    window.fill((5, 5, 5))
    sonar.draw(window)

    for line in line_obstacles:
        line.draw(window, (255, 51, 153))

    if reflected_vector is not None:
        reflected_vector.draw(window, 30, (255, 255, 255))

    for echo_pixel in echo_pixels:
        echo_pixel.draw(window)
    pygame.display.update()

run = True
while run:
    mouse_point = Point(pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1])
    sonar.update_rotation(mouse_point)

    redraw_window()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

        right_mouse_click = (event.type == pygame.MOUSEBUTTONDOWN and event.button == 3)
        if right_mouse_click:
            echo_pixels = []
            reflected_vector = None

        left_mouse_click = (event.type == pygame.MOUSEBUTTONDOWN and event.button == 1)
        if left_mouse_click:
                sonar_ray_vector = UnitVector(center_point, center_point.get_angle_to(mouse_point))
                sonar_ray = Ray(degrees(sonar_ray_vector.angle), sonar_ray_vector)

                print("")
                echo_pixels = []
                generate_echo_pixels(sonar_ray, sonar, line_obstacles, echo_pixels)
