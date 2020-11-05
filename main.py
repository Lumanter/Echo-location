import pygame
import math
from point import Point
from sonar import Sonar
from line_segment import LineSegment
from unit_vector import UnitVector
from monter_ray_generator import MonterRayGenerator
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


def get_generated_echo_pixel(ray, sonar, line_obstacles):
    #if ray.traveled_distance > 0 and sonar.sonar_collision(ray.vector):
    if sonar.sonar_collision(ray.vector):
        print("sonar collision!")
        return EchoPixel(255, Point(50, 50))

    reflection_point = None
    for line_obstacle in line_obstacles:
        reflection_point = line_obstacle.get_intersection_point(ray.vector)
        if reflection_point is not None:
            break

    if reflection_point is not None:
        print("reflection!")
        return

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
                sonar_ray = Ray(sonar_ray_vector.angle, sonar_ray_vector)

                echo_pixel = get_generated_echo_pixel(sonar_ray, sonar, line_obstacles)
                if echo_pixel is not None:
                    echo_pixels.append(echo_pixel)

                """for line_obstacle in line_obstacles:
                    reflection_point = line_obstacle.get_intersection_point(sonar_ray)
                    if reflection_point is not None:
                        reflected_vector = line_obstacle.get_reflected_vector(reflection_point, sonar_ray)

                        sonar.sonar_collision(reflected_vector) # test stuff
                        angle_range = line_segment.get_reflection_angle_range(reflection_point, sonar_ray)
                        print("Reflection angle range: (", math.degrees(angle_range.min), ", ", math.degrees(angle_range.max), ")")

                        sonar_view_angle_range = sonar.get_view_angle_range()
                        print("Sonar view angle range: (", math.degrees(sonar_view_angle_range.min), ", ", math.degrees(sonar_view_angle_range.max), ")")
                         
                        monte=MonterRayGenerator()
                        initial_rays=monte.get_initial_sonar_rays(sonar.center_point,sonar_view_angle_range)
                        print("Rayo principal: ")
                        initial_rays[0].__str__()
                        print("Rayos de foco: ")
                        monte.get_spotlight_rays(initial_rays[0],0)"""


