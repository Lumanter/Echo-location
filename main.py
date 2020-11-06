import pygame
from math import radians, degrees
from point import Point
from sonar import Sonar
from line_segment import LineSegment
from unit_vector import UnitVector
from ray_generator import RayGenerator
from ray import Ray
from echo_pixel import EchoPixel

screen_width = 700
screen_height = 700
window = pygame.display.set_mode((screen_width, screen_height))
center_point = Point(int(screen_width / 2), int(screen_height / 2))

sonar = Sonar(center_point)
line_obstacles = [LineSegment(Point(250, 250), Point(450, 250)), LineSegment(Point(250, 450), Point(450, 450)), LineSegment(Point(250, 250), Point(250, 450)), LineSegment(Point(450, 250), Point(450, 450))]
echo_pixels = []


def generate_echo_pixels(source_ray, sonar, line_obstacles, echo_pixels):
    if source_ray.bounces > 5:
        return

    if sonar.sonar_collision(source_ray.vector):
        source_ray.traveled_distance += sonar.center_point.get_distance_to(source_ray.vector.origin_point)

        pixel_energy = RayGenerator.get_ray_energy_with_distance_loss(source_ray.energy, source_ray.traveled_distance)
        pixel_x, pixel_y = sonar.get_coordinates_around_center(radians(source_ray.angle_from_sonar), int(source_ray.traveled_distance/2))
        generated_echo_pixel = EchoPixel(pixel_energy, Point(pixel_x, pixel_y))
        echo_pixels.append(generated_echo_pixel)
        #print("sonar collision! distance = ", source_ray.traveled_distance)
        return

    intersected_line = LineSegment.get_nearest_intersected_line(source_ray.vector, line_obstacles)
    ray_bounced = (intersected_line is not None)
    if ray_bounced:
        reflected_ray = RayGenerator.get_reflected_ray(source_ray, intersected_line)
        if reflected_ray.energy > 0:
            #print("bounce " + str(reflected_ray.bounces) + ' ' + str(reflected_ray))
            #echo_pixels.append(EchoPixel(100, reflected_ray.vector.origin_point))
            generate_echo_pixels(reflected_ray, sonar, line_obstacles, echo_pixels)


def redraw_window():
    window.fill((5, 5, 5))
    sonar.draw(window)

    for line in line_obstacles:
        line.draw(window, (255, 51, 153))

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

        left_mouse_click = (event.type == pygame.MOUSEBUTTONDOWN and event.button == 1)
        if left_mouse_click:
                #print("")
                initial_sonar_rays = RayGenerator.get_initial_sonar_rays(sonar.center_point, sonar.get_view_angle_range())
                for ray in initial_sonar_rays:
                    generate_echo_pixels(ray, sonar, line_obstacles, echo_pixels)